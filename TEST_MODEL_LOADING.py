#!/usr/bin/env python3
"""
Quick test script to verify:
1. Model file exists
2. Classes file exists
3. DISEASE_INFO has all classes
4. Model can be loaded successfully
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("MODEL LOADING TEST")
print("=" * 60)

# Check files exist
print("\n1. Checking file existence...")
models_dir = os.path.join(os.path.dirname(__file__), 'backend', 'models')
model_h5 = os.path.join(models_dir, 'skin_disease_model.h5')
model_keras = os.path.join(models_dir, 'skin_disease_model.keras')
classes_file = os.path.join(models_dir, 'classes.txt')

print(f"   Model .h5 exists: {os.path.exists(model_h5)}")
print(f"   Model .keras exists: {os.path.exists(model_keras)}")
print(f"   Classes file exists: {os.path.exists(classes_file)}")

# Read classes
if os.path.exists(classes_file):
    with open(classes_file, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f if line.strip()]
    print(f"\n2. Classes loaded: {len(classes)} classes")
    print("   First 5 classes:")
    for i, c in enumerate(classes[:5]):
        print(f"      {i}: {c}")
    print("   Last 5 classes:")
    for i, c in enumerate(classes[-5:], start=len(classes)-5):
        print(f"      {i}: {c}")
else:
    print("   ERROR: Classes file not found!")
    classes = []

# Check DISEASE_INFO
try:
    from app import DISEASE_INFO, load_model_safe, model, CLASS_NAMES
    print(f"\n3. DISEASE_INFO dictionary loaded: {len(DISEASE_INFO)} entries")
    print("   Checking coverage...")
    
    missing_classes = []
    for cls in classes:
        if cls not in DISEASE_INFO:
            missing_classes.append(cls)
    
    if missing_classes:
        print(f"   WARNING: {len(missing_classes)} classes not in DISEASE_INFO:")
        for mc in missing_classes[:10]:
            print(f"      - {mc}")
    else:
        print("   ✓ All classes covered in DISEASE_INFO!")
    
    # Try to load model
    print(f"\n4. Loading model...")
    load_model_safe()
    
    if model is not None:
        print(f"   ✓ Model loaded successfully!")
        print(f"   Model type: {type(model)}")
        print(f"   Output shape: {model.output_shape}")
        print(f"   CLASS_NAMES count: {len(CLASS_NAMES) if CLASS_NAMES else 'None'}")
    else:
        print(f"   ERROR: Model failed to load!")

except ImportError as e:
    print(f"   ERROR importing from app: {e}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
