from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# DB 초기화 (테이블 없으면 생성)
# 기존 sqlite3 기반은 유지하되, SQLAlchemy로 교체
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
	# Fallback to local SQLite when not provided
	DATABASE_URL = "sqlite:///board.db"

en = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=en, autoflush=False, autocommit=False, future=True)

# 테이블 생성
# posts (id, title, content, author, created_at)
with en.begin() as conn:
	conn.execute(text(
		"""
		CREATE TABLE IF NOT EXISTS posts (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			title TEXT NOT NULL,
			content TEXT NOT NULL,
			author TEXT,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
		"""
	))

@app.route("/")
def index():
	with en.connect() as conn:
		rows = conn.execute(text("SELECT id, title, content, author, created_at FROM posts ORDER BY id DESC")).all()
	return render_template("index.html", posts=rows)

@app.route("/write", methods=["GET", "POST"])
def write():
	if request.method == "POST":
		title = request.form.get("title", "").strip()
		content = request.form.get("content", "").strip()
		author = request.form.get("author", "").strip() or None
		if not title or not content:
			return redirect("/")
		with en.begin() as conn:
			conn.execute(
				text("INSERT INTO posts (title, content, author) VALUES (:title, :content, :author)"),
				{"title": title, "content": content, "author": author}
			)
		return redirect("/")
	return render_template("write.html")

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id: int):
	with en.begin() as conn:
		conn.execute(text("DELETE FROM posts WHERE id = :id"), {"id": post_id})
	return redirect("/")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
