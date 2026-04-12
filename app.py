from flask import Flask, request, jsonify, session, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_login import LoginManager
from datetime import timedelta
import requests
import os
from dotenv import load_dotenv
import subprocess
import threading
import sys

# Start Oauth server
def start_oauth_server():
    oauth_path = os.path.join(os.path.dirname(__file__), "oauth_server.py")
    process = subprocess.Popen(
        [sys.executable, oauth_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )

    print(f"[Main App] OAuth server started on port 5001 (PID={process.pid})")
    def stream_output():
        for line in process.stdout:
            print("[OAuth]", line, end="")
    # threading.Thread(target=stream_output, daemon=True).start()
    return process

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Session lifetime
app.permanent_session_lifetime = timedelta(days=7)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"

# Main App User Model
class AppUser(db.Model):
    __tablename__ = "app_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(20), nullable=False, default="standard")  # standard | github | custom

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "type": self.type
        }

# Flask-Login Loader
@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(user_id)

# Helper Functions
def login_user_session(user):
    session["user_id"] = user.id
    session.permanent = True

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return AppUser.query.get(uid)

# OAuth Client Config

# Custom OAuth client credentials
CUSTOM_CLIENT_ID = os.environ.get("CUSTOM_CLIENT_ID", "client_123")
CUSTOM_CLIENT_SECRET = os.environ.get("CUSTOM_CLIENT_SECRET", "")
CUSTOM_REDIRECT_URI = "http://127.0.0.1:5000/custom_callback"

# IMPORTANT: OAuth server runs on port 5001
CUSTOM_AUTH_URL = "http://127.0.0.1:5001/oauth/authorize"
CUSTOM_TOKEN_URL = "http://127.0.0.1:5001/oauth/token"
CUSTOM_USERINFO_URL = "http://127.0.0.1:5001/oauth/userinfo"
CUSTOM_SCOPE = "profile"

# GitHub OAuth Credentials
GITHUB_CLIENT_ID = "Ov23liYnjEz7sbKDdfhQ"
GITHUB_CLIENT_SECRET = "c2602bddacd1641ff61bc4cb4cab9b743f0dc789"
GITHUB_REDIRECT_URI = "http://127.0.0.1:5000/github_callback"

# HTML Routes
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/reset")
def reset_page():
    return render_template("reset.html")

@app.route("/home")
def home_page():
    if not current_user():
        return redirect("/")
    return render_template("home.html")

# API: Register
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password required"}), 400

    if AppUser.query.filter_by(username=username).first():
        return jsonify({"error": "username already exists"}), 400

    if AppUser.query.filter_by(email=email).first():
        return jsonify({"error": "email already in use"}), 400

    user = AppUser(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        type="standard"
    )
    db.session.add(user)
    db.session.commit()

    login_user_session(user)
    return jsonify({"success": True, "user": user.to_dict()}), 201

# API: Standard Login
@app.route("/api/login_standard", methods=["POST"])
def login_standard():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = AppUser.query.filter_by(email=email, type="standard").first()

    if not user or not user.password_hash:
        return jsonify({"error": "invalid credentials"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    login_user_session(user)
    return jsonify({"success": True, "user": user.to_dict()})

# GitHub OAuth
@app.route("/login_github")
def login_github_redirect():
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "user:email"
    }
    if (0 != (subproccess.call("ping github.com"))):
        redirect(:"error")
    else:
        query = "&".join([f"{k}={v}" for k, v in params.items()])
        return redirect(f"https://github.com/login/oauth/authorize?{query}")

@app.route("/github_callback")
def github_callback():
    code = request.args.get("code")
    if not code:
        return redirect("/")

    token_res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI
        }
    ).json()

    access_token = token_res.get("access_token")
    if not access_token:
        return redirect("/")

    user_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email_res = requests.get(
        "https://api.github.com/user/emails",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = None
    for e in email_res:
        if e.get("primary"):
            email = e.get("email")
            break

    if not email:
        email = user_res.get("email")

    username = user_res.get("login")

    user = AppUser.query.filter_by(email=email).first()
    if not user:
        base = username
        i = 1
        while AppUser.query.filter_by(username=username).first():
            username = f"{base}_{i}"
            i += 1

        user = AppUser(username=username, email=email, password_hash=None, type="github")
        db.session.add(user)
        db.session.commit()

    login_user_session(user)
    return redirect("/home")

# Custom OAuth (Port 5001)
@app.route("/login_custom")
def login_custom_redirect():
    params = {
        "client_id": CUSTOM_CLIENT_ID,
        "redirect_uri": CUSTOM_REDIRECT_URI,
        "scope": CUSTOM_SCOPE,
        "response_type": "code",
    }
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return redirect(f"{CUSTOM_AUTH_URL}?{query}")

@app.route("/custom_callback")
def custom_callback():
    code = request.args.get("code")
    if not code:
        return redirect("/")

    token_res = requests.post(
        CUSTOM_TOKEN_URL,
        auth=(CUSTOM_CLIENT_ID, CUSTOM_CLIENT_SECRET),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": CUSTOM_REDIRECT_URI,
        }
    ).json()

    access_token = token_res.get("access_token")
    if not access_token:
        return redirect("/")

    user_res = requests.get(
        CUSTOM_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = user_res.get("email")
    username = user_res.get("name") or email

    if not email:
        return redirect("/")

    user = AppUser.query.filter_by(email=email).first()
    if not user:
        base = username
        i = 1
        while AppUser.query.filter_by(username=username).first():
            username = f"{base}_{i}"
            i += 1

        user = AppUser(username=username, email=email, password_hash=None, type="custom")
        db.session.add(user)
        db.session.commit()

    login_user_session(user)
    return redirect("/home")

# API: Reset Password
@app.route("/api/reset_password", methods=["POST"])
def reset_password():
    user = current_user()
    if not user:
        return jsonify({"error": "not logged in"}), 401

    if user.type != "standard":
        return jsonify({"error": "Only standard users can reset their password"}), 400

    data = request.json or {}
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({"error": "new_password required"}), 400

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"success": True})

# API: Me / Logout
@app.route("/api/me")
def me():
    user = current_user()
    if not user:
        return jsonify({"error": "not logged in"}), 401
    return jsonify(user.to_dict())

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"success": True})

# Run
if __name__ == "__main__":
    oauth_process = start_oauth_server()

    with app.app_context():
        db.create_all()
    try:
        app.run(debug=True)
    finally:
        oauth_process.terminate()
