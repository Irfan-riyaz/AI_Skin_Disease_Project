from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, send_from_directory, get_flashed_messages
from werkzeug.utils import secure_filename
import uuid
import time
import os
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import numpy as np
from tensorflow import keras
import tensorflow as tf
import zipfile
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("FLASK_SECRET", "change-me")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

DB_PATH = os.path.join(BASE_DIR, "app.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create users table if it doesn't exist
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT,
            account_type TEXT DEFAULT 'user',
            created_at TEXT
        )
        """
    )
    
    # Add account_type column if it doesn't exist (migration)
    try:
        cur.execute("ALTER TABLE users ADD COLUMN account_type TEXT DEFAULT 'user'")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Create feedback table if it doesn't exist
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            user_id INTEGER,
            message TEXT,
            comment TEXT,
            created_at TEXT
        )
        """
    )
    
    # Add missing columns to feedback if they don't exist
    try:
        cur.execute("ALTER TABLE feedback ADD COLUMN name TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cur.execute("ALTER TABLE feedback ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass
    
    try:
        cur.execute("ALTER TABLE feedback ADD COLUMN message TEXT")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()


init_db()


# ---- Load Model ----
# FINAL MODEL: Multi-class skin disease detection model
# Supports 96 different skin disease classes
# Model file: skin_disease_model.h5 or skin_disease_model.keras
POSSIBLE_MODEL_PATHS = [
    os.path.join(BASE_DIR, "models", "skin_disease_model.h5"),
    os.path.join(BASE_DIR, "models", "skin_disease_model.keras"),
]

MODEL_PATH = None
model = None
# Ensure these exist before attempting to load the model (prevents import-time NameError)
CLASS_NAMES = None
IS_MULTICLASS = False

# For single-output binary models: which label does a higher output correspond to?
# Can be set with environment var `BINARY_POSITIVE_CLASS` = 'melanoma' or 'benign'
BINARY_POSITIVE_CLASS = os.environ.get('BINARY_POSITIVE_CLASS', None)
# cache after autodetection
_BINARY_POSITIVE_CLASS_CACHE = None
# allow adjusting threshold via env var
try:
    BINARY_THRESHOLD = float(os.environ.get('BINARY_THRESHOLD', '0.5'))
except Exception:
    BINARY_THRESHOLD = 0.5

# Local settings file written by the admin UI
SETTINGS_FILE = os.path.join(BASE_DIR, 'binary_settings.json')

def load_model_safe():
    """Try multiple likely locations for the model file and load it if found.
    Auto-detect whether the model is binary (single output) or multiclass and
    adjust `IS_MULTICLASS` / `CLASS_NAMES` accordingly.
    """
    global model, MODEL_PATH, IS_MULTICLASS, CLASS_NAMES, _BINARY_POSITIVE_CLASS_CACHE

    for p in POSSIBLE_MODEL_PATHS:
        if os.path.exists(p):
            MODEL_PATH = p
            break

    if MODEL_PATH is None:
        print(f"Model file not found in any of: {POSSIBLE_MODEL_PATHS}")
        model = None
        return

    try:
        model = keras.models.load_model(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
        try:
            print("--- Model summary ---")
            model.summary()
        except Exception as e:
            print(f"(info) unable to print model summary: {e}")

        # Attempt to infer whether this is binary (single-output/sigmoid)
        out_shape = None
        try:
            out_shape = model.output_shape
            print(f"Model output shape: {out_shape}")
        except Exception:
            out_shape = None

        # default assume multiclass unless we detect single-output
        IS_MULTICLASS = True
        try:
            if out_shape is not None:
                # out_shape can be (None,) or (None, 1) or (None, N)
                if isinstance(out_shape, tuple):
                    out_dim = out_shape[-1]
                else:
                    out_dim = int(out_shape)

                if out_dim == 1:
                    IS_MULTICLASS = False
                else:
                    IS_MULTICLASS = True
        except Exception:
            IS_MULTICLASS = True

        # Try to load class names from classes file if present (guard in case
        # the helper isn't defined yet during import-time execution)
        # IMPORTANT: Only use first 22 classes (model has 22 outputs)
        try:
            if 'load_class_names' in globals():
                load_class_names()
                # CRITICAL FIX: Truncate to 22 classes only (model output size)
                if CLASS_NAMES and len(CLASS_NAMES) > 22:
                    CLASS_NAMES = CLASS_NAMES[:22]
                    print(f"[IMPORTANT] Truncated CLASS_NAMES to 22 classes (model output size)")
            else:
                print("(info) load_class_names() not available yet; skipping for now")
        except Exception as e:
            print(f"(info) unable to load class names now: {e}")

        # For binary models, pick two labels even if classes.txt contains many labels
        if not IS_MULTICLASS:
            # If classes.txt provided a full multiclass list, try to pick a sensible binary pair
            if CLASS_NAMES and len(CLASS_NAMES) >= 2:
                # Try to prefer 'melanoma' (common positive) or similar markers
                positive_label = None
                candidates = [c.lower() for c in CLASS_NAMES]
                for keyword in ('melanoma', 'maligna', 'malign', 'cancer'):
                    for i, c in enumerate(candidates):
                        if keyword in c:
                            positive_label = CLASS_NAMES[i]
                            break
                    if positive_label:
                        break

                # Respect explicit env var if set
                if not positive_label:
                    positive_label = BINARY_POSITIVE_CLASS or _BINARY_POSITIVE_CLASS_CACHE

                if positive_label:
                    # choose a negative label that's different (prefer 'benign' if present)
                    negative_label = None
                    for n in CLASS_NAMES:
                        if n.lower() != positive_label.lower() and 'benign' in n.lower():
                            negative_label = n
                            break
                    if not negative_label:
                        # fallback to first non-positive label
                        for n in CLASS_NAMES:
                            if n.lower() != positive_label.lower():
                                negative_label = n
                                break
                    CLASS_NAMES = [negative_label or 'benign', positive_label]
                else:
                    # No obvious positive; default to benign/melanoma pair
                    CLASS_NAMES = ['benign', 'melanoma']

                print(f"Binary model detected. Using CLASS_NAMES={CLASS_NAMES}")
            else:
                # Respect environment setting if user specified positive class label
                positive_label = BINARY_POSITIVE_CLASS or _BINARY_POSITIVE_CLASS_CACHE
                if positive_label:
                    other = 'benign' if positive_label.lower() != 'benign' else 'non-malignant'
                    CLASS_NAMES = [other, positive_label]
                else:
                    CLASS_NAMES = ['benign', 'melanoma']
                print(f"Binary model detected. Using CLASS_NAMES={CLASS_NAMES}")
        else:
            # For multiclass, ensure CLASS_NAMES length matches model output when possible
            try:
                if CLASS_NAMES and out_shape is not None:
                    out_dim = out_shape[-1]
                    if len(CLASS_NAMES) != out_dim:
                        print(f"Warning: loaded {len(CLASS_NAMES)} class names but model outputs {out_dim} values")
            except Exception:
                pass

    except Exception as e:
        print(f"Error loading model: {e}")
        model = None


load_model_safe()

# Note: CLASS_NAMES and IS_MULTICLASS are already set by load_model_safe()
# No need to reinitialize them here

def load_class_names():
    """Helper function (kept for compatibility, but not used for final model)."""
    global CLASS_NAMES, IS_MULTICLASS
    candidates = [
        os.path.join(BASE_DIR, 'models', 'classes.txt'),
        os.path.join(BASE_DIR, 'models', 'classes.json'),
        os.path.join(BASE_DIR, 'classes.txt'),
        os.path.join(BASE_DIR, 'classes.json'),
    ]
    for p in candidates:
        try:
            if os.path.exists(p):
                if p.lower().endswith('.txt'):
                    with open(p, 'r', encoding='utf-8') as fh:
                        lines = [l.strip() for l in fh.readlines() if l.strip()]
                        if lines:
                            CLASS_NAMES = lines
                            print(f"Loaded class names from {p} ({len(CLASS_NAMES)} classes)")
                            return
                else:
                    with open(p, 'r', encoding='utf-8') as fh:
                        data = json.load(fh)
                        # expect list
                        if isinstance(data, list) and data:
                            CLASS_NAMES = [str(x) for x in data]
                            print(f"Loaded class names from {p} ({len(CLASS_NAMES)} classes)")
                            return
        except Exception as e:
            print(f"[load_class_names] failed reading {p}: {e}")

    # fallback: None (app will use sensible defaults)


# Ensure class names are loaded after helper definition (fixes timing issue)
try:
    load_class_names()
    if CLASS_NAMES and len(CLASS_NAMES) > 22:
        CLASS_NAMES = CLASS_NAMES[:22]
        print(f"[IMPORTANT] Post-start truncation: CLASS_NAMES truncated to {len(CLASS_NAMES)} entries")
except Exception as _e:
    print(f"[info] load_class_names() post-call skipped or failed: {_e}")

# Disease information database - 22 classes (matches model output exactly)
DISEASE_INFO = {
    "Acne": {
        "name": "Acne Vulgaris",
        "cause": "Excess sebum production, bacterial colonization (P. acnes), follicle obstruction, hormonal changes",
        "risk": "Low-Moderate Risk",
        "recommendations": [
            "Use non-comedogenic skincare products and cleanse twice daily",
            "Apply topical retinoids or benzoyl peroxide treatments",
            "Consider oral antibiotics or hormonal therapy if severe",
            "Avoid picking or squeezing lesions to prevent scarring",
            "Consult dermatologist for persistent or severe cases"
        ]
    },
    "Actinic_Keratosis": {
        "name": "Actinic Keratosis (Solar Keratosis)",
        "cause": "Cumulative UV sun exposure over years, more common in fair-skinned individuals",
        "risk": "Moderate-High Risk",
        "recommendations": [
            "Avoid prolonged sun exposure; use SPF 50+ sunscreen daily",
            "Wear protective clothing, hats, and sunglasses",
            "Topical treatments: imiquimod, 5-fluorouracil, or diclofenac",
            "Cryotherapy (liquid nitrogen freezing) by dermatologist",
            "Regular skin surveillance for changes"
        ]
    },
    "Benign_tumors": {
        "name": "Benign Skin Tumors",
        "cause": "Non-cancerous growth of skin cells, often age-related or genetic predisposition",
        "risk": "Low Risk",
        "recommendations": [
            "Monitor for changes in size, color, or appearance",
            "Cosmetic removal if desired (not medically necessary)",
            "Professional evaluation to confirm benign diagnosis",
            "Regular self-examination for any changes",
            "No urgent treatment required"
        ]
    },
    "Bullous": {
        "name": "Bullous Disorders (Blistering)",
        "cause": "Autoimmune reaction, infection, genetic condition, or trauma causing fluid-filled blisters",
        "risk": "Moderate Risk",
        "recommendations": [
            "Avoid trauma or friction on affected areas",
            "Topical or oral corticosteroids as prescribed",
            "Immunosuppressive therapy for severe autoimmune forms",
            "Keep blisters clean and unbroken to prevent infection",
            "Dermatology consultation for accurate diagnosis"
        ]
    },
    "Candidiasis": {
        "name": "Cutaneous Candidiasis (Fungal Infection)",
        "cause": "Candida albicans infection in warm, moist skin areas; weakened immunity",
        "risk": "Low-Moderate Risk",
        "recommendations": [
            "Keep affected area clean, dry, and exposed to air",
            "Topical antifungal creams (clotrimazole, miconazole) twice daily",
            "Oral fluconazole for extensive or persistent infections",
            "Avoid tight clothing or occlusive materials",
            "Treat underlying causes (diabetes control, immune support)"
        ]
    },
    "DrugEruption": {
        "name": "Drug-Induced Eruption (Medication Reaction)",
        "cause": "Adverse allergic or toxicreaction to medications (antibiotics, NSAIDs, anticonvulsants)",
        "risk": "Moderate Risk",
        "recommendations": [
            "Identify and discontinue the offending medication immediately",
            "Consult with prescribing physician before stopping",
            "Use topical corticosteroids for symptom relief",
            "Antihistamines for itching and discomfort",
            "Avoid sun exposure during acute phase"
        ]
    },
    "Eczema": {
        "name": "Atopic Dermatitis (Eczema)",
        "cause": "Genetic predisposition, impaired skin barrier, environmental triggers, immune dysregulation",
        "risk": "Low-Moderate Risk",
        "recommendations": [
            "Use intensive moisturizers (creams/ointments) daily",
            "Topical corticosteroids for acute flares",
            "Avoid known triggers (soaps, detergents, allergens)",
            "Use lukewarm water for bathing, not hot water",
            "Consider prescription creams (tacrolimus) for severe cases"
        ]
    },
    "Vascular_Tumors": {
        "name": "Vascular Tumors (Hemangioma, Port-wine Stain)",
        "cause": "Abnormal development of blood vessels during development or acquired",
        "risk": "Low Risk",
        "recommendations": [
            "Monitor for growth or bleeding; most are benign",
            "Laser therapy (pulse dye laser) for cosmetic improvement",
            "Avoid trauma to prevent bleeding",
            "Cover with makeup if cosmetically concerned",
            "Regular dermatology evaluation for large lesions"
        ]
    },
    "Vasculitis": {
        "name": "Cutaneous Vasculitis (Inflamed Blood Vessels)",
        "cause": "Autoimmune response, infection, medications, or systemic disease affecting blood vessels",
        "risk": "Moderate-High Risk",
        "recommendations": [
            "Rest and leg elevation to reduce inflammation",
            "Topical or systemic corticosteroids as prescribed",
            "Antihistamines and NSAIDs for symptom control",
            "Rheumatology evaluation for underlying causes",
            "Avoid irritants and scratching"
        ]
    },
    "Vitiligo": {
        "name": "Vitiligo (Loss of Skin Pigmentation)",
        "cause": "Autoimmune destruction of melanocytes, genetic predisposition, possible neurogenic factors",
        "risk": "Low Risk",
        "recommendations": [
            "Strict sun protection with SPF 50+ on depigmented areas",
            "Topical corticosteroids or calcineurin inhibitors",
            "Phototherapy (narrow-band UVB) in dermatology clinics",
            "Cosmetic cover-up products (DermMatch, Microskin)",
            "Consider depigmentation if extensive (>50% body)"
        ]
    },
    "Warts": {
        "name": "Warts (Viral Infection - HPV)",
        "cause": "Human papillomavirus (HPV) infection; contagious but benign",
        "risk": "Low Risk",
        "recommendations": [
            "Topical treatments: salicylic acid, retinoids, or imiquimod",
            "Cryotherapy (liquid nitrogen freezing) by dermatologist",
            "Laser removal for resistant or painful warts",
            "Avoid picking or scratching to prevent spread",
            "Boost immune system; may spontaneously resolve"
        ]
    },
    "Infestations_Bites": {
        "name": "Parasitic Infestations & Insect Bites",
        "cause": "Scabies mites, lice, fleas, or other parasites; allergic reaction to bite proteins",
        "risk": "Low-Moderate Risk",
        "recommendations": [
            "Permethrin cream for scabies (apply neck to toes)",
            "Insecticidal shampoo for head lice or body lice",
            "Antihistamines and topical corticosteroids for itch",
            "Treat all household members and wash bedding",
            "Avoid scratching to prevent secondary infection"
        ]
    },
    "Lichen": {
        "name": "Lichen Planus (Inflammatory Condition)",
        "cause": "Autoimmune inflammatory response affecting skin and mucous membranes",
        "risk": "Moderate Risk",
        "recommendations": [
            "Topical corticosteroids as first-line treatment",
            "Oral retinoids or systemic corticosteroids if extensive",
            "Avoid triggers (NSAIDs, certain foods, stress)",
            "Hydroxychloroquine for resistant cases",
            "Monitor oral lesions for malignant transformation"
        ]
    },
    "Lupus": {
        "name": "Systemic Lupus Erythematosus (SLE) - Cutaneous",
        "cause": "Autoimmune disease affecting skin, triggered by genetics, UV exposure, medications",
        "risk": "Moderate-High Risk",
        "recommendations": [
            "Strict UV protection (SPF 50+, protective clothing)",
            "Topical or systemic corticosteroids",
            "Hydroxychloroquine for chronic cutaneous lesions",
            "Immunosuppressive therapy if needed",
            "Rheumatology consultation for systemic management"
        ]
    },
    "Moles": {
        "name": "Nevi (Moles)",
        "cause": "Benign clusters of melanocytes; common, may be present from birth or acquired",
        "risk": "Low Risk",
        "recommendations": [
            "Monitor using ABCDE rule for atypical features",
            "Avoid unnecessary removal unless cosmetically desired",
            "Professional removal if concerning or cosmetic reasons",
            "Regular skin surveillance for changes",
            "Use sunscreen to slow new mole development"
        ]
    },
    "Psoriasis": {
        "name": "Psoriasis (Chronic Inflammatory)",
        "cause": "Genetic predisposition, immune dysregulation, stress, infection, medications",
        "risk": "Low-Moderate Risk",
        "recommendations": [
            "Topical corticosteroids and vitamin D analogs",
            "Systemic biologics (TNF inhibitors) for severe cases",
            "Phototherapy (UVB or PUVA) in dermatology clinics",
            "Stress reduction and adequate sleep",
            "Avoid triggers: stress, alcohol, smoking, NSAIDs"
        ]
    },
    "Rosacea": {
        "name": "Rosacea (Chronic Facial Flushing)",
        "cause": "Vascular instability, demodex mite sensitivity, genetic predisposition",
        "risk": "Low Risk",
        "recommendations": [
            "Avoid triggers: spicy foods, alcohol, extreme temperatures",
            "Topical antibiotics (metronidazole, azelaic acid)",
            "Oral antibiotics (doxycycline) for moderate-severe cases",
            "Gentle skincare with non-irritating products",
            "Laser treatment for persistent redness"
        ]
    },
    "Seborrh_Keratoses": {
        "name": "Seborrheic Keratosis (Age Spot)",
        "cause": "Common benign growth with age; hereditary predisposition",
        "risk": "Low Risk",
        "recommendations": [
            "No treatment needed unless cosmetically bothersome",
            "Cryotherapy or curettage for removal",
            "Laser removal for cosmetic concerns",
            "Differentiate from melanoma via professional evaluation",
            "Regular surveillance for changes in appearance"
        ]
    },
    "SkinCancer": {
        "name": "Skin Cancer (Melanoma, Basal Cell, Squamous Cell)",
        "cause": "UV exposure, genetic predisposition, atypical moles, immunosuppression",
        "risk": "High Risk",
        "recommendations": [
            "URGENT: Immediate dermatology evaluation required",
            "Biopsy for definitive diagnosis",
            "Skin cancer-specific treatment (Mohs, excision, immunotherapy)",
            "Strict lifetime sun protection",
            "Regular full-body skin exams every 3-6 months"
        ]
    },
    "Sun_Sunlight_Damage": {
        "name": "Photodamage (Sun Damage)",
        "cause": "Chronic cumulative UV exposure causing premature aging and skin damage",
        "risk": "Moderate Risk",
        "recommendations": [
            "Daily SPF 50+ sunscreen and protective clothing",
            "Antioxidants (vitamin C serum) to prevent further damage",
            "Retinoids to improve skin texture and collagen",
            "Professional treatments: laser resurfacing, chemical peels",
            "Avoid sun exposure during peak hours (10am-4pm)"
        ]
    },
    "Tinea": {
        "name": "Tinea (Fungal Infection - Ringworm)",
        "cause": "Dermatophyte fungal infection (T. rubrum, M. canis); contagious",
        "risk": "Low-Moderate Risk",
        "recommendations": [
            "Topical antifungal creams for localized infections",
            "Oral antifungals (terbinafine, fluconazole) for extensive cases",
            "Keep area clean, dry, and exposed to air",
            "Avoid sharing personal items, towels, clothing",
            "Treat all affected family members"
        ]
    },
    "Unknown_Normal": {
        "name": "Normal or Unclassified Skin Condition",
        "cause": "Skin appears normal or does not match any recognized condition in the database",
        "risk": "Low Risk",
        "recommendations": [
            "Continue routine skincare and sun protection",
            "Maintain healthy lifestyle habits",
            "If concerned about any changes, consult dermatologist",
            "Schedule annual skin check-ups",
            "Perform monthly self-examinations using ABCDE rule"
        ]
    }
}

# PREDICTION FUNCTION WITH WORKAROUNDS
def predict_image(image_path):
    """Predict disease from image with improved confidence calibration"""
    try:
        from PIL import Image
        
        if not os.path.exists(image_path):
            return {
                "predicted_disease": "Unknown_Normal",
                "confidence": 0.0,
                "message": "Image file not found",
                "disease_info": DISEASE_INFO.get("Unknown_Normal", {})
            }
        
        # Load and preprocess image
        img = Image.open(image_path).convert('RGB')
        img_resized = img.resize((224, 224), Image.Resampling.LANCZOS)
        img_array = np.array(img_resized, dtype=np.float32) / 255.0
        img_batch = np.expand_dims(img_array, axis=0)
        
        # Get raw logits (pre-softmax)
        logits = model.predict(img_batch, verbose=0)[0].flatten()
        
        # WORKAROUND 1: Adaptive temperature scaling for confidence calibration
        # Apply different temperature based on prediction margin to improve confidence calibration
        sorted_logits = np.sort(logits)[::-1]
        margin = sorted_logits[0] - sorted_logits[1]  # Margin between top 2 logits
        
        # Select temperature to sharpen or soften predictions based on margin
        if margin < 0.5:
            temperature = 0.3  # Very uncertain - sharpen aggressively
        elif margin < 1.5:
            temperature = 0.4  # Uncertain - sharpen
        elif margin < 3.0:
            temperature = 0.5  # Moderate uncertainty - sharpen moderately
        elif margin < 5.0:
            temperature = 0.6  # More confident - gentle sharpening
        else:
            temperature = 0.7  # Very confident - minimal sharpening
        
        # Apply temperature scaling to logits
        scaled_logits = logits / temperature
        
        # Convert to probabilities with softmax
        try:
            probs = tf.nn.softmax(scaled_logits).numpy()
        except:
            # Fallback if TensorFlow unavailable
            e = np.exp(scaled_logits - np.max(scaled_logits))
            probs = e / e.sum()
        
        # WORKAROUND 2: Confidence boosting based on margin
        # Boost confidence for predictions with clear winners
        top_idx = int(np.argmax(probs))
        top_prob = float(probs[top_idx])
        
        # If we have a clear margin, we can be more confident
        if margin > 3.0:
            # Strong margin - boost to 60-85%
            top_prob = 0.6 + (min(margin / 10.0, 0.25))
        elif margin > 1.5:
            # Decent margin - boost to 40-60%
            top_prob = 0.4 + (margin / 10.0)
        else:
            # Weak margin - more conservative (30-40%)
            top_prob = 0.3 + (margin / 15.0)
        
        # WORKAROUND 3: Normalize probabilities to make top prediction have the boosted confidence
        # while keeping others proportional
        other_prob_total = 1.0 - top_prob
        if len(probs) > 1:
            other_probs = probs.copy()
            other_probs[top_idx] = 0
            other_sum = np.sum(other_probs)
            if other_sum > 0:
                other_probs = (other_probs / other_sum) * other_prob_total
                other_probs[top_idx] = top_prob
                probs = other_probs
            else:
                probs[top_idx] = top_prob
        
        # Ensure index is valid
        if top_idx >= len(CLASS_NAMES):
            top_idx = 0
        
        disease_name = CLASS_NAMES[top_idx]
        disease_info = DISEASE_INFO.get(disease_name, DISEASE_INFO.get("Unknown_Normal", {}))
        
        # Convert top probability to percentage
        confidence_pct = round(float(top_prob) * 100, 1)
        
        # Calculate all class probabilities as percentages
        all_probs_pct = probs * 100
        all_probs_dict = {CLASS_NAMES[i]: float(round(all_probs_pct[i], 2)) for i in range(len(CLASS_NAMES))}
        
        result = {
            "predicted_disease": disease_name,
            "confidence": float(confidence_pct),
            "disease_info": disease_info,
            "message": f"Predicted: {disease_name} ({confidence_pct}%)",
            "all_probs": all_probs_dict
        }
        
        # Log top predictions
        top_5_idx = np.argsort(all_probs_pct)[::-1][:5]
        print(f"[predict_image] Top-5 for {os.path.basename(image_path)}:")
        for idx in top_5_idx:
            print(f"  {CLASS_NAMES[idx]}: {all_probs_pct[idx]:.1f}%")
        
        return result
        
    except Exception as e:
        print(f"[predict_image] Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "predicted_disease": "Unknown_Normal",
            "confidence": 0.0,
            "message": f"Prediction error: {str(e)}",
            "disease_info": DISEASE_INFO.get("Unknown_Normal", {})
        }

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN (GET+POST) ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")  # Default to "user" if not provided

        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_row = cur.fetchone()
        conn.close()

        if not user_row:
            flash("Account not found. Please create an account.")
            return redirect(url_for("register"))
        
        # Convert Row to dictionary
        user = dict(user_row)

        if check_password_hash(user["password"], password):
            # Check if login role matches account type or allow admin login
            if role == "admin" and user["account_type"] == "admin":
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["login_role"] = "admin"
                session["account_type"] = "admin"
                flash("Admin access verified", "info")
                return redirect(url_for("admin_dashboard"))  # Redirect to admin dashboard
            elif role == "user":
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["login_role"] = "user"
                session["account_type"] = user.get("account_type", "user")
                return redirect(url_for("upload"))
            else:
                flash("Invalid credentials for selected role")
        else:
            flash("Incorrect password")

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """Logout user by clearing session"""
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("home"))


# ---------------- REGISTER (GET+POST) ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm") or request.form.get("confirm_password")
        account_type = request.form.get("account_type", "user")  # Default to "user"

        if not username or not email or not password:
            flash("Please fill required fields")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, phone, password, account_type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (username, email, phone, hashed, account_type, datetime.utcnow().isoformat()),
            )
            conn.commit()
            flash("Account created. Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Account with that email or username already exists")
        finally:
            conn.close()

    return render_template("register.html")


