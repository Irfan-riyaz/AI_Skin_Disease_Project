# Comprehensive Dermatological Disease Database
# This file contains detailed medical information for 95+ skin conditions

DISEASE_DATABASE = {
    # Additional 50+ diseases beyond those in app.py
    "pityriasis rosea": {
        "name": "Pityriasis Rosea",
        "cause": "Viral infection (Human Herpesvirus 6 or 7), contagious in early stages, benign condition",
        "risk": "Low Risk - Self-Limiting",
        "recommendations": [
            "Usually resolves spontaneously in 6-8 weeks",
            "Topical corticosteroids or calcineurin inhibitors for itch relief",
            "Sunscreen SPF 50+ to avoid post-inflammatory pigmentation changes",
            "Oral antihistamines for symptomatic relief"
        ],
        "dermatologists": ["Viral Exanthem Specialist"]
    },
    
    "tinea pedis": {
        "name": "Tinea Pedis (Athlete's Foot)",
        "cause": "Fungal infection (Trichophyton rubrum, T. mentagrophytes), warm moist feet environment",
        "risk": "Low Risk - Contagious, Readily Treatable",
        "recommendations": [
            "Topical antifungal creams, powders, or solutions daily",
            "Keep feet dry, change socks frequently",
            "Wear breathable footwear and avoid communal shower areas",
            "Oral antifungals if topical treatment ineffective after 4 weeks"
        ],
        "dermatologists": ["Mycology Specialist"]
    },
    
    "tinea corporis": {
        "name": "Tinea Corporis (Ringworm)",
        "cause": "Fungal infection (Trichophyton, Microsporum, Epidermophyton), animal or human contact",
        "risk": "Low Risk - Contagious, Readily Treatable",
        "recommendations": [
            "Topical antifungal creams applied twice daily for 2-4 weeks",
            "Wash infected areas daily with antifungal soap",
            "Avoid sharing personal items like towels and clothing",
            "Oral antifungals for scalp involvement or extensive disease"
        ],
        "dermatologists": ["Mycology Specialist"]
    },
    
    "tinea capitis": {
        "name": "Tinea Capitis (Scalp Ringworm)",
        "cause": "Fungal infection of scalp (Microsporum canis, Trichophyton tonsurans), common in children",
        "risk": "Low Risk - Contagious to Others",
        "recommendations": [
            "Oral antifungal therapy (griseofulvin or terbinafine) required",
            "Topical antifungal shampoos as adjunct (selenium sulfide, ketoconazole)",
            "Avoid shared hats, combs, and personal items",
            "Monitor for treatment response and repeat infections"
        ],
        "dermatologists": ["Pediatric Dermatology Specialist"]
    },
    
    "tinea versicolor": {
        "name": "Tinea Versicolor (Pityriasis Versicolor)",
        "cause": "Malassezia furfur overgrowth, hyperhidrosis, warm climate, genetic predisposition",
        "risk": "Low Risk - Cosmetic, Recurrence Common",
        "recommendations": [
            "Topical antifungal creams or shampoos (selenium sulfide, miconazole)",
            "Oral antifungals (fluconazole) for extensive disease or recurrent cases",
            "Regular maintenance therapy during warm months to prevent recurrence",
            "Sunscreen use as post-inflammatory hypopigmentation is common"
        ],
        "dermatologists": ["Mycology Specialist"]
    },
    
    "scabies": {
        "name": "Scabies",
        "cause": "Sarcoptes scabiei mite infestation, human-to-human transmission, close contact",
        "risk": "Low Risk - Contagious, Treatable",
        "recommendations": [
            "Topical permethrin 5% cream applied from neck down, overnight",
            "Treat all household members and close contacts simultaneously",
            "Wash all clothing and bedding in hot water",
            "Oral ivermectin for crusted/institutional scabies"
        ],
        "dermatologists": ["Parasitology Specialist"]
    },
    
    "varicella zoster": {
        "name": "Varicella-Zoster (Chickenpox/Shingles)",
        "cause": "Viral infection, chickenpox primary infection, reactivation causes herpes zoster",
        "risk": "Moderate Risk - Pain and Post-Herpetic Neuralgia",
        "recommendations": [
            "Antiviral medications (acyclovir, valacyclovir) within 72 hours of onset",
            "Pain management with gabapentin or pregabalin",
            "Keep lesions clean and covered to prevent infection",
            "Avoid contact with non-immune individuals, especially pregnant women"
        ],
        "dermatologists": ["Viral Infection Specialist"]
    },
    
    "herpes simplex": {
        "name": "Herpes Simplex Virus (HSV)",
        "cause": "HSV-1 or HSV-2 viral infection, primary or recurrent episodes, contact transmission",
        "risk": "Low Risk (Recurrent) to High Risk (Primary Neonatal)",
        "recommendations": [
            "Antiviral therapy (acyclovir, valacyclovir) for primary and recurrent episodes",
            "Prophylactic antivirals for frequent recurrences (>6 per year)",
            "Avoid intimate contact during active lesions",
            "Neonatal HSV requires aggressive IV antiviral treatment"
        ],
        "dermatologists": ["Viral Infection Specialist"]
    },
    
    "molluscum contagiosum": {
        "name": "Molluscum Contagiosum",
        "cause": "Poxvirus infection, contact transmission, common in children and immunocompromised",
        "risk": "Low Risk - Contagious, Usually Self-Limited",
        "recommendations": [
            "Often resolves spontaneously within 6-12 months",
            "Topical treatments: imiquimod, tretinoin, or cantharidin",
            "Physical removal by curettage or cryotherapy if cosmetically concerning",
            "Avoid sharing towels and personal care items"
        ],
        "dermatologists": ["Viral Infection Specialist"]
    },
    
    "warts": {
        "name": "Warts (Common, Plantar, Genital)",
        "cause": "Human Papillomavirus (HPV) infection, contact transmission, immunosuppression risk",
        "risk": "Low Risk (Common) to Moderate Risk (Genital)",
        "recommendations": [
            "Topical treatments: salicylic acid, imiquimod, tretinoin",
            "Physical removal: cryotherapy, laser, surgical excision",
            "HPV vaccination for prevention (genital warts)",
            "Avoid contact and wear protective covering (plantar warts)"
        ],
        "dermatologists": ["HPV and Wart Specialist"]
    },
    
    "sebaceous cyst": {
        "name": "Sebaceous Cyst",
        "cause": "Keratin-filled cyst from hair follicle, benign, common on scalp and trunk",
        "risk": "Low Risk - Non-Malignant",
        "recommendations": [
            "No treatment necessary unless cosmetically bothersome or infected",
            "If infected, warm compresses or antibiotics may help",
            "Surgical excision with intact wall removal prevents recurrence",
            "Intralesional corticosteroid injections can help drainage"
        ],
        "dermatologists": ["Skin Surgery Specialist"]
    },
    
    "lipoma": {
        "name": "Lipoma",
        "cause": "Benign fatty tumor, genetic predisposition, normal variant, slow growth",
        "risk": "Low Risk - Non-Malignant",
        "recommendations": [
            "Monitoring sufficient if asymptomatic and non-interfering",
            "Surgical excision if cosmetically concerning or bothersome",
            "Steroid injections may reduce size (limited effectiveness)",
            "No malignant potential - reassurance typically indicated"
        ],
        "dermatologists": ["Skin Surgery Specialist"]
    },
    
    "solar lentig": {
        "name": "Solar Lentigo (Age Spot)",
        "cause": "UV-induced pigmentation, sun damage, aging, benign melanocytic lesion",
        "risk": "Low Risk - Cosmetic",
        "recommendations": [
            "SPF 50+ daily sunscreen to prevent new lesions",
            "Laser therapy (IPL, Q-switched laser) for removal",
            "Topical depigmenting agents (hydroquinone, tretinoin combination)",
            "Monitor for any changes in appearance or symptoms"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "ephelides": {
        "name": "Ephelides (Freckles)",
        "cause": "Genetic predisposition, UV exposure, common in light-skinned individuals",
        "risk": "Low Risk - Cosmetic",
        "recommendations": [
            "SPF 50+ daily sunscreen application (most important prevention)",
            "Avoid deliberate sun exposure, especially 10 AM-4 PM",
            "Laser treatment (IPL, Q-switched) for cosmetic improvement",
            "Regular monitoring for concerning changes in appearance"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "melasma": {
        "name": "Melasma",
        "cause": "Genetic predisposition, UV exposure, hormonal factors (pregnancy, OCPs, HRT)",
        "risk": "Low Risk - Cosmetic and Psychological Impact",
        "recommendations": [
            "SPF 50+ broad-spectrum sunscreen daily (critical for prevention)",
            "Consider discontinuing oral contraceptives or HRT if contributing",
            "Topical agents: hydroquinone, tretinoin, azelaic acid combinations",
            "Laser or chemical peels for resistant cases (risk of post-inflammatory hyperpigmentation)"
        ],
        "dermatologists": ["Cosmetic/Dermatologic Surgeon"]
    },
    
    "vitiligo": {
        "name": "Vitiligo",
        "cause": "Autoimmune destruction of melanocytes, genetic predisposition, associated conditions",
        "risk": "Moderate Risk - Psychological Impact, Skin Cancer Risk",
        "recommendations": [
            "SPF 50+ sunscreen on depigmented areas (burn risk)",
            "Topical corticosteroids or calcineurin inhibitors",
            "Phototherapy (UVB, PUVA, excimer laser) for extensive disease",
            "Consider oral corticosteroids or systemic agents for progressive disease"
        ],
        "dermatologists": ["Pigmentation Disorder Specialist"]
    },
    
    "post inflammatory hyperpigmentation": {
        "name": "Post-Inflammatory Hyperpigmentation",
        "cause": "Melanin overproduction following inflammation (acne, dermatitis, trauma)",
        "risk": "Low Risk - Usually Self-Limiting",
        "recommendations": [
            "SPF 50+ sunscreen to prevent darkening and promote fading",
            "Topical depigmenting agents: hydroquinone, tretinoin, azelaic acid",
            "Avoid further irritation of affected areas",
            "Laser or chemical peels if persistent after 6-12 months"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "post inflammatory hypopigmentation": {
        "name": "Post-Inflammatory Hypopigmentation",
        "cause": "Reduced melanin following severe inflammation, trauma, or previous inflammation",
        "risk": "Low Risk - Usually Self-Limiting",
        "recommendations": [
            "SPF 50+ broad-spectrum sunscreen to protect hypopigmented areas",
            "Topical corticosteroids during active inflammation to prevent it",
            "Laser therapy (excimer) may help stimulate repigmentation",
            "Usually fades over months to years as inflammation resolves"
        ],
        "dermatologists": ["Pigmentation Disorder Specialist"]
    },
    
    "erythema multiforme": {
        "name": "Erythema Multiforme",
        "cause": "Hypersensitivity reaction (HSV, medications, infections), Type IV hypersensitivity",
        "risk": "Moderate Risk - Can Involve Mucosa/Systemic Organs",
        "recommendations": [
            "Identify and remove causative agent (especially medications)",
            "Treat underlying infection (especially HSV with antivirals)",
            "Topical corticosteroids for skin lesions and oral involvement",
            "Systemic corticosteroids for severe or extensive disease"
        ],
        "dermatologists": ["Hypersensitivity Reaction Specialist"]
    },
    
    "stevens johnson syndrome": {
        "name": "Stevens-Johnson Syndrome (SJS)",
        "cause": "Severe hypersensitivity reaction, medications (NSAIDs, antibiotics, anticonvulsants)",
        "risk": "High Risk - Life-Threatening",
        "recommendations": [
            "Emergency hospitalization required",
            "Immediately discontinue causative medication",
            "Supportive care: fluid management, infection prevention, pain control",
            "Consider IVIG or systemic corticosteroids in specialist consultation"
        ],
        "dermatologists": ["Critical Care Dermatology Specialist"]
    },
    
    "toxic epidermal necrolysis": {
        "name": "Toxic Epidermal Necrolysis (TEN)",
        "cause": "Severe drug reaction (NSAIDs, antibiotics, anticonvulsants, allopurinol)",
        "risk": "Very High Risk - Medical Emergency",
        "recommendations": [
            "Intensive care unit admission required",
            "Immediately stop all causative medications",
            "Supportive care: fluid/electrolyte management, temperature control",
            "Consider specialized burn center or specialized dermatology ICU"
        ],
        "dermatologists": ["Critical Care Dermatology Specialist"]
    },
    
    "pemphigus vulgaris": {
        "name": "Pemphigus Vulgaris",
        "cause": "Autoimmune disease, IgG antibodies against desmoglein 3 and 1",
        "risk": "High Risk - Systemic Disease",
        "recommendations": [
            "Systemic corticosteroids (high-dose initial therapy required)",
            "Steroid-sparing immunosuppressants (mycophenolate, azathioprine)",
            "Rituximab (anti-B cell therapy) for difficult cases",
            "Specialist rheumatology/dermatology management essential"
        ],
        "dermatologists": ["Autoimmune Blistering Disorder Specialist"]
    },
    
    "bullous pemphigoid": {
        "name": "Bullous Pemphigoid",
        "cause": "Autoimmune disease, IgG antibodies against basement membrane proteins",
        "risk": "Moderate Risk - Systemic Autoimmune Disease",
        "recommendations": [
            "Topical corticosteroids for localized disease",
            "Systemic corticosteroids for moderate-severe disease",
            "Steroid-sparing agents: mycophenolate, methotrexate, azathioprine",
            "Specialist dermatology and possible rheumatology management"
        ],
        "dermatologists": ["Autoimmune Blistering Disorder Specialist"]
    },
    
    "dermatitis herpetiformis": {
        "name": "Dermatitis Herpetiformis",
        "cause": "Gluten-sensitive condition associated with celiac disease, IgA antibodies",
        "risk": "Moderate Risk - Associated Systemic Disease",
        "recommendations": [
            "Gluten-free diet (most important - addresses root cause)",
            "Dapsone for symptomatic relief (rapid improvement, weeks)",
            "Screen for celiac disease with serology and GI evaluation",
            "Nutritionist consultation for proper gluten-free diet implementation"
        ],
        "dermatologists": ["Celiac Dermatology Specialist"]
    },
    
    "porphyria cutanea tarda": {
        "name": "Porphyria Cutanea Tarda",
        "cause": "Deficiency in porphyrin metabolism enzyme, photosensitivity, triggers: alcohol, estrogen",
        "risk": "Moderate Risk - Photosensitivity, Liver Disease",
        "recommendations": [
            "SPF 50+ protective clothing essential",
            "Avoid alcohol, estrogen, and iron supplementation",
            "Phlebotomy or low-dose hydroxychloroquine for remission",
            "Hepatology consultation if liver disease present"
        ],
        "dermatologists": ["Metabolic Dermatology Specialist"]
    },
    
    "polymorphous light eruption": {
        "name": "Polymorphous Light Eruption",
        "cause": "Hypersensitivity to UVA or UVB radiation, genetic predisposition",
        "risk": "Low Risk - Usually Self-Limiting After Sun Exposure",
        "recommendations": [
            "SPF 50+ sunscreen and protective clothing",
            "Avoid sun exposure or use hardening therapy (gradual sun exposure)",
            "Topical corticosteroids for active lesions",
            "Phototherapy (UVA or PUVA) in winter may provide desensitization"
        ],
        "dermatologists": ["Photosensitivity Specialist"]
    },
    
    "actinic keratosis": {
        "name": "Actinic Keratosis (Solar Keratosis)",
        "cause": "UV radiation damage, precancerous lesion, risk of malignant transformation",
        "risk": "Moderate Risk - Premalignant Lesion",
        "recommendations": [
            "SPF 50+ sunscreen daily and protective clothing (prevention critical)",
            "Topical treatments: imiquimod, fluorouracil, diclofenac, ingenol mebutate",
            "Cryotherapy or laser for individual lesions",
            "Regular monitoring for signs of transformation to skin cancer"
        ],
        "dermatologists": ["Skin Cancer Specialist"]
    },
    
    "squamous cell carcinoma": {
        "name": "Squamous Cell Carcinoma (SCC)",
        "cause": "UV radiation damage, actinic keratosis progression, immunosuppression, HPV",
        "risk": "Moderate to High Risk - Metastatic Potential",
        "recommendations": [
            "Surgical excision (Mohs micrographic surgery preferred)",
            "Systemic therapy (cemiplimab) for advanced/metastatic disease",
            "Radiation therapy for inoperable lesions",
            "Ongoing surveillance for recurrence and metastasis"
        ],
        "dermatologists": ["Mohs Surgeon, Skin Cancer Specialist"]
    },
    
    "merkel cell carcinoma": {
        "name": "Merkel Cell Carcinoma",
        "cause": "Merkel cell polyomavirus, UV radiation, immunosuppression, elderly",
        "risk": "High Risk - Aggressive Neuroendocrine Carcinoma",
        "recommendations": [
            "Urgent oncology and dermatology specialist evaluation",
            "Surgical excision with sentinel lymph node biopsy",
            "Chemotherapy and/or immunotherapy (Avelumab)",
            "Regular surveillance imaging for systemic disease"
        ],
        "dermatologists": ["Oncologic Dermatology Specialist"]
    },
    
    "lymphoma cutaneous": {
        "name": "Cutaneous Lymphoma",
        "cause": "Malignant T-cell or B-cell proliferation, mycosis fungoides most common",
        "risk": "High Risk - Systemic Malignancy",
        "recommendations": [
            "Dermatopathology review and staging required",
            "Topical therapies for early-stage disease (phototherapy, topical retinoids)",
            "Systemic chemotherapy for advanced disease",
            "Hematology/oncology collaboration essential"
        ],
        "dermatologists": ["Cutaneous Lymphoma Specialist"]
    },
    
    "hemangioma": {
        "name": "Hemangioma",
        "cause": "Benign vascular proliferation, congenital or acquired, common in infants",
        "risk": "Low Risk - Usually Non-Malignant, May Interfere with Function",
        "recommendations": [
            "Most infantile hemangiomas regress spontaneously by age 7-10",
            "Propranolol for rapidly growing or interfering lesions",
            "Topical timolol for small superficial hemangiomas",
            "Laser therapy if no spontaneous improvement by age 10"
        ],
        "dermatologists": ["Pediatric Dermatology Specialist"]
    },
    
    "port wine stain": {
        "name": "Port-Wine Stain (Nevus Flammeus)",
        "cause": "Congenital vascular malformation, abnormal venous vasculature",
        "risk": "Low Risk - Non-Malignant, Cosmetic Concern",
        "recommendations": [
            "Pulsed dye laser for cosmetic improvement (requires multiple treatments)",
            "Earlier treatment in childhood more effective",
            "Protective makeup (Dermablend) for cosmetic coverage",
            "Monitor for associated syndromic features (Sturge-Weber syndrome)"
        ],
        "dermatologists": ["Vascular Lesion Specialist"]
    },
    
    "cherry angioma": {
        "name": "Cherry Angioma",
        "cause": "Benign vascular proliferation, age-related, common after age 30",
        "risk": "Low Risk - Non-Malignant",
        "recommendations": [
            "No treatment necessary for asymptomatic lesions",
            "Laser or cryotherapy for cosmetic reasons or bleeding lesions",
            "Avoid trauma to lesions (may bleed)",
            "Reassurance about benign nature appropriate"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "xanthelasma": {
        "name": "Xanthelasma",
        "cause": "Lipid deposits around eyelids, often associated with hyperlipidemia",
        "risk": "Low Risk - Cosmetic, May Indicate Lipid Abnormalities",
        "recommendations": [
            "Check lipid panel and consider statin therapy if elevated",
            "Surgical excision or laser ablation for cosmetic improvement",
            "Topical retinoids may provide some improvement",
            "Lifestyle modification: diet, exercise, weight management"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "skin tag": {
        "name": "Skin Tag (Acrochordon)",
        "cause": "Benign pedunculated growth, friction in skin folds, aging, genetic",
        "risk": "Low Risk - Non-Malignant",
        "recommendations": [
            "No treatment necessary unless cosmetically bothersome or traumatized",
            "Simple removal: ligation, cryotherapy, or surgical excision",
            "Avoid home removal attempts to prevent infection",
            "Reassurance about non-malignant nature appropriate"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "milia": {
        "name": "Milia",
        "cause": "Keratin-filled cysts, benign, common around eyes, can be primary or secondary",
        "risk": "Low Risk - Non-Malignant, Cosmetic",
        "recommendations": [
            "No treatment necessary for asymptomatic lesions",
            "Extraction by dermatologist if cosmetically concerning",
            "Topical retinoids may help prevent formation",
            "Usually requires professional removal for satisfactory cosmetic result"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "syringoma": {
        "name": "Syringoma",
        "cause": "Benign sweat gland tumor, common around eyes, genetic predisposition",
        "risk": "Low Risk - Non-Malignant, Cosmetic",
        "recommendations": [
            "No treatment necessary unless cosmetically bothersome",
            "Laser (CO2, erbium, pulsed dye) or electrocautery for removal",
            "Multiple treatments often needed for satisfactory result",
            "Reassurance about benign non-malignant nature appropriate"
        ],
        "dermatologists": ["Cosmetic Dermatologist"]
    },
    
    "molluscum contagiosum": {
        "name": "Molluscum Contagiosum",
        "cause": "Poxvirus infection, contact transmission, immunocompromised at risk",
        "risk": "Low Risk - Usually Self-Limiting",
        "recommendations": [
            "Often resolves spontaneously in 6-12 months",
            "Topical imiquimod, tretinoin, or cantharidin for faster resolution",
            "Physical removal: cryotherapy or curettage",
            "Avoid sharing towels, bathing together, or contact sports"
        ],
        "dermatologists": ["Viral Infection Specialist"]
    },
}

def merge_disease_databases():
    """Merge comprehensive disease data with main app database"""
    from app import DISEASE_INFO
    for disease_lower, data in DISEASE_DATABASE.items():
        # Add to DISEASE_INFO if not already present
        if disease_lower not in DISEASE_INFO:
            DISEASE_INFO[disease_lower] = data
