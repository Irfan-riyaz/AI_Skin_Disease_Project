import os
import numpy as np
from tensorflow import keras
import tensorflow as tf
from PIL import Image

MODEL_PATH = os.path.join('models', 'multi_class_model.h5')
CLASSES_PATH = os.path.join('models', 'classes.txt')
UPLOADS = ['uploads/test_benign.jpg', 'uploads/test_melanoma_like.jpg', 'uploads/test_skin.jpg']

if not os.path.exists(MODEL_PATH):
    print('Model not found:', MODEL_PATH)
    raise SystemExit(1)
if not os.path.exists(CLASSES_PATH):
    print('Classes file not found:', CLASSES_PATH)
    raise SystemExit(1)

model = keras.models.load_model(MODEL_PATH)
with open(CLASSES_PATH, 'r', encoding='utf-8') as fh:
    classes = [l.strip() for l in fh if l.strip()]

print(f'Loaded model: {MODEL_PATH}\nFound {len(classes)} classes')

def preprocess(path, size=(224,224)):
    img = Image.open(path).convert('RGB')
    img = img.resize(size)
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, 0)

for up in UPLOADS:
    if not os.path.exists(up):
        print('Missing upload:', up)
        continue
    arr = preprocess(up)
    preds = model.predict(arr, verbose=0)
    vec = np.array(preds[0]).flatten()
    try:
        probs = tf.nn.softmax(vec).numpy()
    except Exception:
        probs = vec
        s = probs.sum()
        if s>0:
            probs = probs / s
    top_k = min(3, len(probs))
    idxs = np.argsort(probs)[::-1][:top_k]
    print('\n==', up, '==')
    for i in idxs:
        print(f"{classes[int(i)]}: {probs[int(i)]*100:.2f}%")
