import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model and scaler
@st.cache_resource
def load_model():
    model = joblib.load('breast_cancer_ensemble_model.pkl')
    scaler = joblib.load('scaler.pkl')
    return model, scaler

model, scaler = load_model()

# App title
st.title("Breast Cancer Prediction")
st.markdown("### Enter patient tumor measurements below")

# Create two columns for better layout
col1, col2 = st.columns(2)

# Input fields (30 features)
with col1:
    radius_mean = st.number_input("Radius Mean", min_value=0.0, value=14.0)
    texture_mean = st.number_input("Texture Mean", min_value=0.0, value=19.0)
    perimeter_mean = st.number_input("Perimeter Mean", min_value=0.0, value=90.0)
    area_mean = st.number_input("Area Mean", min_value=0.0, value=600.0)
    smoothness_mean = st.number_input("Smoothness Mean", min_value=0.0, value=0.1)
    compactness_mean = st.number_input("Compactness Mean", min_value=0.0, value=0.1)
    concavity_mean = st.number_input("Concavity Mean", min_value=0.0, value=0.08)
    concave_points_mean = st.number_input("Concave Points Mean", min_value=0.0, value=0.05)
    symmetry_mean = st.number_input("Symmetry Mean", min_value=0.0, value=0.18)
    fractal_dimension_mean = st.number_input("Fractal Dimension Mean", min_value=0.0, value=0.06)

with col2:
    radius_se = st.number_input("Radius SE", min_value=0.0, value=0.4)
    texture_se = st.number_input("Texture SE", min_value=0.0, value=1.2)
    perimeter_se = st.number_input("Perimeter SE", min_value=0.0, value=3.0)
    area_se = st.number_input("Area SE", min_value=0.0, value=40.0)
    smoothness_se = st.number_input("Smoothness SE", min_value=0.0, value=0.007)
    compactness_se = st.number_input("Compactness SE", min_value=0.0, value=0.03)
    concavity_se = st.number_input("Concavity SE", min_value=0.0, value=0.03)
    concave_points_se = st.number_input("Concave Points SE", min_value=0.0, value=0.01)
    symmetry_se = st.number_input("Symmetry SE", min_value=0.0, value=0.02)
    fractal_dimension_se = st.number_input("Fractal Dimension SE", min_value=0.0, value=0.004)

with col1:
    radius_worst = st.number_input("Radius Worst", min_value=0.0, value=16.0)
    texture_worst = st.number_input("Texture Worst", min_value=0.0, value=25.0)
    perimeter_worst = st.number_input("Perimeter Worst", min_value=0.0, value=110.0)
    area_worst = st.number_input("Area Worst", min_value=0.0, value=800.0)
    smoothness_worst = st.number_input("Smoothness Worst", min_value=0.0, value=0.13)
    compactness_worst = st.number_input("Compactness Worst", min_value=0.0, value=0.25)
    concavity_worst = st.number_input("Concavity Worst", min_value=0.0, value=0.25)
    concave_points_worst = st.number_input("Concave Points Worst", min_value=0.0, value=0.15)

with col2:
    symmetry_worst = st.number_input("Symmetry Worst", min_value=0.0, value=0.3)
    fractal_dimension_worst = st.number_input("Fractal Dimension Worst", min_value=0.0, value=0.08)

# Predict button
if st.button("Predict Cancer Type"):
    # Create feature array
    features = np.array([[radius_mean, texture_mean, perimeter_mean, area_mean,
                         smoothness_mean, compactness_mean, concavity_mean, concave_points_mean,
                         symmetry_mean, fractal_dimension_mean,
                         radius_se, texture_se, perimeter_se, area_se,
                         smoothness_se, compactness_se, concavity_se, concave_points_se,
                         symmetry_se, fractal_dimension_se,
                         radius_worst, texture_worst, perimeter_worst, area_worst,
                         smoothness_worst, compactness_worst, concavity_worst, concave_points_worst,
                         symmetry_worst, fractal_dimension_worst]])
    
    # Scale and predict
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]
    
    # Display result
    if prediction == 1:
        st.error("Malignant (Cancerous)")
        st.warning(f"Confidence: {probability[1]:.2%}")
    else:
        st.success("Benign (Non-Cancerous)")
        st.info(f"Confidence: {probability[0]:.2%}")

# Footer
st.markdown("---")
st.markdown("**Model**: Ensemble (LGBM + RF + DT + KNN) | Accuracy: 98.25% on test set")