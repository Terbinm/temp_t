import os
from flask import Flask
from dotenv import load_dotenv  # 匯入 load_dotenv
from routes import main_bp

# 載入 .env 檔案
load_dotenv()


def create_app():
    app = Flask(__name__)

    # --- 在終端機列印出環境變數 ---
    secret_key = os.getenv('MY_SECRET_KEY')
    db_url = os.getenv('DATABASE_URL')

    print(f"DEBUG: 讀取到的 SECRET_KEY 為: {secret_key}")
    print(f"DEBUG: 讀取到的 DATABASE_URL 為: {db_url}")
    # -----------------------------

    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)