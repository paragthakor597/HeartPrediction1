from django.shortcuts import render,redirect
from .models import HeartPrediction
from .forms import HeartForm,UserRegistrationForm
from .reasons import get_risk_reasons
from .report import build_report_pdf
from django.contrib.auth import login
from django.http import HttpResponse, Http404
from django.utils.text import slugify
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
    reasons = []
    prediction_id = None

    if request.method == 'POST':
        form = HeartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

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

            result = int(pipeline.predict(input_data)[0])
            print("predicton", result)

            if result == 1:
                prediction = "Heart Disease Risk Detected"
                reasons = get_risk_reasons(data)
            else:
                prediction = "No Heart Disease Risk"

            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.user = request.user
            obj.result = result
            obj.risk_reasons = reasons
            obj.save()
            prediction_id = obj.id
    else:
        # Returning user: start the form with whatever they filled in last time.
        initial = {}
        if request.user.is_authenticated:
            last = HeartPrediction.objects.filter(user=request.user).order_by('-id').first()
            if last:
                initial = {f: getattr(last, f) for f in HeartForm.Meta.fields}
        form = HeartForm(initial=initial)

    return render(request, 'heart/all_heart_view.html', {
        'form': form,
        'prediction': prediction,
        'reasons': reasons,
        'prediction_id': prediction_id,
    })


def download_report(request, pk):
    try:
        obj = HeartPrediction.objects.get(pk=pk)
    except HeartPrediction.DoesNotExist:
        raise Http404("Report not found")

    pdf_bytes = build_report_pdf(obj)
    # Name the file after the user, falling back to "guest" for anonymous entries.
    name = slugify(obj.user.username) if obj.user else "guest"
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="heart_report_{name}.pdf"'
    return response

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
            print(form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def About(request):
    return render(request, "heart/About.html")
