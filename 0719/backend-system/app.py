import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "postgres-db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password123")
DB_NAME = os.getenv("DB_NAME", "intro_project")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def init_system_db():
    """初始化核心系統資料庫：建立使用者帳號表"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """
    )
    # 建立一組預設的登入系統帳密
    cur.execute("SELECT * FROM users WHERE username = 'admin';")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);",
            ("admin", "admin123"),
        )
    conn.commit()
    cur.close()
    conn.close()


init_system_db()


@app.route("/api/system/login", methods=["POST"])
def login():
    """共用的系統登入 API"""
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT username FROM users WHERE username = %s AND password = %s;",
        (username, password),
    )
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "系統登入成功！",
                    "token": "mock-jwt-token-xyz",
                }
            ),
            200,
        )
    return (
        jsonify({"status": "fail", "message": "密碼錯誤或使用者不存在"}),
        401,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)