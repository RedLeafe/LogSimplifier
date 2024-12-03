import streamlit as st
import requests

st.title("IDS Alert Simplifier For Non Experts")

user_input = st.text_area("Enter your alert:")

if st.button("Simplify!"):
    if user_input:
        response = requests.post("http://localhost:8000/simplify-alert", json={"alert": user_input})

        if response.status_code == 200:
            simplified_log = response.json().get("simplified_log", "No simplified log returned.")
            st.text_area("Simplified Log:", value=simplified_log, height=200)
        else:
            st.write("Error: Could not process the alert.")
    else:
        st.write("Please enter an alert.")
