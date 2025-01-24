def calculateCreatinineClearance(age, weight, creatinine, sex):
    # Validate inputs
    if age <= 0 or weight <= 0 or creatinine <= 0:
        raise ValueError("Age, weight, and creatinine must be positive values.")

    # Convert creatinine to mg/dL if necessary (e.g., if provided in µmol/L)
    creatinine_mg_dl = creatinine / 88.4 if creatinine > 10 else creatinine

    # Use the correct K value
    K = 1.23 if sex.lower() == "male" else 1.04

    # Cockcroft-Gault formula
    creatinine_clearance = ((140 - age) * weight * K) / creatinine_mg_dl

    return creatinine_clearance
