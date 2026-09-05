"""Rule-based explanation of why a heart-disease risk was flagged."""


def get_risk_reasons(data):
    """data = form.cleaned_data -> returns list of human-readable risk factors."""
    reasons = []

    if data["age"] >= 55:
        reasons.append(f"Age {data['age']} - risk rises after 55.")

    if data["sex"] == "M":
        reasons.append("Male - higher baseline risk of heart disease.")

    if data["chest_pain_type"] == "ASY":
        reasons.append("Chest pain type 'Asymptomatic' (ASY) - no typical angina; in this data "
                       "such patients most often turn out to have heart disease (silent ischemia).")
    elif data["chest_pain_type"] == "TA":
        reasons.append("Typical angina - chest pain of cardiac origin.")

    if data["resting_bp"] >= 140:
        reasons.append(f"High resting blood pressure ({data['resting_bp']} mmHg, normal < 120).")

    if data["cholesterol"] >= 240:
        reasons.append(f"High cholesterol ({data['cholesterol']} mg/dL, desirable < 200).")

    if data["fasting_bs"] == 1:
        reasons.append("Fasting blood sugar reported as high - a diabetes-related risk factor.")

    if data["resting_ecg"] in ("ST", "LVH"):
        label = "ST-T wave abnormality" if data["resting_ecg"] == "ST" else "left ventricular hypertrophy"
        reasons.append(f"Abnormal resting ECG ({label}).")

    if data["max_hr"] < 120:
        reasons.append(f"Low maximum heart rate ({data['max_hr']} bpm) - poor exercise capacity.")

    if data["exercise_angina"] == "Y":
        reasons.append("Chest pain during exercise (exercise-induced angina).")

    if data["oldpeak"] >= 2.0:
        reasons.append(f"High ST depression on exercise ECG (oldpeak {data['oldpeak']}) - "
                       f"below 2.0 is considered the healthy side.")

    if data["st_slope"] in ("Flat", "Down"):
        reasons.append(f"{data['st_slope']} ST slope during exercise - abnormal (normal is 'Up').")

    if not reasons:
        reasons.append("A combination of several borderline values pushed the overall risk up.")

    return reasons
