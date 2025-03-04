import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # 让 Flask 监听 Railway 分配的端口
    app.run(host="0.0.0.0", port=port, debug=True)
