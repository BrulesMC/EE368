from flask import Flask, request, jsonify, session, redirect, url_for
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
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Helper: Login Required
def login_required(route_function):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login_page"))
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__
    return wrapper


# API: Register
@app.post("/api/register")
def api_register():
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([first_name, last_name, username, password]):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
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
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid credentials"})

    # Create session
    session.permanent = True
    session["user_id"] = user.id
    session["username"] = user.username

    return jsonify({"success": True})



# API: Logout
@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify({"success": True})


# API: Reset Password
@app.post("/api/reset-password")
def api_reset_password():
    data = request.get_json()
    email = data.get("email")
    return jsonify({"success": True})


# Protected Route
@app.get("/home")
@login_required
def home_page():
    return """
    <h1>Logged in</h1>
    <button onclick="logout()">Logout</button>
    <script>
    function logout() {
        fetch('/api/logout', { method: 'POST' })
            .then(() => window.location.href = '/');
    }
    </script>
    """



# Public Pages
@app.get("/")
def login_page():
    return redirect("/static/login.html")

@app.get("/register")
def register_page():
    return redirect("/static/register.html")

@app.get("/reset")
def reset_page():
    return redirect("/static/reset.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)