import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    print("Received update:", update)  # 方便 Debug，检查收到的 Telegram 数据
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway 默认用 8080
    app.run(host="0.0.0.0", port=port, debug=True)

