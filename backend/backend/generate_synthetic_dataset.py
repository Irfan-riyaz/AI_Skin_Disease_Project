import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(__file__)
CLASSES_FILE = os.path.join(BASE, 'models', 'classes_template.txt')
OUT_DIR = os.path.join(BASE, '..', 'data')
NUM_PER_CLASS = 2
IMG_SIZE = (224,224)

os.makedirs(OUT_DIR, exist_ok=True)

with open(CLASSES_FILE, 'r', encoding='utf-8') as fh:
    classes = [line.strip() for line in fh if line.strip()]

print(f"Creating synthetic dataset for {len(classes)} classes at {OUT_DIR}")

for cls in classes:
    safe = ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in cls).strip()
    cls_dir = os.path.join(OUT_DIR, safe)
    os.makedirs(cls_dir, exist_ok=True)
    for i in range(NUM_PER_CLASS):
        # create color from hash of class + index
        h1 = hash(safe + str(i))
        h2 = hash(safe + str(i*2))
        h3 = hash(safe + str(i*3))
        img = Image.new('RGB', IMG_SIZE, (int(h1 % 200)+30, int(h2 % 200)+30, int(h3 % 200)+30))
        draw = ImageDraw.Draw(img)
        text = cls[:30]
        try:
            font = ImageFont.truetype('arial.ttf', 16)
        except Exception:
            font = ImageFont.load_default()
        # Pillow versions vary; use textbbox if available
        try:
            bbox = draw.textbbox((0,0), text, font=font)
            w = bbox[2]-bbox[0]
            h = bbox[3]-bbox[1]
        except Exception:
            try:
                w,h = font.getsize(text)
            except Exception:
                w,h = (100, 20)
        draw.text(((IMG_SIZE[0]-w)/2, (IMG_SIZE[1]-h)/2), text, fill=(255,255,255), font=font)
        fname = os.path.join(cls_dir, f"{safe.replace(' ','_')}_{i+1}.jpg")
        img.save(fname, quality=85)

print('Done')
