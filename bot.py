from flask import Flask, request
import os
import requests

app = Flask(__name__)

TOKEN = "8143371310:AAEYrgXF6uxRFy0y9HgVVcn4kq2k5FRu7xA"  # 这里换成你的 Telegram Bot Token

@app.route('/', methods=['GET'])
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json  # 解析 Telegram 发来的 JSON
    print(update)  # 打印日志，确保服务器收到了消息

    # 解析消息数据
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # 发送一个简单的回复
        send_message(chat_id, f"你说了: {text}")

    return "OK", 200

def send_message(chat_id, text):
    """ 发送消息到 Telegram """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
