# AI-Health-Prediction-system


# 🩺 AI Health Prediction System

A patient management app that predicts possible diseases from blood test results. Built with Python and Streamlit, backed by a Random Forest model trained on 12,000+ real hospital lab records.

---


## What It Does

You enter a patient's basic details and three blood values — glucose, hemoglobin, cholesterol. The app runs the values through a trained ML model and tells you the most likely disease, along with a plain-English remark explaining why.

Full CRUD — you can add, view, update, and delete patient records. Everything is stored in a local SQLite database.

---

## Dataset

**[Hospital Laboratory Data — Kaggle](https://www.kaggle.com/datasets/klingill/laboratory-data)**

- 12,009 patient records collected from a hospital laboratory  
- Features: Age, Gender, RBC, WBC, Hemoglobin, AST, ALT, Cholesterol, Glucose, Lipase, Spirometry, Creatinine, Troponin  
- Target: 9 disease categories (Anemia, Asthma, Cardiovascular Disease, Diabetes, Heart Attack, Infection, Kidney Disease, Liver Disease, Pancreatitis)  
- License: CC0 (Public Domain)

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| ML Model | Random Forest (scikit-learn) |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |

---

## ML Model Details

Trained and compared 7 classifiers on the dataset:

- Logistic Regression  
- KNN  
- SVM  
- Naive Bayes  
- Decision Tree  
- **Random Forest** ← selected as final model  
- XGBoost  

Random Forest gave the best results and passed 5-fold cross-validation. The model and label encoder are saved as `.pkl` files using `joblib`.

Key features by importance: Glucose, Hemoglobin, Cholesterol, Creatinine.

---

## App Features

- **Add Patient** — enter name, DOB (auto-calculates age), gender, email, and blood values. Validates email format. Age is read-only and auto-filled.  
- **View Patients** — table view of all records  
- **Update Patient** — fetch by ID, edit values, re-run prediction  
- **Delete Patient** — remove record by ID  
- **AI Remark** — auto-generated explanation shown alongside the disease prediction

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/pranali1911/ai-health-prediction
cd ai-health-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```

Make sure `disease_prediction_model.pkl` and `label_encoder.pkl` are in the same folder as `app.py`. If not, run `train_model.py` first to generate them.

---

## Requirements

```
streamlit
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
joblib
```

---

## Project Structure

```
├── app.py                        # Streamlit UI + CRUD logic
├── train_model.py                # EDA + model training script
├── disease_prediction_model.pkl  # Trained Random Forest model
├── label_encoder.pkl             # LabelEncoder for disease names
├── patients.db                   # SQLite database (auto-created)
├── laboratory__data.csv          # Dataset (download from Kaggle)
└── README.md
```

---

## Disease Predictions Supported

| Label | Disease |
|---|---|
| 0 | Anemia |
| 1 | Asthma |
| 2 | Cardiovascular Disease |
| 3 | Diabetes |
| 4 | Heart Attack |
| 5 | Infection |
| 6 | Kidney Disease |
| 7 | Liver Disease |
| 8 | Pancreatitis |

---

## Sample Prediction

Input:
```
Gender: Male | Age: 59 | Glucose: 96 | Hemoglobin: 6 | Cholesterol: 227
```

Output:
```
Predicted Disease: Anemia
Remark: Low hemoglobin detected. Possible anemia risk.
```

---

## Author

**Pranali Rahangdale**  
MCA Graduate | AI/ML & Full Stack Developer  
📧 prahangdale868@gmail.com  
🔗 [GitHub](https://github.com/pranali1911)

---

> Dataset used under CC0 Public Domain License from Kaggle.
