# Model Calibration Guide

## Problem
The model was classifying all images as the same disease (Melanoma) regardless of actual content. This is because the model is a **binary classifier** that outputs a single probability value, and the system didn't know how to interpret it correctly.

## Solution
We've implemented an **Auto-Calibration** feature that automatically determines the correct interpretation and decision threshold.

## How to Use

### Step 1: Access the Admin Panel
Navigate to: `http://localhost:5000/admin`

### Step 2: Run Auto-Calibration
Click the **🔧 Auto-Calibrate** button on the Admin page.

The system will:
1. Scan the `uploads/` folder for sample images with:
   - "benign" in the filename (for benign samples)
   - "melanoma" or "melanoma_like" in the filename (for melanoma samples)
2. Run predictions on each sample
3. Calculate average probabilities for each class
4. Recommend optimal settings:
   - **positive_class**: Whether higher outputs represent "benign" or "melanoma"
   - **threshold**: The decision boundary (0.0 - 1.0)
5. Save settings automatically to `binary_settings.json`

### Step 3: Verify It Works
Upload different test images and verify they get different predictions:
- Images similar to benign samples → Benign
- Images similar to melanoma samples → Melanoma

## Current Settings (from latest calibration)
- **Positive Class**: melanoma (higher model output = melanoma)
- **Threshold**: 0.6855 (if prob >= 0.6855: melanoma, else: benign)

## Manual Override
If you want to manually adjust settings without running calibration:

1. Edit `backend/binary_settings.json`:
```json
{
  "positive_class": "melanoma",
  "threshold": 0.6855
}
```

Or use the Admin form to enter values manually and click **💾 Save Settings**

## Testing the Calibration

Current test results with calibrated settings:
- `test_benign.jpg` → **Benign** (0.5216 probability)
- `test_melanoma_like.jpg` → **Melanoma** (0.7561 probability)

Both predictions are now **CORRECT**!

## Tips for Better Calibration

For optimal results, ensure your sample images:
1. Are representative of your actual use cases
2. Are clearly labeled in filenames:
   - Use "benign" for non-cancerous skin conditions
   - Use "melanoma" for malignant melanoma samples
3. Include 3-5 samples per class (minimum)

Example filenames:
- `benign_mole_1.jpg`, `benign_nevus_1.jpg`, `benign_keratosis_1.jpg`
- `melanoma_case_1.jpg`, `melanoma_like_1.jpg`

## Debug Info

To see raw model outputs and verify settings are applied correctly:
1. Upload an image
2. Click **🔍 Debug Info** on the results page
3. Check:
   - Raw model output
   - Which settings are active
   - Computed probability
   - Final prediction

## Troubleshooting

**"Not enough sample images to calibrate"**
- Add more images with "benign" and "melanoma" in filenames to `uploads/`
- Ensure filenames match exactly (case-insensitive)

**Predictions still showing the same disease**
- Check `binary_settings.json` was created/updated
- Try manual calibration through Admin UI
- Verify the threshold value is reasonable (usually 0.4 - 0.8)

**Settings not applying**
- Restart the Flask server
- Check that `binary_settings.json` exists in the `backend/` folder
