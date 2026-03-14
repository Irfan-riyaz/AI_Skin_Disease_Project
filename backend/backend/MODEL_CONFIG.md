# Model Class Mapping Configuration

## Current Setup

Your model should output 5 classes in this order:

```python
class_names = ["melanoma", "benign", "keratosis", "nevus", "carcinoma"]
```

## Detailed Mapping

### Class 0: Melanoma
- **Display Name**: Melanoma (Skin Cancer)
- **Risk Level**: High Risk ⚠️
- **Cause**: Excessive sun exposure, UV radiation, genetic predisposition, irregular moles
- **Recommendations**:
  1. Consult a dermatologist immediately
  2. Consider skin biopsy for confirmation
  3. Seek specialist oncology consultation
  4. Avoid further sun exposure

### Class 1: Benign
- **Display Name**: Benign Skin Lesion
- **Risk Level**: Low Risk ✓
- **Cause**: Common benign growth, age spots, non-cancerous moles, skin tags
- **Recommendations**:
  1. Monitor for any changes
  2. Annual dermatology checkup recommended
  3. Use sunscreen for prevention
  4. No immediate intervention needed

### Class 2: Keratosis
- **Display Name**: Seborrheic Keratosis
- **Risk Level**: Low Risk ✓
- **Cause**: Common harmless skin growth, age-related, genetic factors
- **Recommendations**:
  1. Monitor for cosmetic concerns
  2. Can be removed if irritated
  3. Regular skin screening advised
  4. Non-malignant growth

### Class 3: Nevus
- **Display Name**: Nevus (Mole)
- **Risk Level**: Low Risk ✓
- **Cause**: Clusters of pigmented cells, common in all skin types
- **Recommendations**:
  1. Regular monitoring recommended
  2. ABCDE rule for mole assessment
  3. Annual dermatology visit
  4. Avoid unnecessary sun exposure

### Class 4: Carcinoma
- **Display Name**: Basal Cell Carcinoma
- **Risk Level**: Moderate Risk ⚠️
- **Cause**: Cumulative sun exposure, fair skin, age, chronic sun damage
- **Recommendations**:
  1. Consult dermatologist for treatment options
  2. Possible surgical removal
  3. Mohs micrographic surgery may be recommended
  4. Long-term follow-up required

## How to Verify Your Model Output

Run this test to ensure your model outputs in the correct order:

```python
import numpy as np
from tensorflow import keras

# Load your model
model = keras.models.load_model('backend/models/Skin_Cancer_Model.h5')

# Print model info
print("Model name:", model.name)
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)
print("Total parameters:", model.count_params())

# Get class names
class_names = ["melanoma", "benign", "keratosis", "nevus", "carcinoma"]
print(f"Classes ({len(class_names)}): {class_names}")

# Expected output: (None, 5) for 5 classes
```

## If Your Model Has Different Classes

If your trained model uses different class names or order, update this in `app.py`:

```python
# Line ~180 in app.py, find this section:
class_names = ["melanoma", "benign", "keratosis", "nevus", "carcinoma"]

# Replace with your actual class names in the order your model outputs them
class_names = ["class0_name", "class1_name", "class2_name", ...]
```

## If Your Model Has Different Number of Classes

If your model outputs more or fewer than 5 classes:

1. Update `class_names` list with all classes
2. The app will automatically handle any number of classes
3. Unmapped classes will default to "Unclassified Skin Condition"

## Expected Model Output Example

When you predict an image, the model should return:

```
Input: Image (224, 224, 3) normalized to [0, 1]
Process: Forward pass through network
Output: Array of 5 probabilities, e.g., [0.02, 0.85, 0.08, 0.03, 0.02]

In this example:
- Class 0 (melanoma): 2%
- Class 1 (benign): 85% ← Highest confidence (predicted class)
- Class 2 (keratosis): 8%
- Class 3 (nevus): 3%
- Class 4 (carcinoma): 2%

Result displayed:
- Disease: "Benign Skin Lesion"
- Accuracy: "85.0%"
- Risk: "Low Risk"
```

## Confidence Thresholds (Optional)

You can add confidence thresholds by modifying `predict_image()` in app.py:

```python
# After line ~220, add:
if confidence < 60:
    return {
        "disease": "Low Confidence - Consult Dermatologist",
        "cause": "Model confidence below 60%",
        "accuracy": f"{confidence:.1f}%",
        "risk": "Requires Professional Review",
        "recommendations": [
            "Please provide a clearer image",
            "Ensure proper lighting",
            "Consult a dermatologist for accurate diagnosis",
            "Multiple images may improve accuracy"
        ]
    }
```

## Testing with Sample Images

Create `test_model.py` in the backend folder:

```python
import os
import numpy as np
from PIL import Image
from tensorflow import keras

# Load model
MODEL_PATH = "models/Skin_Cancer_Model.h5"
model = keras.models.load_model(MODEL_PATH)

# Load and preprocess image
image_path = "uploads/test_image.jpg"
img = Image.open(image_path).convert('RGB')
img = img.resize((224, 224))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
predictions = model.predict(img_array)
class_idx = np.argmax(predictions[0])
confidence = predictions[0][class_idx] * 100

# Display
class_names = ["melanoma", "benign", "keratosis", "nevus", "carcinoma"]
print(f"Predicted Class: {class_names[class_idx]}")
print(f"Confidence: {confidence:.2f}%")
print(f"All predictions: {predictions[0]}")
```

Run with:
```bash
cd backend
python test_model.py
```

---

**Your model is fully integrated and ready to make predictions!**
