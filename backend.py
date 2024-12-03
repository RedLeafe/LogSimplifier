from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import jsonlines
from dotenv import load_dotenv

load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

JSONL_FILE_PATH = "dataset.jsonl"

class AlertRequest(BaseModel):
    alert: str

def load_knowledge_base(file_path):
    knowledge_base = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            knowledge_base.append(obj)
    return knowledge_base

def retrieve_relevant_info(alert: str, knowledge_base):
    relevant_info = []
    for entry in knowledge_base:
        user_message = entry["messages"][0]["content"]
        
        if any(keyword.lower() in user_message.lower() for keyword in alert.split()):
            assistant_message = entry["messages"][1]["content"]
            relevant_info.append(assistant_message)
    
    return relevant_info

@app.post("/simplify-alert")
async def simplify_alert(request: AlertRequest):
    alert_data = request.alert
    if alert_data:
        knowledge_base = load_knowledge_base(JSONL_FILE_PATH)
        
        retrieved_info = retrieve_relevant_info(alert_data, knowledge_base)
        
        prompt_message = "Simplify the following log entry in plain language for non-experts. Make it only one sentence, include number of attempts, IP addresses, who did it, and if it was suspicious or not."
        context = "\n".join(retrieved_info)
        full_prompt = f"{prompt_message}\n\nAlert: {alert_data}\n\nRelevant Information:\n{context}"

        response = openai.chat.completions.create(
            model=os.getenv('FINE_TUNED_MODEL'),
            messages=[{"role": "system", "content": prompt_message},
                      {"role": "user", "content": full_prompt}],
            max_tokens=100,
            temperature=0,
            top_p=1
        )

        simplified_log = response.choices[0].message.content.strip()
        return {"simplified_log": simplified_log}
    else:
        return {"error": "No alert provided"}
