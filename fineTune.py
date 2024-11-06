from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv('.env')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    with open("dataset.jsonl", "rb") as file:
        response = client.files.create(file=file, purpose='fine-tune')
        training_file_id = response.id
    print(f"File uploaded successfully. File ID: {training_file_id}")
except Exception as e:
    print(f"File upload failed: {e}")
    exit()

try:
    response = client.fine_tuning.jobs.create(
        training_file=training_file_id, 
        model="gpt-4o-mini-2024-07-18", 
        hyperparameters={
            "n_epochs": 15,
            "batch_size": 3,
            "learning_rate_multiplier": 0.3
        }
    )
    job_id = response.id
    status = response.status
    print(f'Fine-tuning model with jobID: {job_id}.')
    print(f"Training Response: {response}")
    print(f"Training Status: {status}")
except Exception as e:
    print(f"Fine-tuning job creation failed: {e}")
    exit()

# Polling for Job Completion
status = client.fine_tuning.jobs.retrieve(job_id).status
if status not in ["succeeded", "failed"]:
    print(f"Job not in terminal status: {status}. Waiting.")
    while status not in ["succeeded", "failed"]:
        time.sleep(10)
        status = client.fine_tuning.jobs.retrieve(job_id).status
        print(f"Status: {status}")
else:
    print(f"Fine-tune job {job_id} finished with status: {status}")

# List All Fine-Tuning Jobs
try:
    result = client.fine_tuning.jobs.list()
    print(f"Found {len(result.data)} fine-tune jobs.")
except Exception as e:
    print(f"Failed to list fine-tune jobs: {e}")