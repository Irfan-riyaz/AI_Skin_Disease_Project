# AI Skin Disease Detection System

An intelligent healthcare support system that uses Artificial Intelligence to analyze skin images and provide early screening insights.

## Features

- **User Authentication**: Secure login and registration
- **Image Upload**: Upload skin images for analysis
- **AI Prediction**: Real-time skin disease detection using deep learning
- **Detailed Results**: Disease name, cause, confidence level, and recommendations
- **Professional UI**: Modern, responsive design with consistent styling
- **Report Generation**: Download analysis reports

## Project Structure

```
AI_Skin_Disease_Project/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── app.db                 # SQLite database
│   ├── uploads/               # Uploaded images
│   ├── models/
│   │   └── Skin_Cancer_Model.h5  # Trained ML model
│   ├── static/
│   │   └── style.css          # CSS styling
│   └── templates/
│       ├── index.html         # Landing page
│       ├── login.html         # Login page
│       ├── register.html      # Registration page
│       ├── upload.html        # Image upload page
│       ├── result.html        # Diagnosis results page
│       ├── faq.html           # FAQ page
│       ├── help.html          # Help page
│       ├── feedback.html      # Feedback page
│       └── thanks.html        # Thank you page
└── README.md
```

## Setup & Installation

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Ensure Model is in Place
Place your trained model at: `backend/models/Skin_Cancer_Model.h5`

The model should output predictions for these classes:
- Melanoma
- Benign Lesions
- Seborrheic Keratosis
- Nevus (Moles)
- Basal Cell Carcinoma

### 5. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## User Flow

1. **Landing Page** → View system features and information
2. **Login/Register** → Create account or sign in
3. **Upload** → Select and upload a skin image (PNG/JPG)
4. **Processing** → AI model analyzes the image
5. **Results** → View diagnosis with:
   - Disease name
   - Confidence level (accuracy %)
   - Risk assessment
   - Cause of disease
   - Dermatologist recommendations
6. **Download** → Get detailed report (optional)

## Model Integration

The system uses a pre-trained Keras model (`Skin_Cancer_Model.h5`) that:
- Accepts images of size 224×224 pixels
- Outputs probabilities for 5 disease classes
- Achieves high accuracy on dermatological images

### Image Preprocessing
- Resizes input to 224×224
- Normalizes pixel values (0-1 range)
- Converts to RGB if necessary

## Database

SQLite database stores:
- User credentials (hashed passwords)
- User profiles (email, phone, username)
- Feedback entries with timestamps

## Security Features

- Password hashing using Werkzeug
- Session management with Flask
- CSRF protection ready
- Input validation on all forms

## Pages & Routes

| Page | Route | Method | Purpose |
|------|-------|--------|---------|
| Landing | `/` | GET | Home page with features |
| Login | `/login` | GET/POST | User authentication |
| Register | `/register` | GET/POST | New user signup |
| Upload | `/upload` | GET/POST | Image submission |
| Result | `/result` | GET | Diagnosis display |
| FAQ | `/faq` | GET | Frequently asked questions |
| Help | `/help` | GET | User assistance |
| Feedback | `/feedback` | GET/POST | User feedback form |
| Thanks | `/thanks` | GET | Thank you page |

## Important Notes

⚠️ **Disclaimer**: This system provides screening insights only and is NOT a substitute for professional medical diagnosis. Always consult a certified dermatologist for medical advice.

## Dependencies

- **Flask**: Web framework
- **TensorFlow/Keras**: Deep learning library
- **NumPy**: Numerical computing
- **Pillow**: Image processing
- **Werkzeug**: Utility library for web applications

## Troubleshooting

### Model Not Loading
- Ensure `Skin_Cancer_Model.h5` exists in `backend/models/`
- Check file permissions
- Verify TensorFlow is installed: `pip install --upgrade tensorflow`

### Image Upload Issues
- Ensure `backend/uploads/` directory exists
- Check file size limits
- Verify supported formats (PNG, JPG, JPEG)

### Database Issues
- Delete `app.db` to reset database
- Check write permissions on `backend/` folder

## Development

To modify disease information:
1. Edit `DISEASE_INFO` dictionary in `app.py`
2. Update class names in `class_names` list
3. Adjust image preprocessing if needed

## License

This project is for educational purposes.

## Support

For issues or questions, please create an issue or contact support.
