from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    print(update)  # 先打印出来看看收到什么
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Railway 分配的端口
    app.run(host='0.0.0.0', port=port, debug=True)
