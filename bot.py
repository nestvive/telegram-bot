import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ 读取环境变量
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # ✅ 你的 Telegram 用户 ID
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# ✅ Telegram API 网址
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
NOTION_API_URL = f"https://api.notion.com/v1/pages"

# ✅ 主页测试
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

# ✅ 处理 Telegram Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("收到消息:", data)  # ✅ 方便调试

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # ✅ 处理 "/start" 命令
        if text == "/start":
            send_message(chat_id, "你好！欢迎使用 ViveLume 助理 Bot！")

        # ✅ 记录到 Notion
        record_to_notion(text)

        # ✅ 发送回显消息
        send_message(chat_id, f"你说了: {text}")

    return jsonify({"status": "ok"}), 200

# ✅ 发送 Telegram 消息
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(TELEGRAM_API_URL, json=payload)

# ✅ 记录到 Notion 数据库
def record_to_notion(text):
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": text}}]}
        }
    }
    response = requests.post(NOTION_API_URL, json=data, headers=headers)
    print("Notion API 响应:", response.json())  # ✅ 调试日志

# ✅ 启动 Flask 服务器
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
