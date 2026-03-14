# Pre-Launch Checklist

## ✅ Before Running the App

### 1. Environment Setup
- [ ] Python 3.7+ installed
- [ ] Virtual environment created (`venv/`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No import errors when running `python -c "import tensorflow"`

### 2. Model File
- [ ] `Skin_Cancer_Model.h5` exists in `backend/models/`
- [ ] Model file size > 1MB
- [ ] Model is readable (not corrupted)
- [ ] Model supports 5 output classes

### 3. Project Structure
- [ ] `backend/` folder exists
- [ ] `backend/templates/` has all 9 HTML files
- [ ] `backend/static/style.css` exists
- [ ] `backend/uploads/` folder exists (auto-created)

### 4. Configuration
- [ ] No hardcoded passwords in code
- [ ] `app.secret_key` is configured
- [ ] Database path is correct
- [ ] Upload folder path is correct

### 5. Dependencies Check
```bash
python -c "import flask; import tensorflow; import numpy; import PIL; print('✓ All dependencies OK')"
```

---

## 🚀 Launch Steps

### Step 1: Activate Environment
```bash
cd backend
.\venv\Scripts\Activate.ps1
# On Linux/Mac: source venv/bin/activate
```

### Step 2: Verify Model
```bash
python -c "
from tensorflow import keras
try:
    m = keras.models.load_model('models/Skin_Cancer_Model.h5')
    print('✓ Model loaded successfully')
    print(f'  Input shape: {m.input_shape}')
    print(f'  Output shape: {m.output_shape}')
except Exception as e:
    print(f'✗ Error: {e}')
"
```

### Step 3: Run Application
```bash
python app.py
```

### Step 4: Verify Output
```
✓ Model loaded from backend/models/Skin_Cancer_Model.h5
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### Step 5: Open Browser
Go to: `http://localhost:5000`

---

## 🧪 Testing Checklist

### Account Creation
- [ ] Navigate to Register
- [ ] Fill all fields (username, email, phone, password)
- [ ] Passwords match
- [ ] Click "Create Account"
- [ ] Redirected to Login page
- [ ] Can login with credentials

### Login Process
- [ ] Go to Login page
- [ ] Enter email and password
- [ ] Click "Login"
- [ ] Redirected to Upload page
- [ ] Session is active

### Image Upload
- [ ] Navigate to Upload page
- [ ] Select PNG or JPG image
- [ ] Click "Upload & Process"
- [ ] File is saved to `backend/uploads/`
- [ ] Redirected to Result page

### Model Prediction
- [ ] Result page loads
- [ ] Image is displayed
- [ ] Disease name appears
- [ ] Confidence % is shown (e.g., "92.5%")
- [ ] Confidence bar fills correctly
- [ ] Risk level displayed (color-coded)
- [ ] Cause text appears
- [ ] Recommendations list populated (4 items)

### Navigation
- [ ] Navbar appears on all pages
- [ ] All links work (Home, Login, FAQ, Help, Feedback)
- [ ] "Download Report" button works
- [ ] "Back to Home" button works

### Database
- [ ] `app.db` is created
- [ ] User data is stored
- [ ] Can login multiple times

---

## 🔍 Troubleshooting During Launch

### Issue: "Module not found: tensorflow"
```bash
# Solution:
pip install --upgrade tensorflow
```

### Issue: "Model file not found"
```bash
# Check file exists:
dir backend\models\
# Should show: Skin_Cancer_Model.h5

# If not found, copy it:
# Copy your .h5 file to backend/models/ folder
```

### Issue: "Port 5000 already in use"
```bash
# Change port in app.py (last line):
app.run(debug=True, port=5001)  # Use 5001
# Then visit: http://localhost:5001
```

### Issue: "Database locked" error
```bash
# Solution:
# Delete app.db and restart (it recreates automatically)
del backend\app.db
python app.py
```

### Issue: Image doesn't display on result page
```bash
# Check:
# 1. File exists in backend/uploads/
# 2. Image is valid PNG/JPG
# 3. No special characters in filename
```

### Issue: Model prediction slow
```bash
# Normal: First prediction ~2-3 seconds (model loads)
# Subsequent: <1 second (cached)
# If slower: Check CPU usage, consider GPU acceleration
```

---

## 📊 Model Output Verification

Create `test_model.py`:
```python
import numpy as np
from tensorflow import keras
from PIL import Image

# Load model
model = keras.models.load_model('models/Skin_Cancer_Model.h5')

# Load test image
img = Image.open('uploads/test_image.jpg').convert('RGB')
img = img.resize((224, 224))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
predictions = model.predict(img_array)
print(f"Predictions: {predictions[0]}")
print(f"Sum of probabilities: {np.sum(predictions[0])}")  # Should be ~1.0
print(f"Max confidence: {np.max(predictions[0]) * 100:.1f}%")
print(f"Predicted class: {np.argmax(predictions[0])}")
```

Run:
```bash
python test_model.py
```

Expected output:
```
Predictions: [0.02 0.85 0.08 0.03 0.02]
Sum of probabilities: 1.0
Max confidence: 85.0%
Predicted class: 1
```

---

## 🔐 Security Pre-Launch

- [ ] Change `app.secret_key` to random string
  ```python
  app.secret_key = os.environ.get("FLASK_SECRET", "your-random-key-here")
  ```

- [ ] Remove `debug=True` for production
  ```python
  app.run(debug=False)  # Production
  ```

- [ ] Verify password hashing is enabled
  ```python
  # Check in register() function:
  hashed = generate_password_hash(password)
  ```

- [ ] CORS is configured (if needed)
  ```python
  # Already imported: from flask_cors import CORS
  # Can add: CORS(app)
  ```

---

## 📈 Performance Checklist

- [ ] Model loads in < 5 seconds on startup
- [ ] First prediction in < 3 seconds
- [ ] Subsequent predictions in < 1 second
- [ ] Database queries are fast
- [ ] File uploads complete quickly
- [ ] Result page loads in < 2 seconds

### Optimization Tips
```python
# Already implemented:
# ✓ Model cached in memory
# ✓ Predictions run with verbose=0 (no console spam)
# ✓ Image preprocessing is efficient
# ✓ Database uses indexes
```

---

## 📝 Deployment Checklist

Before deploying to production:

- [ ] All HTML files present
- [ ] CSS file properly linked
- [ ] Model file in correct location
- [ ] Database initialized
- [ ] Upload folder exists
- [ ] Environment variables set
- [ ] Debug mode OFF
- [ ] Secret key changed
- [ ] HTTPS/SSL configured
- [ ] Rate limiting enabled
- [ ] Error logging configured

---

## 🎯 Success Criteria

After launch, verify:

✅ Home page loads
✅ Can register account
✅ Can login
✅ Can upload image
✅ Can view prediction
✅ Model predicts correctly
✅ Recommendation text displays
✅ Confidence % shows
✅ Risk level visible
✅ Download works
✅ All links functional
✅ Database stores data
✅ No errors in console
✅ Mobile responsive
✅ Fast performance

---

## 📞 Emergency Contact Points

If something breaks:

1. **Check console for errors**
   ```bash
   # Look for red text in terminal/console
   # Note the error message
   ```

2. **Verify model file**
   ```bash
   ls backend/models/
   # Should show: Skin_Cancer_Model.h5
   ```

3. **Reset database**
   ```bash
   del backend/app.db
   python app.py  # Recreates DB
   ```

4. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

5. **Check Python version**
   ```bash
   python --version  # Should be 3.7+
   ```

---

## ✨ Final Verification

Before declaring success:

```bash
# 1. Run this command
python -c "
import flask
import tensorflow
import numpy
import PIL
print('✓ All imports successful')
"

# 2. Check model file
dir backend\models\Skin_Cancer_Model.h5

# 3. Start app
python app.py

# 4. Visit http://localhost:5000

# 5. Complete test flow:
#    - Register
#    - Login
#    - Upload test image
#    - View results
#    - Check console for errors
```

If all steps complete without errors → **LAUNCH SUCCESSFUL** 🎉

---

## 📋 Post-Launch Tasks

After successful launch:

- [ ] Monitor error logs
- [ ] Test with different image sizes
- [ ] Test with different skin tones
- [ ] Gather user feedback
- [ ] Monitor model accuracy
- [ ] Check database growth
- [ ] Verify backup strategy
- [ ] Monitor server performance
- [ ] Update documentation based on issues

---

**Your AI Skin Disease Detection system is ready for launch!**

Good luck! 🚀
