from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])  
def webhook():
    update = request.json
    print(update)  # 先打印更新数据，确认是否有消息收到
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)  
