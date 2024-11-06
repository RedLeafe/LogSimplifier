from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv('.env')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

st.title("Log Simplifier For Non Experts")

user_input = st.text_area("Enter your log:")

if st.button("Simplify!"):
    if user_input:
        prompt_message = "Simplify the following log entry in plain language for non-experts. Make it only one sentence, include number of attempts, IP addresses, who did it, and if it was suspicious or not."
        messages = [
            {"role": "system", "content": prompt_message},
            {"role": "user", "content": user_input}
        ]
        response = client.chat.completions.create(
            model=os.getenv('FINE_TUNED_MODEL'),  
            messages=messages,
            max_tokens=100,
            temperature=0,
            top_p=1
        )
        simplified_log = response.choices[0].message.content.strip()
        st.text_area("Simplified Log:", value=simplified_log, height=200)
    else:
        st.write("Enter Here.")