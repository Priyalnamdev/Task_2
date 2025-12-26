from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ---------------- MYSQL CONFIG ----------------
# REAL PASSWORD: Pri#yal%1*8nam_04$
# ENCODED PASSWORD: Pri%23yal%251%2A8nam_04%24

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:Pri%23yal%251%2A8nam_04%24@localhost/comment_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- CREATE TABLES ----------------

with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Flask MySQL API is running"

# CREATE TASK
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title}), 201

# CREATE COMMENT
@app.route("/tasks/<int:task_id>/comments", methods=["POST"])
def create_comment(task_id):
    Task.query.get_or_404(task_id)
    data = request.json
    comment = Comment(content=data["content"], task_id=task_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content}), 201

# GET COMMENTS
@app.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([
        {"id": c.id, "content": c.content}
        for c in comments
    ])

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
