from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# DB 초기화 (테이블 없으면 생성)
# 기존 sqlite3 기반은 유지하되, SQLAlchemy로 교체
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, Text, String, TIMESTAMP, func, UniqueConstraint
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

users_table = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("username", String, nullable=False),
	Column("password_hash", String, nullable=False),
	Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
	UniqueConstraint("username", name="uq_users_username"),
)

# 테이블 생성 (DB에 맞춰 이식성 있게 생성)
metadata.create_all(bind=en)

@app.route("/")
def index():
	with en.connect() as conn:
		rows = conn.execute(text("SELECT id, title, content, author, created_at FROM posts ORDER BY id DESC")).all()
	return render_template("index.html", posts=rows, current_user=session.get("user"))

@app.route("/write", methods=["GET", "POST"])
def write():
	if not session.get("user"):
		return redirect(url_for("login"))
	if request.method == "POST":
		title = request.form.get("title", "").strip()
		content = request.form.get("content", "").strip()
		author = session.get("user")
		if not title or not content:
			return redirect("/")
		with en.begin() as conn:
			conn.execute(
				text("INSERT INTO posts (title, content, author) VALUES (:title, :content, :author)"),
				{"title": title, "content": content, "author": author}
			)
		return redirect("/")
	return render_template("write.html", current_user=session.get("user"))

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
	if not session.get("user"):
		return redirect(url_for("login"))
	with en.begin() as conn:
		# 본인 글만 삭제하도록 제한 (author 일치 시)
		conn.execute(text("DELETE FROM posts WHERE id = :id AND author = :author"), {"id": post_id, "author": session.get("user")})
	return redirect("/")

from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		username = request.form.get("username", "").strip()
		password = request.form.get("password", "").strip()
		if not username or not password:
			return redirect(url_for("register"))
		pw_hash = generate_password_hash(password)
		try:
			with en.begin() as conn:
				conn.execute(text("INSERT INTO users (username, password_hash) VALUES (:u, :p)"), {"u": username, "p": pw_hash})
		except Exception:
			# 중복 등 오류 시 재시도
			return redirect(url_for("register"))
		return redirect(url_for("login"))
	return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username", "").strip()
		password = request.form.get("password", "").strip()
		with en.connect() as conn:
			row = conn.execute(text("SELECT id, username, password_hash FROM users WHERE username = :u"), {"u": username}).fetchone()
		if row and check_password_hash(row[2], password):
			session["user"] = row[1]
			return redirect(url_for("index"))
		return redirect(url_for("login"))
	return render_template("login.html")

@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
