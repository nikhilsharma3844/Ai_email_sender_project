import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_email_with_groq(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful email assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "llama3-70b-8192"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions",headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"
