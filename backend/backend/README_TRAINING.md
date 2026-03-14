Training instructions for multi-class dermatology model
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
Overview
--------
This project supports training a multi-class skin disease classifier from data organized in a directory structure:

  data/train/<class_name>/*.jpg

The included `train.py` uses transfer learning (EfficientNetB0 by default) and writes a Keras `.h5` model and a `classes.txt` file.

Prepare your dataset
--------------------
1. Create a folder with one subfolder per disease label. Subfolder names will be used as class labels.

Example:

  data/
    acne_vulgaris/
      img001.jpg
      img002.jpg
    psoriasis_vulgaris/
      ps1.jpg

2. Aim for at least 50-200 images per class for reasonable results — more is better.

Train
-----
Install dependencies in the `backend` virtualenv (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install tensorflow==2.12.0  # or appropriate TF version for your GPU
```

Run training (example):

```powershell
python train.py --data_dir data --output models/multi_class_model.h5 --classes_out models/classes.txt --epochs 20 --batch_size 32
```

Notes
-----
- For best accuracy, gather high-quality labeled images and consider data augmentation.
- After initial training, unfreeze base layers and fine-tune with a lower learning rate.
- Use class weights or oversampling if classes are imbalanced.
- Evaluate with a separate hold-out test set.

Integrate into app
------------------
Place `models/multi_class_model.h5` and `models/classes.txt` in `backend/models/` (or `backend/`) then restart the Flask app. The app will automatically detect and use the multi-class model and class labels.
