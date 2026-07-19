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

# 從 docker-compose 環境變數動態讀取各自的資料表名稱
TABLE_NAME = os.getenv("TABLE_NAME", "member_intro_default")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def init_member_db():
    """初始化個人資料表，塞入預設的自我介紹內容"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            bio TEXT,
            skills TEXT
        );
    """
    )
    cur.execute(f"SELECT * FROM {TABLE_NAME};")
    if not cur.fetchone():
        cur.execute(
            f"INSERT INTO {TABLE_NAME} (name, bio, skills) VALUES (%s, %s, %s);",
            (
                f"我是成員 ({TABLE_NAME})",
                "這是我的自我介紹內容...",
                "Python, Flask, Docker",
            ),
        )
    conn.commit()
    cur.close()
    conn.close()


init_member_db()


@app.route("/api/intro", methods=["GET"])
def get_intro():
    """獲取個人自我介紹"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT name, bio, skills FROM {TABLE_NAME} LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return (
            jsonify({"name": row[0], "bio": row[1], "skills": row[2]}),
            200,
        )
    return jsonify({"message": "找不到資料"}), 404


@app.route("/api/intro", methods=["PUT"])
def update_intro():
    """更新個人自我介紹"""
    data = request.json or {}
    name = data.get("name")
    bio = data.get("bio")
    skills = data.get("skills")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE {TABLE_NAME} SET name = %s, bio = %s, skills = %s;",
        (name, bio, skills),
    )
    conn.commit()
    cur.close()
    conn.close()
    return (
        jsonify({"status": "success", "message": f"{TABLE_NAME} 更新成功！"}),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)