
import streamlit as st
import requests

API_URL = "https://response-predictor-50046884446.development.catalystappsail.in"
PREDICT_URL = f"{API_URL}/predict"

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="💰",
    layout="centered"
)

st.title("Insurance Premium Predictor")
st.markdown("Enter your details below")

age = st.number_input("Age", min_value=1, max_value=119, value=30)

weight = st.number_input("Weight (kg)", min_value=0.1, value=65.0)

height = st.number_input("Height in cm", min_value=1, value=170)

income_lpa = st.number_input(
    "Your income (LPA)",
    min_value=0.1,
    value=5.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    options=[True, False],
    format_func=lambda x: "Yes" if x else "No"
)

city = st.text_input("Enter your city", value="Mumbai")

occupation = st.selectbox(
    "Occupation",
    options=[
        "unemployed",
        "retired",
        "private_job",
        "business_owner",
        "government_job",
        "self_employed"
    ]
)

if st.button("Predict Premium Category", type="primary"):

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
        with st.spinner("Predicting insurance premium..."):
            response = requests.post(
                PREDICT_URL,
                json=input_data,
                timeout=30
            )

        response.raise_for_status()
        result = response.json()

        st.success("Prediction completed successfully!")

        if "response" in result:
            st.subheader("Prediction Result")
            st.success(
                f"Insurance Premium Category: {result['response']}"
            )
        else:
            st.subheader("API Response")
            st.json(result)

    except requests.exceptions.HTTPError:
        st.error(
            f"API Error: {response.status_code} - {response.text}"
        )

    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to backend: {e}")

    except ValueError:
        st.error("Backend returned an invalid JSON response.")
