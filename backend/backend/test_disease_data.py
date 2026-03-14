#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify comprehensive disease information is loaded"""

from app import DISEASE_INFO, CLASS_NAMES

print("=" * 70)
print("DISEASE INFORMATION VERIFICATION")
print("=" * 70)

# Test diseases that should have comprehensive data
test_diseases = [
    'acne comedonica',
    'acne conglobata',
    'melanoma',
    'benign',
    'atopic dermatitis',
]

for disease_key in test_diseases:
    disease = DISEASE_INFO.get(disease_key, {})
    if disease:
        print(f"\n[OK] {disease.get('name', 'N/A')}")
        print(f"  Risk: {disease.get('risk', 'N/A')}")
        print(f"  Cause: {disease.get('cause', 'N/A')[:80]}...")
        recs = disease.get('recommendations', [])
        print(f"  Recommendations: {len(recs)} items")
    else:
        print(f"\n[MISSING] {disease_key} - NOT FOUND")

print("\n" + "=" * 70)
print(f"Total diseases in DISEASE_INFO: {len(DISEASE_INFO)}")
print(f"Total classes in CLASS_NAMES: {len(CLASS_NAMES) if CLASS_NAMES else 0}")
print("=" * 70)

# Check for placeholder text
placeholder_count = 0
real_data_count = 0

for key, disease_info in DISEASE_INFO.items():
    if "Consult a dermatologist for professional evaluation" in disease_info.get('cause', ''):
        placeholder_count += 1
    else:
        real_data_count += 1

print(f"\nDiseases with real data: {real_data_count}")
print(f"Diseases with placeholder data: {placeholder_count}")
print("=" * 70)
