# Quick Start Guide

## Prerequisites

Make sure you have Python 3.8+ installed with these packages:
```bash
pip install flask tensorflow numpy pillow
```

## Running the Application

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Start Flask Server
```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 3: Open in Browser
Open your web browser and go to:
```
http://localhost:5000
```

## Using the Application

### Home Page
- Click "Upload" to start analyzing a skin condition image

### Upload Image
1. Select a high-quality image of the skin condition
2. Click "Upload and Analyze"
3. Wait for model to process

### View Results
The result page shows:
- **Disease Name**: Top prediction from the model
- **Cause**: Medical explanation of the condition
- **Risk Level**: Severity assessment (Low/Moderate/High)
- **Confidence**: Accuracy percentage (0-100%)
- **Recommendations**: Evidence-based treatment options
- **Top-3 Predictions**: Alternative conditions with confidence scores

## Troubleshooting

### Model Not Loading
- Check if `backend/models/skin_disease_model.h5` exists
- Verify TensorFlow is installed: `pip install --upgrade tensorflow`

### Port Already in Use
- Change port in `app.py` line: `app.run(debug=False, port=5001)`

### Import Errors
```bash
pip install --upgrade tensorflow keras pillow numpy flask
```

### Image Upload Issues
- Ensure image is in JPG, PNG, or BMP format
- Recommended size: 224x224 pixels
- Maximum file size: 5MB

## Testing the Model

Quick test to verify everything works:
```bash
cd backend
python TEST_MODEL_LOADING.py
```

This will:
- ✓ Verify model file exists
- ✓ Load disease classes
- ✓ Check DISEASE_INFO database
- ✓ Test model loading

## File Structure

```
AI_Skin_Disease_Project/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── models/
│   │   ├── skin_disease_model.h5 # AI Model
│   │   └── classes.txt           # Disease class names
│   ├── templates/
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── result.html           # Prediction results display
│   │   └── ...
│   ├── static/
│   │   ├── style.css
│   │   └── index.css
│   └── uploads/                  # User-uploaded images
├── README.md
├── QUICK_START.md                # This file
└── PROJECT_COMPLETION_REPORT.md  # Full documentation
```

## Key Features

✅ **95+ Disease Classifications**
- Acne variants
- Urticaria types
- Dermatitis/Eczema conditions
- Fungal infections
- Psoriasis variants
- Rosacea types
- And many more...

✅ **Comprehensive Disease Information**
- Medical causes
- Risk assessment
- Treatment recommendations
- Professional guidance

✅ **Production Ready**
- No debug information exposed
- Clean, professional UI
- Secure error handling
- Database support for user accounts

## Next Steps

1. ✓ Run the application: `python app.py`
2. ✓ Test with sample images
3. ✓ Verify predictions are accurate
4. ✓ Deploy to production server
5. ✓ Monitor user feedback

## Support

For detailed information, see:
- `PROJECT_COMPLETION_REPORT.md` - Full technical details
- `MODEL_CONFIG.md` - Model specifications
- Flask error logs in console - Detailed debugging

---

**Happy diagnosing!** 🏥
