from django.shortcuts import render, HttpResponse
from django.db.models import Avg, Count
from sklearn.calibration import CalibratedClassifierCV

import os
import joblib
import pandas as pd
import numpy as np
import string
import re
from nltk.stem import PorterStemmer

from django.conf import settings
from .models import Predictions
from datetime import datetime

# Create your views here.
def home(request):
    return HttpResponse("Hello World")

def base(request):
    return render(request, 'base.html')

def history(request):
    records = Predictions.objects.all().order_by('-id')

    total_predictions = Predictions.objects.count()

    last_prediction = Predictions.objects.order_by('-Pre_Date').first()

    avg_confidence = Predictions.objects.aggregate(
        Avg('Confidence')
    )['Confidence__avg']

    most_common = (
        Predictions.objects
        .values('Conditions')
        .annotate(total=Count('Conditions'))
        .order_by('-total')
        .first()
    )

    return render(request, 'history.html', {
        'records': records,
        'total_predictions': total_predictions,
        'last_prediction': last_prediction,
        'avg_confidence': avg_confidence,
        'most_common': most_common
    })

# Data Cleaning
def preprocess(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# model logic
MODEL_PATH = os.path.join(settings.BASE_DIR, 'myapp/models/model.pkl')

VECTORIZER_PATH = os.path.join(settings.BASE_DIR,'myapp/models/vectorizer.pkl')

ENCODER_PATH = os.path.join(settings.BASE_DIR, 'myapp/models/label_encoder.pkl')

# load model
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
encoder = joblib.load(ENCODER_PATH)

# def predict_condition(request):
#     prediction = None
#     if request.method == 'POST':
#         symptoms = request.POST.get('symptoms')

#         vector = vectorizer.transform([symptoms])
#         pred = model.predict(vector)
#         prediction = encoder.inverse_transform(pred)[0]
#     return render(request, 'myapp/templates/base.html', {
#         'prediction':prediction
#     })

# Gabe

def is_gibberish(text):
    if not text or len(text) < 3:
        return False
    
    if re.match(r'^(.)\1{4,}$', text):
        return True
    
    most_common = max(set(text), key=text.count)
    if text.count(most_common) / len(text) > 0.9:
        return True
    
    if re.match(r'^[bcdfghjklmnpqrstvwxyz]{8,}$', text):
        return True
    return False

# def base(request):
#     prediction = None
#     recommended_drug = None
#     confidence  =  None
#     error_message = None

#     if request.method == 'POST':
#         symptoms = request.POST.get('symptoms', '').strip()
        
#         if not symptoms:
#             error_message = "Please enter your symptoms"
#             records = Predictions.objects.all().order_by('-id')[:3]
#             return render(request, 'base.html', {
#                 'prediction': None,
#                 'recommended_drug': None,
#                 'error': error_message,
#                 'records': records
#             })
        
#         if is_gibberish(symptoms):
#             error_message = "Please enter valid symptoms, not random characters"
#             records = Predictions.objects.all().order_by('-id')[:3]
#             return render(request, 'base.html', {
#                 'prediction': None,
#                 'recommended_drug': None,
#                 'error': error_message,
#                 'records': records
#             })
        
#         if len(symptoms) < 3:
#             error_message = "Please provide more details"
#             records = Predictions.objects.all().order_by('-id')[:3]
#             return render(request, 'base.html', {
#                 'prediction': None,
#                 'recommended_drug': None,
#                 'error': error_message,
#                 'records': records

#             })

#         # clean text before model
#         # cleaned_symptoms = preprocess(symptoms)
#     try:
#         cleaned_symptoms = preprocess(symptoms)
#         if not cleaned_symptoms:
#             error_message = "Invalid symptoms. Please use text only."
#             return render(request, 'base.html', {
#                 'prediction': prediction,
#                 'recommended_drug': recommended_drug,
#                 'error': error_message,
#                 'records': Predictions.objects.all().order_by('-id')[:3]
#             })

#         vector = vectorizer.transform([symptoms])
#         pred = model.predict(vector)
#         prediction = encoder.inverse_transform(pred)[0]
#         recommended_drug = recommend_drug(prediction)

#         # dump Values
#         # confidence  =  0.95
#         # scores = model.decision_function(vector)
#         # probabilities = softmax(scores[0])
#         # confidence = round(np.max(probabilities) * 100, 2)
#         probs = model.predict_proba(vector)[0]
#         confidence = round(np.max(probs) * 100, 1)
#         # prediction = model.predict(vector)[0]

#         # Error 4 Low Condifence Score'
#         if confidence < 50:
#             error_message = f"Low confidence ({confidence}%). Please consult a doctor."

#         # save data to my sql
#         Predictions.objects.create(
#             Symptoms = symptoms,
#             Conditions = prediction,
#             Confidence = confidence,
#             RecommendedDrug = recommended_drug,
#             Pre_Date = datetime.now()
#         )
#     except Exception as e:
#         error_message = f"Prediction error: {str(e)}"


#     # keep records
#     records = Predictions.objects.all().order_by('-id')[:3]

#     return render(request, 'base.html', {
#         'prediction': prediction,
#         'recommended_drug': recommended_drug,
#         'error': error_message,
#         'records': records
#     })
def has_vowels(text):
    return bool(re.search(r'[aeiou]', text))

import requests

def is_real_word(word):

    try:
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
            timeout=2
        )

        return response.status_code == 200

    except:
        return False
    
