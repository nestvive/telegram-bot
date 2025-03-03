from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN}")  # Debugging 输出
