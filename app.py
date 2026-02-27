
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

<<<<<<< Updated upstream
    if not all([first_name, last_name, email, password]):
        return jsonify({"success": False, "message": "Missing fields"}), 400
=======
    if not username or not email or not password:
        return jsonify({"error": "username, email, and password required"}), 400
>>>>>>> Stashed changes

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "User already exists"}), 400

<<<<<<< Updated upstream
    hashed_pw = generate_password_hash(password)
=======
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already in use"}), 400
>>>>>>> Stashed changes

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_pw
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True})

<<<<<<< Updated upstream

# API: Login
@app.post("/api/login")
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

=======
# API: Standard Login
@app.route("/api/login_standard", methods=["POST"])
def login_standard():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = User.query.filter_by(email=email, type="standard").first()

    if not user or not user.password_hash:
        return jsonify({"error": "invalid credentials"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    login_user(user)
    return jsonify({"success": True, "user": user.to_dict()})



# GitHub Login (Server-Side OAuth)
@app.route("/login_github")
def login_github_redirect():
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "user:email"
    }
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return redirect(f"https://github.com/login/oauth/authorize?{query}")


@app.route("/github_callback")
def github_callback():
    code = request.args.get("code")
    if not code:
        return redirect("/")

    # Exchange code for access token
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

    # Fetch GitHub user info
    user_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    # Fetch email list
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

    # Auto-create or fetch user
>>>>>>> Stashed changes
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
    app.run(host='0.0.0.0', port=8000, debug=True)

