# AI-DRUG-RECOMMENDATION-APPLICATION

## MedRecomm

MedRecomm is a machine learning-based drug recommendation system that predicts patient conditions from drug reviews and recommends suitable medications through an interactive dashboard.

The system focuses on three medical conditions:
- Depression
- High Blood Pressure
- Type 2 Diabetes

Natural Language Processing (NLP) techniques were used to preprocess and analyze patient reviews. TF-IDF feature extraction and a Linear Support Vector Machine (Linear SVM) model were implemented to achieve accurate condition classification and intelligent drug recommendation.

---

## Features

- Predicts patient conditions from review text
- Recommends suitable medications
- Uses NLP preprocessing techniques
- TF-IDF feature extraction
- Linear SVM machine learning model
- Interactive prediction dashboard
- Displays confidence scores
- Stores prediction history

---

## Machine Learning Workflow

1. Data Collection
2. Data Filtering
3. Text Preprocessing
4. Tokenization
5. Lemmatization
6. Feature Extraction using TF-IDF
7. Feature Scaling using StandardScaler
8. Model Training using Linear SVM
9. Model Evaluation

---

## Technologies Used

- Python
- Django
- Scikit-learn
- Pandas
- NumPy
- HTML/CSS
- NLP (Natural Language Processing)

---

## Dataset Features

The dataset contains:
- Drug Name
- Condition
- Patient Review
- Rating
- Date
- Useful Count

---

## Model Performance

- Model: Linear Support Vector Machine (Linear SVM)
- Feature Extraction: TF-IDF
- Hyperparameter Tuning: RandomizedSearchCV
- Final Accuracy: 95.73%

---

## Project Structure

```text
medics/
│
├── manage.py
├── db.sqlite3
├── medics/
├── myapp/
│   ├── models/
│   ├── static/
│   ├── templates/
│   └── migrations/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Khopolo5/AI-DRUG-RECOMMENDATION-APPLICATION.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python manage.py runserver
```

---

## Authors

AI Drug Recommendation Group Project
