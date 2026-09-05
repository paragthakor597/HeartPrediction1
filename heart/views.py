from django.shortcuts import render,redirect
from .models import HeartPrediction
from .forms import HeartForm,UserRegistrationForm
from django.contrib.auth import login
import joblib
import pandas as pd
import os
from django.conf import settings

pipeline = joblib.load(
    os.path.join(settings.BASE_DIR, "saved_model", "heart_pipeline.pkl")
)


def Home(request):
    return render(request, "heart/Home.html")

def all_heart_view(request):
    prediction = None
    if request.method == 'POST':
        form = HeartForm(request.POST) 
        if form.is_valid():
            data = form.cleaned_data
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
            obj.save()
            input_data = pd.DataFrame([{  
                    "Age": data["age"],
                    "Sex": data["sex"],
                    "ChestPainType": data["chest_pain_type"],
                    "RestingBP": data["resting_bp"],
                    "Cholesterol": data["cholesterol"],
                    "FastingBS": data["fasting_bs"],
                    "RestingECG": data["resting_ecg"],
                    "MaxHR": data["max_hr"],
                    "ExerciseAngina": data["exercise_angina"],
                    "Oldpeak": data["oldpeak"],
                    "ST_Slope": data["st_slope"]
            }])
            result = pipeline.predict(input_data)
            print("predicton",result)

        if result[0] == 1:
            prediction = "Heart Disease Risk Detected"
        else:
            prediction = "No Heart Disease Risk"
    else:
        form = HeartForm()
         
    return render(request, 'heart/all_heart_view.html', {
    'form': form,
    'prediction': prediction if request.method == "POST" and form.is_valid() else None
})
    
def register(request):
    if request.method == "POST":
        print(request.POST)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            print("User saved:", user.username)
            return redirect('Home')
        else:
            print(form.errors)   # 👈 ye add karo
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def About(request):
    return render(request, "heart/About.html")
        
