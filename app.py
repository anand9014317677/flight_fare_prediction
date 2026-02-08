import streamlit as st
import pandas as pd
import joblib
import gdown
import os

st.title("Flight Fare Prediction")

# -------------------------
# Download model from Google Drive
# -------------------------
model_url = "https://drive.google.com/uc?id=1RWeh8crNREKgWizx_Z3XgvBffHnuZfJ9"
model_path = "model.pkl"

if not os.path.exists(model_path):
    st.write("Downloading model...")
    gdown.download(model_url, model_path, quiet=False)

model = joblib.load(model_path)

# -------------------------
# MODEL COLUMNS
# -------------------------
model_columns = [
'Total_Stops','Journey_Day','Journey_Month','Dep_Hour','Dep_Min',
'Arrival_Hour','Arrival_Min','Duration_Hours','Duration_Mins',
'Airline_Air India','Airline_GoAir','Airline_IndiGo',
'Airline_Jet Airways','Airline_Jet Airways Business',
'Airline_Multiple carriers',
'Airline_Multiple carriers Premium economy',
'Airline_SpiceJet','Airline_Trujet','Airline_Vistara',
'Airline_Vistara Premium economy',
'Source_Chennai','Source_Delhi','Source_Kolkata','Source_Mumbai',
'Destination_Cochin','Destination_Delhi','Destination_Hyderabad',
'Destination_Kolkata','Destination_New Delhi'
]

st.subheader("Flight Details")

total_stops = st.selectbox("Total Stops", [0,1,2,3])
journey_day = st.slider("Journey Day", 1, 31)
journey_month = st.slider("Journey Month", 1, 12)

dep_hour = st.slider("Departure Hour", 0, 23)
dep_min = st.slider("Departure Minute", 0, 59)

arrival_hour = st.slider("Arrival Hour", 0, 23)
arrival_min = st.slider("Arrival Minute", 0, 59)

duration_hours = st.number_input("Duration Hours", 0, 24)
duration_mins = st.number_input("Duration Minutes", 0, 59)

airline = st.selectbox("Airline", [
"Air India","GoAir","IndiGo","Jet Airways",
"Jet Airways Business","Multiple carriers",
"Multiple carriers Premium economy",
"SpiceJet","Trujet","Vistara","Vistara Premium economy"
])

source = st.selectbox("Source",
["Chennai","Delhi","Kolkata","Mumbai"])

destination = st.selectbox("Destination",
["Cochin","Delhi","Hyderabad","Kolkata","New Delhi"])

if st.button("Predict Fare"):

    input_data = dict.fromkeys(model_columns, 0)

    input_data['Total_Stops'] = total_stops
    input_data['Journey_Day'] = journey_day
    input_data['Journey_Month'] = journey_month
    input_data['Dep_Hour'] = dep_hour
    input_data['Dep_Min'] = dep_min
    input_data['Arrival_Hour'] = arrival_hour
    input_data['Arrival_Min'] = arrival_min
    input_data['Duration_Hours'] = duration_hours
    input_data['Duration_Mins'] = duration_mins

    input_data[f'Airline_{airline}'] = 1
    input_data[f'Source_{source}'] = 1
    input_data[f'Destination_{destination}'] = 1

    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)

    st.success(f"Estimated Flight Fare: ₹{int(prediction[0])}")