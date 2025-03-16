from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Load credentials from environment variables
WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/634957356359676/messages"
ACCESS_TOKEN = "EAANj8m0V4WIBOyOmgSGdcVfjwjmMYSGGFl4kIt8PxAggcrFcInxHZBOZCPYp0UkLZCRwvFMhQGE77ZCBjmbV0VZCFbm1PBE0woDie8DCU5P0pq6vUQNnfXGF1ddk2y4N6oh2S3vZBo42GPLEZCqYu3wFMvaoqSAn1865ugeQ6LuqZBZB9q3hKieVTY2qpeC5s0NRZBhF6ZCurM1hWjJI1ml7v8FYjxTdQidTv10tvgZD"

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
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    requests.post(WHATSAPP_API_URL, json=data, headers=headers)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "messages" in data:
        for message in data["messages"]:
            if "type" in message and message["type"] == "document":
                doc_url = message["document"]["link"]
                send_message(message["from"], f"Received your file! Downloading: {doc_url}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render requires a dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
