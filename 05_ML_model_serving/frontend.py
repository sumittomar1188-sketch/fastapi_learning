
import streamlit as st
import requests

app_url = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Predictor")
st.markdown("Enter your details below")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)

weight = st.number_input("Weight", min_value=0.1, value=65.0)

height = st.number_input("Height in cm", min_value=1, value=170)

income_lpa = st.number_input(
    "Your income (LPA)",
    min_value=0.1,
    value=5.0
)

smoker = st.selectbox(
    "Are you smoker?",
    options=[True, False]
)

city = st.text_input("Enter your city", value="Mumbai")

occupation = st.selectbox(
    "Occupation",
    options=[
        'unemployed',
        'retired',
        'private_job',
        'business_owner',
        'government_job',
        'self_employed'
    ]
)

if st.button("Predict Premium Category"):

    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(app_url, json=input_data)

        if response.status_code == 201:

            result = response.json()

            st.success(
                f"Predicted Insurance Premium Category: {result['response']}"
            )

        else:
            st.error(
                f"API Error: {response.status_code} - {response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to FastAPI server.")
   