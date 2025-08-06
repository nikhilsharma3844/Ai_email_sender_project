from django.shortcuts import render
from django.http import JsonResponse,HttpResponseNotAllowed
import smtplib
from email.mime.text import MIMEText
import os, json, requests
from dotenv import load_dotenv
from emailapp.groq_utils import generate_email_with_groq

load_dotenv()
print(os.getenv("GROQ_API_KEY"))
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def index(request):
    return render(request, 'index.html')




def generate_email_with_groq(prompt):
    headers = {
        "Authorization": f"Bearer {'GROQ_API_KEY'}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful email assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "llama3-70b-8192",  # Groq model
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions",headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"


def generate_email(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        prompt = data.get("prompt", "")
        email_text = generate_email_with_groq(prompt)
        return JsonResponse({"email": email_text})

    return HttpResponseNotAllowed(['POST'], 'This endpoint only supports POST requests.')
    








def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipients = data.get("recipients", [])
        email_body = data.get("emailBody", "")
        subject = "AI Generated Email"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                for recipient in recipients:
                    msg = MIMEText(email_body)
                    msg['Subject'] = subject
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = recipient
                    server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

print("Using GROQ API KEY:", os.getenv("GROQ_API_KEY"))
print("Loaded API Key:",GROQ_API_KEY)
