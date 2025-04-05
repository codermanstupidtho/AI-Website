import subprocess
import sys
import os

try:
    import ollama
except ImportError:
    print("Error: Ollama is not installed. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
    import ollama

try:
    import pyttsx3
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
    import pyttsx3

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MODEL = "tinyllama"
speaker = pyttsx3.init()

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

def chat_with_ai(message):
    try:
        response = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": "You're a friendly and helpful AI assistant."},
            {"role": "user", "content": message}
        ])
        reply = response["message"]["content"] if "message" in response else "No response from model."
        speak(reply)
        return reply
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_input = data.get("message", "")
    print(f"User said: {user_input}")
    reply = chat_with_ai(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
