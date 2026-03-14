# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.7+
- Your trained `Skin_Cancer_Model.h5` file

### Step 1: Setup (2 min)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# OR Windows CMD
venv\Scripts\activate

# OR Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Place Your Model (1 min)
```
Copy your Skin_Cancer_Model.h5 to:
backend/models/Skin_Cancer_Model.h5
```

### Step 3: Run the App (1 min)
```bash
python app.py
```

You'll see:
```
✓ Model loaded from backend/models/Skin_Cancer_Model.h5
* Running on http://localhost:5000
```

### Step 4: Test It (1 min)
1. Open browser: `http://localhost:5000`
2. Click "Start Skin Check"
3. Register new account
4. Login
5. Upload a test image
6. View AI prediction results!

---

## 📁 File Structure

```
backend/
├── app.py                      ← Main Flask app with model integration
├── requirements.txt            ← Dependencies
├── models/
│   └── Skin_Cancer_Model.h5    ← Your trained model (PLACE HERE)
├── uploads/                    ← User uploaded images (auto-created)
├── static/
│   └── style.css               ← All page styling
├── templates/
│   ├── index.html              ← Landing page
│   ├── login.html              ← Login
│   ├── register.html           ← Sign up
│   ├── upload.html             ← Image upload
│   ├── result.html             ← AI prediction (MODEL RESULTS)
│   ├── faq.html                ← FAQ
│   ├── help.html               ← Help
│   ├── feedback.html           ← Feedback form
│   └── thanks.html             ← Thank you
├── app.db                      ← SQLite database (auto-created)
└── venv/                       ← Virtual environment
```

---

## 🎯 User Journey

```
Home Page
    ↓
"Start Skin Check" button
    ↓
Login Page
    ↓
Register (if new user)
    ↓
Upload Page
    ↓
Select image → Upload
    ↓
Result Page (AI PREDICTION)
    ├─ Disease name
    ├─ Confidence %
    ├─ Risk level
    ├─ Cause explanation
    ├─ Doctor recommendations
    └─ Download report button
```

---

## ✨ Key Features Implemented

✅ User authentication (login/register)
✅ Image upload (PNG/JPG)
✅ **AI Model Integration** (Skin_Cancer_Model.h5)
✅ Disease prediction with confidence
✅ 5 disease classification
✅ Personalized recommendations
✅ Professional UI (all pages styled)
✅ Report generation
✅ SQLite database
✅ Session management

---

## 🔧 Configuration

### Model Classes
The model predicts 5 classes:
1. Melanoma (High Risk)
2. Benign Lesions (Low Risk)
3. Seborrheic Keratosis (Low Risk)
4. Nevus/Moles (Low Risk)
5. Basal Cell Carcinoma (Moderate Risk)

**If your model has different classes:** Edit line ~180 in `app.py`:
```python
class_names = ["your_class_1", "your_class_2", ...]
```

---

## 📊 What Happens on Result Page

1. **Image Display** - Shows uploaded skin image
2. **Disease Name** - Top prediction from model
3. **Risk Level** - Color-coded (High/Moderate/Low)
4. **Confidence %** - Shows accuracy with progress bar
5. **Cause** - Explanation of disease
6. **Recommendations** - 4 personalized doctor recommendations
7. **Download** - Generate and download report

---

## 🛠️ Troubleshooting

### "Model not loading"
```bash
# Check if file exists
dir backend\models\
# Should show: Skin_Cancer_Model.h5

# Test model directly
python
>>> from tensorflow import keras
>>> m = keras.models.load_model('backend/models/Skin_Cancer_Model.h5')
>>> m.summary()
```

### "Import error for tensorflow"
```bash
pip install --upgrade tensorflow
```

### "Database locked"
```bash
# Delete and recreate
del backend\app.db
# Run app again - DB recreates automatically
```

### "Port 5000 in use"
```bash
# Change port in app.py last line:
app.run(debug=True, port=5001)  # Use 5001 instead
```

---

## 📝 Testing Checklist

- [ ] Model loads without errors (check console)
- [ ] Can create account and login
- [ ] Can upload PNG/JPG image
- [ ] Result page shows prediction
- [ ] Confidence % displays correctly
- [ ] Recommendations appear
- [ ] All links work (navbar, buttons)
- [ ] Can download report
- [ ] Can logout and login again

---

## 🎓 Understanding the Model Integration

```python
# In app.py, the prediction flow:

1. User uploads image
   ↓
2. Image saved to uploads/ folder
   ↓
3. Image path stored in session
   ↓
4. User visits /result route
   ↓
5. predict_image(filepath) is called:
   a. Load model (cached from startup)
   b. Read and resize image to 224×224
   c. Normalize pixel values (0-1)
   d. Run model.predict()
   e. Get highest probability class
   f. Map class to disease info
   g. Return results object
   ↓
6. result.html displays:
   - Image
   - Disease name
   - Confidence
   - Risk level
   - Cause
   - Recommendations
```

---

## 🚀 Production Tips

Before deploying:
1. Change `app.secret_key` in app.py
2. Set `debug=False` in app.py
3. Use environment variables for secrets
4. Add HTTPS/SSL certificate
5. Use proper WSGI server (gunicorn, waitress)
6. Implement API rate limiting

---

## 📞 Support

If model doesn't predict:
1. Check MODEL_CONFIG.md for class mapping
2. Verify model input: 224×224 RGB images
3. Check console for error messages
4. Ensure requirements.txt packages are installed

---

**Your AI Skin Disease Detection system is complete and ready to use!** 🎉