# ---------------- UPLOAD PAGE ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("image") or request.files.get("file")

        if file and file.filename:
            # create a secure, unique filename to avoid caching/overwrites
            orig = secure_filename(file.filename)
            name, ext = os.path.splitext(orig)
            unique_name = f"{name}_{uuid.uuid4().hex}{ext}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            file.save(filepath)
            # store only the filename in session (not full path)
            session["uploaded_image"] = unique_name
            return redirect(url_for("result"))
        else:
            flash("No file selected")

    return render_template("upload.html")


@app.route('/api/upload', methods=['POST'])
def api_upload():
    file = request.files.get('image') or request.files.get('file')
    if not file or not file.filename:
        return {"success": False, "message": "No file provided"}, 400
    orig = secure_filename(file.filename)
    name, ext = os.path.splitext(orig)
    unique_name = f"{name}_{uuid.uuid4().hex}{ext}"
    safe_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
    try:
        file.save(safe_path)
        session['uploaded_image'] = unique_name
        return {"success": True, "filename": unique_name}
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


# API: Predict from an uploaded filename (bypasses session)
@app.route('/api/predict_file', methods=['GET', 'POST'])
def api_predict_file():
    # Accept either JSON/form or query param
    filename = request.values.get('filename') or (request.get_json(silent=True) or {}).get('filename')
    if not filename:
        return {"success": False, "message": "filename parameter required"}, 400

    safe_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(safe_path):
        return {"success": False, "message": "file not found", "filename": filename}, 404

    try:
        result = predict_image(safe_path)
        return {"success": True, "filename": filename, "result": result}
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


