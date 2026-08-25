import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("iris_model.pkl")

st.title("Iris Flower Classifier")

st.write("Enter flower measurements to predict the species.")

# Input fields
sepal_length = st.number_input("Sepal length (cm)", min_value=0.0)
sepal_width = st.number_input("Sepal width (cm)", min_value=0.0)
petal_length = st.number_input("Petal length (cm)", min_value=0.0)
petal_width = st.number_input("Petal width (cm)", min_value=0.0)

# Prediction button
if st.button("Predict"):
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(features)[0]
    species = ["Setosa", "Versicolor", "Virginica"][prediction]

    st.success(f"Predicted Species: **{species}**")
