# app.py

import os
from flask import Flask, request, jsonify
from models import db, User, Task
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    # Register
    @app.route("/auth/register", methods=["POST"])
    def register():
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"msg":"username & password required"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"msg":"user exists"}), 400
        u = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()
        return jsonify({"msg":"registered"}), 201

    # Login
    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"msg":"username & password required"}), 400
        u = User.query.filter_by(username=username).first()
        if not u or not check_password_hash(u.password_hash, password):
            return jsonify({"msg":"bad username/password"}), 401
        access_token = create_access_token(identity=str(u.id))
        return jsonify({"access_token":access_token})

    # Create Task
    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        user_id = get_jwt_identity()
        data = request.json or {}
        title = data.get("title")
        description = data.get("description")
        due_date_str = data.get("due_date")  # expect ISO format e.g. "2025-09-21T15:30:00"
        recurrence = data.get("recurrence")  # "daily", "weekly", or None
        priority = data.get("priority", 1)
        if not title:
            return jsonify({"msg":"title required"}), 400
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.datetime.fromisoformat(due_date_str)
            except:
                return jsonify({"msg":"bad due_date format"}), 400
        t = Task(user_id=int(user_id), title=title, description=description, due_date=due_date, priority=priority, recurrence=recurrence)
        db.session.add(t)
        db.session.commit()
        return jsonify({"msg":"task created", "task": {"id": t.id, "title": t.title}}), 201

    # List tasks
    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def list_tasks():
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=int(user_id)).all()
        result = []
        now = datetime.datetime.utcnow()
        for t in tasks:
            # adaptive priority: increase priority if close or past due date
            score = t.priority
            if t.due_date:
                delta = (t.due_date - now).total_seconds()
                if delta < 0:
                    score += 5  # overdue
                elif delta < 3600*24:  # due within a day
                    score += 2
            result.append({
                "id": t.id,
                "title": t.title,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "priority": t.priority,
                "status": t.status,
                "recurrence": t.recurrence,
                "adaptive_score": score
            })
        # sort by adaptive_score descending
        result_sorted = sorted(result, key=lambda x: x["adaptive_score"], reverse=True)
        return jsonify({"tasks": result_sorted})

    # Recommendation endpoint: top N tasks to do now
    @app.route("/tasks/recommend", methods=["GET"])
    @jwt_required()
    def recommend():
        user_id = get_jwt_identity()
        # reuse list_tasks logic
        # maybe limit to top 3
        tasks_list_resp = list_tasks().get_json().get("tasks", [])
        top = tasks_list_resp[:3]
        return jsonify({"recommendations": top})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
