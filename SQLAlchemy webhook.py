from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blinker import Namespace
import requests
import json

my_signals = Namespace()
db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
db.init_app(app)

user_saved_signal = my_signals.signal('user-saved')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

# webhook fired after user is inserted (registration)
def send_webhook_notification(_mapper, _connection, target):
    payload = {
        "event": "user_registered",
        "data": {
            "id": target.id,
            "name": target.name,
            "email": target.email
        }
    }

    try:
        requests.post(
            "http://<java-app-ip>:<port>/api/webhook-receiver",
            json=payload,
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

from sqlalchemy import event
event.listen(User, 'after_insert', send_webhook_notification)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)