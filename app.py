import os
import joblib
import streamlit as st

st.set_page_config(page_title="Source Code Vulnerability Classifier", page_icon="logo.png", layout="wide")

@st.cache_resource
def load_artifacts():
    model = joblib.load("models/model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_artifacts()

col_logo, col_text = st.columns([1, 6])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=95)
with col_text:
    st.title("Source Code Vulnerability Classifier")
    st.caption("Machine Learning System for Vulnerability Detection in Python and C++ Snippets")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Source Code Input")
    source_code = st.text_area(
        "Enter Code Snippet:",
        height=260,
        placeholder="Enter C++ or Python code snippet..."
    )
    analyze_btn = st.button("Run Vulnerability Scan")

with col2:
    st.subheader("Classification Output")
    if analyze_btn and source_code.strip():
        features = vectorizer.transform([source_code])
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = max(probabilities) * 100

        if prediction == "Safe":
            st.success(f"Status: {prediction}")
        else:
            st.error(f"Status: {prediction}")
            
        st.write(f"Confidence: {confidence:.2f}%")
        
        st.write("---")
        st.write("Probability Distribution:")
        classes = model.classes_
        for label, prob in zip(classes, probabilities):
            st.write(f"- {label}: {prob * 100:.1f}%")

    elif analyze_btn:
        st.warning("Please enter a valid code snippet.")
