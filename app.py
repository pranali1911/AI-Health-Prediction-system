
import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import date

# =================================
# DATABASE CONNECTION
# =================================
conn = sqlite3.connect("patients.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    dob TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT,
    glucose REAL,
    hemoglobin REAL,
    cholesterol REAL,
    prediction TEXT,
    remarks TEXT
)
""")

conn.commit()


# =================================
# FUNCTIONS
# =================================

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def calculate_age(dob):
    today = date.today()

    age = today.year - dob.year - (
        (today.month, today.day) <
        (dob.month, dob.day)
    )

    return age


# =================================
# AI PREDICTION
# =================================
def predict_disease(gender, age, glucose, hemoglobin, cholesterol):

    # Anemia
    if hemoglobin < 11:
        disease = "Anemia"
        remark = "Low hemoglobin detected. Possible anemia risk."

    # Diabetes
    elif glucose >= 126:
        disease = "Diabetics"
        remark = "High glucose level detected. Diabetes risk present."

    # Heart Attack
    elif cholesterol >= 240:
        disease = "Heart Attack"
        remark = "High cholesterol level. Increased cardiac risk."

    # Asthma
    elif (
        gender == "Male"
        and age >= 70
        and hemoglobin >= 35
        and glucose <= 100
    ):
        disease = "Asthma"
        remark = "Pattern indicates possible asthma."

    # Infection
    elif (
        gender == "Female"
        and 20 <= age <= 35
        and 11 <= hemoglobin <= 15
        and 220 <= cholesterol <= 230
    ):
        disease = "Infection"
        remark = "Possible infection risk detected."

    # Liver Disease
    elif (
        gender == "Male"
        and age >= 50
        and hemoglobin >= 15
        and 200 <= cholesterol <= 230
        and glucose <= 100
    ):
        disease = "Liver Disease"
        remark = "Blood values indicate possible liver disorder."

    else:
        disease = "Normal"
        remark = "Blood parameters are within normal range."

    return disease, remark


# =================================
# PAGE CONFIG
# =================================
st.set_page_config(
    page_title="AI Health Prediction System",
    layout="wide"
)

st.title("🩺 AI Health Prediction System")

menu = st.sidebar.radio(
    "Menu",
    [
        "Add Patient",
        "View Patients",
        "Update Patient",
        "Delete Patient"
    ]
)


# =================================
# ADD PATIENT
# =================================
if menu == "Add Patient":

    st.subheader("Add Patient")

    full_name = st.text_input("Full Name")

    from datetime import date

    dob = st.date_input(
    "Date of Birth",
    min_value=date(1900, 1, 1),
    max_value=date.today()
)
            
    # age

    if dob:
        age = calculate_age(dob)
        
        st.text_input("Age",value=str(age),disabled=True)
    else:
        age = ""

    gender = st.selectbox("Gender",["Select Gender", "Male", "Female"])
   
    email_name = st.text_input("Email",placeholder="Enter email")
    email = email_name.strip().lower()
    

    glucose = st.number_input(
        "Glucose",
        min_value=0.0
    )

    hemoglobin = st.number_input(
        "Hemoglobin",
        min_value=0.0
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0
    )

    if st.button("Predict & Save"):

        if full_name == "":
            st.error("Please enter full name.")

        elif not validate_email(email):
            st.error("Please enter a valid email.")

        else:

            disease, remark = predict_disease(
                gender,
                age,
                glucose,
                hemoglobin,
                cholesterol
            )

            c.execute("""
            INSERT INTO patients(
                full_name,
                dob,
                age,
                gender,
                email,
                glucose,
                hemoglobin,
                cholesterol,
                prediction,
                remarks
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                full_name,
                str(dob),
                age,
                gender,
                email,
                glucose,
                hemoglobin,
                cholesterol,
                disease,
                remark
            ))

            conn.commit()

            st.success("Patient Saved Successfully")

            st.info(f"Disease Prediction : {disease}")

            st.warning(f"AI Remark : {remark}")


# =================================
# VIEW PATIENTS
# =================================
elif menu == "View Patients":

    st.subheader("Patient Records")

    df = pd.read_sql(
        "SELECT * FROM patients",conn)

    st.dataframe(df,width='stretch')


# =================================
# UPDATE PATIENT
# =================================
elif menu == "Update Patient":

    st.subheader("Update Patient")

    patient_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1
    )

    if st.button("Fetch"):

        data = c.execute(
            "SELECT * FROM patients WHERE id=?",
            (patient_id,)
        ).fetchone()

        if data:

            email = st.text_input(
                "Email",
                value=data[5]
            )

            glucose = st.number_input(
                "Glucose",
                value=float(data[6])
            )

            hemoglobin = st.number_input(
                "Hemoglobin",
                value=float(data[7])
            )

            cholesterol = st.number_input(
                "Cholesterol", value=float(data[8])
            )

            if st.button("Update Record"):

                disease, remark = predict_disease(
                    data[3],
                    data[2],
                    glucose,
                    hemoglobin,
                    cholesterol
                )

                c.execute("""
                UPDATE patients
                SET
                email=?,
                glucose=?,
                hemoglobin=?,
                cholesterol=?,
                prediction=?,
                remarks=?
                WHERE id=?
                """,
                (
                    email,
                    glucose,
                    hemoglobin,
                    cholesterol,
                    disease,
                    remark,
                    patient_id
                ))

                conn.commit()

                st.success("Updated Successfully")

        else:
            st.error("Patient ID not found.")


# =================================
# DELETE PATIENT
# =================================
elif menu == "Delete Patient":

    st.subheader("Delete Patient")

    patient_id = st.number_input(
        "Patient ID",min_value=1,step=1
    )

    if st.button("Delete"):

        c.execute(
            "DELETE FROM patients WHERE id=?",(patient_id,))

        conn.commit()

        st.success("Deleted Successfully")

