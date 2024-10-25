import pickle
import streamlit as st
import pandas as pd
import xgboost
import numpy as np

# loading the saved model
loaded_model = xgboost.Booster()
loaded_model.load_model('xgb_model.bin')

# page title and header
st.markdown("<h1 style='text-align: center; color: #ff4757;'>Heart Attack Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #333;'>Check your risk of heart attack by entering some key health metrics</p>", unsafe_allow_html=True)

# hero section with image
st.markdown(
    f'<div style="text-align: center;"><img src="https://media.tenor.com/91scJf-xrKEAAAAi/emoji-coraz%C3%B3n-humano.gif" width="200"></div>', 
    unsafe_allow_html=True,
)

# Form inputs (mimicking your HTML form structure)

age = st.number_input('Enter age', step=1)

sex = st.selectbox('Enter sex', ('Male', 'Female'))
sex = 1 if sex == 'Male' else 0

st.write("Chest Pain type \n\n Value 0: Typical Angina \n\n Value 1: Atypical Angina \n\n Value 2: Non-Anginal Pain \n\n Value 3: Asymptomatic")
cp = st.selectbox('Enter Chest Pain type', (0, 1, 2, 3))

trtbps = st.number_input('Enter resting blood pressure value (in mm Hg)', step=1)

chol = st.number_input('Enter cholesterol value (mg/dl)', step=1)

fbs = st.selectbox('Is fasting blood sugar > 120 mg/dl?', ('Yes', 'No'))
fbs = 1 if fbs == 'Yes' else 0

st.write("Resting Electrocardiographic Results \n\n Value 0: Normal \n\n Value 1: ST-T wave abnormality \n\n Value 2: Left ventricular hypertrophy")
restecg = st.selectbox('Enter Resting Electrocardiographic Results', (0, 1, 2))

thalachh = st.number_input('Enter maximum heart rate achieved (bpm)', step=1)

exng = st.selectbox('Do you experience exercise-induced angina?', ('Yes', 'No'))
exng = 1 if exng == 'Yes' else 0

oldpeak = st.number_input('Enter oldpeak (ST depression caused by activity compared to rest)', step=0.01)

st.write("Slope of the peak exercise ST segment — \n\n 0: Downsloping \n\n 1: Flat \n\n 2: Upsloping")
slp = st.selectbox('Enter slope of the peak exercise ST segment', (0, 1, 2))

caa = st.selectbox('Enter number of major vessels (0-3) colored by fluoroscopy (caa)', (0, 1, 2, 3))

st.write("Thalassemia Value — \n\n 0: Normal \n\n 1: Fixed Defect \n\n 2: Reversible Defect")
thall = st.selectbox('Enter thalassemia value', (0, 1, 2))

# Prediction button
if st.button('Predict'):
    # Input validation to check if all values are entered
    features_values = {'age': age, 'trtbps': trtbps, 'chol': chol, 'thalachh': thalachh, 'oldpeak': oldpeak}
    
    if any(value == 0 or value == 0.00 for value in features_values.values()):
        st.warning('Please input all the details.')
    else:
        # Prepare data for prediction
        data_1 = pd.DataFrame({'thall': [thall],
                               'caa': [caa],
                               'cp': [cp],
                               'oldpeak': [oldpeak],
                               'exng': [exng],
                               'chol': [chol],
                               'thalachh': [thalachh]
                              })

        dtest = xgboost.DMatrix(data_1)
        prediction = loaded_model.predict(dtest)
        
        # Set threshold to classify heart attack risk
        threshold = 0.5
        prediction = np.where(prediction >= threshold, 1, 0)
        
        # Display results
        if prediction == 0:
            st.markdown("<h2 style='text-align: center; color: green;'>Patient has no risk of Heart Attack</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: red;'>Patient has risk of Heart Attack</h2>", unsafe_allow_html=True)

# Footer section
st.markdown("<footer style='text-align: center; color: #ff4757; margin-top: 20px;'>Heart Attack Predictor © 2024</footer>", unsafe_allow_html=True)