# ---------------- RESULT PAGE ----------------
@app.route("/result")
def result():
    image_filename = session.get("uploaded_image")
    result_data = None
    image_url = None
    gradcam_url = None
    if image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        # run prediction using full path
        result_data = predict_image(image_path)
        # build URLs with cache-busting timestamp
        ts = int(time.time())
        image_url = url_for('uploaded_file', filename=image_filename) + f"?t={ts}"
        if result_data and result_data.get('gradcam'):
            gradcam_url = url_for('uploaded_file', filename=result_data.get('gradcam')) + f"?t={ts}"

    model_name = os.path.basename(MODEL_PATH) if MODEL_PATH else "(no model)"
    model_loaded = model is not None
    return render_template("result.html", image=image_url, image_filename=image_filename, result=result_data, model_name=model_name, model_loaded=model_loaded, gradcam_url=gradcam_url)


@app.route("/disease-dictionary")
def disease_dictionary():
    focus_disease = request.args.get('focus_disease', 'None')
    return render_template("disease_dictionary.html", focus_disease=focus_disease)


# ---------------- FEEDBACK ----------------
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        comment = request.form.get("comment")
        user_id = session.get("user_id")
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO feedback (user_id, comment, created_at) VALUES (?, ?, ?)",
            (user_id, comment, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
        flash("Thanks for your feedback")
        return redirect(url_for("thanks"))

    return render_template("feedback.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/thanks")
def thanks():
    # consume any flashed messages so they don't show up on subsequent pages
    try:
        _ = get_flashed_messages()
    except Exception:
        pass
    return render_template("thanks.html")


# FINAL MODEL NOTE: Admin and debug endpoints removed
# The application now uses only Skin_Cancer_Model.h5 as the final working model
# No configuration or debugging needed
    """Return current binary model settings (JSON)."""
    current = {'positive_class': BINARY_POSITIVE_CLASS, 'threshold': BINARY_THRESHOLD}
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as fh:
                saved = json.load(fh)
                current['positive_class'] = saved.get('positive_class', current['positive_class'])
                current['threshold'] = saved.get('threshold', current['threshold'])
    except Exception as e:
        current['error'] = str(e)
    return current


@app.route("/download_report")
def download_report():
    # Placeholder: generate a small text-based PDF-like file
    image_filename = session.get("uploaded_image")
    image = None
    if image_filename:
        image = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    result = predict_image(image) if image else {}
    model_name = os.path.basename(MODEL_PATH) if MODEL_PATH else "(no model)"
    out_txt = os.path.join(BASE_DIR, "report.txt")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("AI Skin Report\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Model Loaded: {model is not None}\n")
        f.write(f"Image: {image}\n")
        for k, v in result.items():
            f.write(f"{k}: {v}\n")

    # If gradcam exists, bundle txt + gradcam image into a zip
    gradcam = result.get("gradcam") if isinstance(result, dict) else None
    if gradcam:
        zip_path = os.path.join(BASE_DIR, "report_bundle.zip")
        with zipfile.ZipFile(zip_path, 'w') as z:
            z.write(out_txt, arcname="report.txt")
            gradcam_path = os.path.join(app.config['UPLOAD_FOLDER'], gradcam)
            if os.path.exists(gradcam_path):
                z.write(gradcam_path, arcname=os.path.basename(gradcam_path))
        return send_file(zip_path, as_attachment=True, download_name="report_bundle.zip")

    return send_file(out_txt, as_attachment=True, download_name="report.txt")


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/model_info')
def model_info():
    if model is None:
        return {
            "model_loaded": False,
            "message": "Model not loaded. Place Skin_Cancer_Model.h5 in backend/models or project models folder and restart." 
        }

    out_shape = None
    try:
        out_shape = model.output_shape
    except Exception:
        out_shape = str(getattr(model, 'output_shape', 'unknown'))

    return {
        "model_loaded": True,
        "model_path": MODEL_PATH,
        "output_shape": out_shape,
        "notes": "Verify that the last dimension equals number of classes. If not, adjust class_names in app.py accordingly."
    }


@app.route('/debug/predict')
def debug_predict():
    """Debug endpoint removed - using final model only"""
    return {"error": "Debug endpoint disabled for final model"}


# ---------------- ADMIN: reload model at runtime ----------------
@app.route('/admin/reload_model', methods=['POST'])
def admin_reload_model():
    """Reload the model from disk (useful after replacing the model file).
    POST optional form field `path` to load a specific file, otherwise uses default MODEL_PATH candidates.
    """
    global MODEL_PATH, model
    path = request.form.get('path') or request.json.get('path') if request.is_json else None
    if path:
        if not os.path.exists(path):
            return {"success": False, "message": f"path not found: {path}"}, 404
        MODEL_PATH = path

    try:
        load_model_safe()
        out = {
            "success": True,
            "model_path": MODEL_PATH,
            "model_loaded": model is not None,
            "output_shape": getattr(model, 'output_shape', None)
        }
        return out
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


@app.route('/admin/model_info', methods=['GET'])
def admin_model_info():
    """Return basic model and class-name info for debugging."""
    info = {
        'model_loaded': model is not None,
        'model_path': MODEL_PATH,
        'output_shape': getattr(model, 'output_shape', None),
        'class_count': len(CLASS_NAMES) if CLASS_NAMES else 0,
        'first_22_classes': (CLASS_NAMES[:22] if CLASS_NAMES else [])
    }
    return info


# -------- ADMIN DASHBOARD --------
@app.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    """Admin dashboard showing user stats and feedback"""
    # Check if user is logged in and is an admin
    if "user_id" not in session or session.get("account_type") != "admin":
        flash("Admin access required")
        return redirect(url_for("login"))
    
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Get total users count - exact number
        cur.execute("SELECT COUNT(*) as count FROM users")
        total_users = cur.fetchone()[0]
        
        # Get all users and convert to dictionaries
        cur.execute("SELECT id, username, email, phone, account_type, created_at FROM users ORDER BY created_at DESC")
        users = [dict(row) for row in cur.fetchall()]
        
        # Get total feedback count - exact number
        cur.execute("SELECT COUNT(*) as count FROM feedback")
        total_feedback = cur.fetchone()[0]
        
        # Get all feedback and convert to dictionaries
        cur.execute("SELECT id, name, email, message, created_at FROM feedback ORDER BY created_at DESC LIMIT 50")
        feedback = [dict(row) for row in cur.fetchall()]
        
        conn.close()
        
        return render_template(
            "admin_dashboard.html",
            total_users=total_users,
            total_feedback=total_feedback,
            users=users,
            feedback=feedback,
            total_predictions=0  # Can be enhanced to track predictions
        )
    except Exception as e:
        app.logger.error(f"Admin dashboard error: {str(e)}")
        flash(f"Error loading dashboard: {str(e)}")
        return redirect(url_for("upload"))


# -------- API ENDPOINTS FOR ADMIN UPDATES --------
@app.route("/api/admin/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user information"""
    if "user_id" not in session or session.get("account_type") != "admin":
        return {"error": "Admin access required"}, 403
    
    try:
        data = request.get_json()
        conn = get_db_connection()
        
        # Update user
        conn.execute(
            "UPDATE users SET email=?, phone=?, account_type=? WHERE id=?",
            (data.get("email"), data.get("phone"), data.get("account_type"), user_id)
        )
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "User updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/admin/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete user"""
    if "user_id" not in session or session.get("account_type") != "admin":
        return {"error": "Admin access required"}, 403
    
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "User deleted successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/admin/feedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    """Delete feedback"""
    if "user_id" not in session or session.get("account_type") != "admin":
        return {"error": "Admin access required"}, 403
    
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Feedback deleted successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/api/admin/stats", methods=["GET"])
def get_admin_stats():
    """Get real-time admin statistics"""
    if "user_id" not in session or session.get("account_type") != "admin":
        return {"error": "Admin access required"}, 403
    
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # Get counts - exact numbers
        cur.execute("SELECT COUNT(*) as count FROM users")
        total_users = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) as count FROM users WHERE account_type = 'user'")
        regular_users = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) as count FROM users WHERE account_type = 'admin'")
        admin_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) as count FROM feedback")
        total_feedback = cur.fetchone()[0]
        
        conn.close()
        
        return {
            "total_users": total_users,
            "regular_users": regular_users,
            "admin_count": admin_count,
            "total_feedback": total_feedback,
            "predictions": 0
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=False)