def is_meaningful_text(text):

    words = text.lower().split()

    valid_words = 0

    for word in words:

        # remove very short words
        if len(word) < 3:
            continue

        if is_real_word(word):
            valid_words += 1

    return valid_words >= 1

def base(request):
    prediction = None
    recommended_drug = None
    confidence = None
    error_message = None

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '').strip()
        
        if not symptoms:
            error_message = "Please enter your symptoms"
        elif is_gibberish(symptoms):
            error_message = "Please enter valid symptoms, not random characters"
        elif not is_meaningful_text(symptoms):
            error_message = "Please enter meaningful English symptoms"
        else:
            try:
                cleaned_symptoms = preprocess(symptoms)
                
                
                if not cleaned_symptoms or len(cleaned_symptoms) < 3 or not has_vowels(cleaned_symptoms):
                    error_message = "Please enter meaningful symptoms (at least 3 letters)"
                else:
                    # FIXED: Use cleaned_symptoms here
                    vector = vectorizer.transform([cleaned_symptoms])
                    pred = model.predict(vector)
                    prediction = encoder.inverse_transform(pred)[0]
                    recommended_drug = recommend_drug(prediction)
                    
                    probs = model.predict_proba(vector)[0]
                    confidence = round(np.max(probs) * 100, 1)
                    
                    if confidence < 62:
                        error_message = f"Low confidence ({confidence}%). Please consult a doctor."
                    
                    # Save original symptoms (not cleaned)
                    Predictions.objects.create(
                        Symptoms = symptoms,
                        Conditions = prediction,
                        Confidence = confidence,
                        RecommendedDrug = recommended_drug,
                        Pre_Date = datetime.now()
                    )
            except Exception as e:
                error_message = f"Prediction error: {str(e)}"
    
    # Single records query at the bottom
    records = Predictions.objects.all().order_by('-id')[:3]
    
    return render(request, 'base.html', {
        'prediction': prediction,
        'recommended_drug': recommended_drug,
        'error': error_message,
        'records': records,
        'confidence': confidence
    })


DRUG_DATASET = os.path.join(settings.BASE_DIR, 'myapp/models/drugs.csv')
drug_df = pd.read_csv(DRUG_DATASET)

def recommend_drug(condition):

    filtered = drug_df[drug_df['condition'].str.lower() == condition.lower()]
    if filtered.empty:
        return "No Drug Found"
    
    # Group Drugs
    grouped = filtered.groupby('drugName').agg({
        'rating': 'mean',
        'usefulCount': 'sum'
    }).reset_index()

    # Calculate Recommendation Score that is 70% Rating
    grouped['score'] = (
        0.7 * grouped['rating']
        + 0.3 * np.log1p(grouped['usefulCount'])
    )

    # Search and Sort Drug with Higher Score
    top_drug = grouped.sort_values(
        by='score',
        ascending=False
    ).iloc[0]
    return top_drug['drugName']
