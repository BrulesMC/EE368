from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SECRET_KEY'] = 'CHANGE_THIS_SECRET_KEY'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Helper: Login Required
def login_required(route_function):
    def wrapper(*args, **kwargs):
        print("Session in login_required:", dict(session))
        print("user_id in session:", "user_id" in session)
        if "user_id" not in session:
            print("No user_id found - redirecting to login")
            return redirect(url_for("login_page"))
        print("user_id found - allowing access")
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__
    return wrapper

# API: Register
@app.post("/api/register")
def api_register():
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, email, password]):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True})


# API: Login
@app.post("/api/login")
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    # Create session
    session.permanent = True
    session["user_id"] = user.id
    session["email"] = user.email

    return jsonify({"success": True}), 200


@app.get("/api/me")
def api_me():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    })

# API: Logout
@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify({"success": True})


# API: Reset Password
@app.post("/api/change-password")
@login_required
def api_change_password():
    data = request.get_json()
    new_password = data.get("new_password")

    if not all([new_password]):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    # Get the current logged-in user
    user = User.query.get(session["user_id"])

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404


    # Update to new password
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"success": True, "message": "Password changed successfully"}), 200

# Protected Route
@app.get("/home")
@login_required
def home_page():
    return render_template("home.html")

@app.get("/check-session")
def check_session():
    return jsonify({
        "user_id": session.get("user_id"),
        "email": session.get("email"),
        "session_data": dict(session)
    })

# Public Pages
@app.get("/")
def login_page():
    return render_template("login.html")

@app.get("/register")
def register_page():
    return render_template("register.html")
    return jsonify({"fail": False})

@app.get("/reset")
def reset_page():
    return render_template("reset.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

