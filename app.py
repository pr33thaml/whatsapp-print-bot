from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Load credentials from environment variables
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/634957356359676/messages"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Secure access token

@app.route("/")
def home():
    return "✅ WhatsApp Print Bot is Live!"

def send_message(user, text):
    data = {
        "messaging_product": "whatsapp",
        "to": user,
        "type": "text",
        "text": {"body": text}
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(WHATSAPP_API_URL, json=data, headers=headers)
    print(response.json())  # Debugging

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":  # Meta verification step
        mode = request.args.get("hub.mode")
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and verify_token == os.getenv("VERIFY_TOKEN", "whatsapp_bot_verification@123"):
            print(f"Webhook verified successfully! Challenge: {challenge}")
            return challenge, 200  # Must return plain text response

        print("Webhook verification failed!")
        return "Verification failed", 403

    elif request.method == "POST":  # Handling incoming messages
        data = request.get_json()
        print("🔹 Full Incoming Data:", data)  # <-- ADDED LOGGING

        try:
            messages = data["entry"][0]["changes"][0]["value"]["messages"]
            print("✅ Extracted Messages:", messages)  # <-- ADDED LOGGING

            for message in messages:
                if message["type"] == "text":
                    text = message["text"]["body"]
                    sender = message["from"]
                    print(f"📩 Received message from {sender}: {text}")  # <-- ADDED LOGGING
                    send_message(sender, f"Echo: {text}")  # Send a response
                    
                elif message["type"] == "document":
                    doc_url = message["document"]["link"]
                    sender = message["from"]
                    print(f"📄 Received document from {sender}: {doc_url}")  # <-- ADDED LOGGING
                    send_message(sender, f"✅ Received your file! Downloading: {doc_url}")

        except KeyError:
            print("⚠️ No valid messages found in the request")

        return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render requires a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
