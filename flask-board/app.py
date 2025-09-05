from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# DB 초기화 (테이블 없으면 생성)
# 기존 sqlite3 기반은 유지하되, SQLAlchemy로 교체
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, Text, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
	# Fallback to local SQLite when not provided
	DATABASE_URL = "sqlite:///board.db"

en = create_engine(DATABASE_URL.replace("postgresql+psycopg2", "postgresql+psycopg"), future=True)
SessionLocal = sessionmaker(bind=en, autoflush=False, autocommit=False, future=True)

metadata = MetaData()
posts_table = Table(
	"posts",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("title", String, nullable=False),
	Column("content", Text, nullable=False),
	Column("author", String, nullable=True),
	Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
)

# 테이블 생성 (DB에 맞춰 이식성 있게 생성)
metadata.create_all(bind=en)

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

@app.route("/healthz")
def healthz():
	try:
		with en.connect() as conn:
			conn.execute(text("SELECT 1"))
		return ("ok", 200)
	except Exception:
		return ("unhealthy", 500)

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id: int):
	with en.begin() as conn:
		conn.execute(text("DELETE FROM posts WHERE id = :id"), {"id": post_id})
	return redirect("/")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
