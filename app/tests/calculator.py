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

def calculateBMI(height_cm, weight):
    max_weight = 1000
    max_height = 350
    # Validate inputs
    if height_cm <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive values.")
    if weight > max_weight:
        raise ValueError(f"Weight cannot exceed {max_weight} kg.")
    if height_cm > max_height:
        raise ValueError(f"Height cannot exceed {max_height} cm")
    # Convert height from cm to m
    height_m = height_cm / 100
    #Calculate BMI
    bmi = weight / (height_m ** 2)
    bmi = round(bmi, 2)
    # Determine BMI category
    if bmi < 18.5: category = 'Underweight'
    elif bmi < 24.9: category = 'Normal weight'
    elif bmi < 29.9: category = 'Overweight'
    else: category = 'Obesity'
    return bmi, category