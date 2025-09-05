from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# DB 초기화 (테이블 없으면 생성)
def init_db():
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect("board.db")
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = sqlite3.connect("board.db")
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("write.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
