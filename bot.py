from flask import Flask, request
import os
import time
import threading
import requests

# === 你的 Telegram Bot 配置 ===
TOKEN = 8143371310:AAEYrgXF6uxRFy0y9HgVVcn4kq2k5FRu7xA
CHAT_ID = 1344678579

# === 你的 Notion API 配置 ===
NOTION_API_KEY = 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
NOTION_DATABASE_ID = "1ace10bf08f2801b9da0d265aabee5e8"


# === 任务列表 ===
TASKS = ["✅ 处理供应链对接", "✅ 拍摄小红书素材", "✅ 远程管理团队"]

app = Flask(__name__)

# === 定时推送每日任务 ===
def send_daily_tasks():
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == "09:00":  # 每天 9:00 AM 推送任务
            message = "🌟 **今日任务清单** 🌟\n\n" + "\n".join(TASKS) + "\n\n完成后请回复 ✅"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
        time.sleep(60)  # 每分钟检查一次

# === Telegram 交互 ===
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if "message" in update and "text" in update["message"]:
        user_text = update["message"]["text"]
        if user_text == "✅":
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          data={"chat_id": CHAT_ID, "text": "🎉 任务完成，已记录！AI 会调整后续安排"})
            update_notion_task("今日任务", "完成")  # 自动更新 Notion
    return "OK", 200

# === Notion 任务同步 ===
def update_notion_task(task_name, status):
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "任务名称": {"title": [{"text": {"content": task_name}}]},
            "状态": {"select": {"name": status}}
        }
    }
    requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

# === 启动 Flask 服务器 ===
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=send_daily_tasks).start()
    app.run(host='0.0.0.0', port=port)
