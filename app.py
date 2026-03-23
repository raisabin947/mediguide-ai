from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔑 Put your API key here
API_KEY = "YOUR_OPENAI_API_KEY"

def get_ai_response(symptoms):

    prompt = f"""
You are a healthcare assistant.
User symptoms: {symptoms}

Give response in this format:

Possible Causes:
Precautions:
Home Care Tips:
When to See a Doctor:

Keep it simple and safe.
Do not give medical diagnosis.
"""

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    symptoms = request.json["symptoms"]

    ai_response = get_ai_response(symptoms)

    return jsonify({"response": ai_response})


if __name__ == "__main__":
    app.run(debug=True)
