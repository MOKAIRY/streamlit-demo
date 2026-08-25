import streamlit as st

st.title("BMI Calculator")

with st.form("bmi_calculator"):
    weight = st.number_input("Enter your weight (kg)", min_value=0.0)
    height = st.number_input("Enter your height (m)", min_value=0.0)
    
    submitted = st.form_submit_button("Calculate BMI")
    
    if submitted and height > 0:
        bmi = weight / (height ** 2)
        st.write(f"Your BMI is: {bmi:.2f}")
        
        # Determine BMI category
        if bmi < 18.5:
            st.warning("You are underweight")
        elif bmi < 25:
            st.success("You have a normal weight")
        elif bmi < 30:
            st.warning("You are overweight")
        else:
            st.error("You are obese")
            
        # Display BMI chart
        st.markdown("""
        ### BMI Categories:
        - Underweight: < 18.5
        - Normal weight: 18.5 - 24.9
        - Overweight: 25 - 29.9
        - Obese: ≥ 30
        """)
