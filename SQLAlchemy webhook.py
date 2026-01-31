import Item
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

item_saved_signal = my_signals.signal('item-saved')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

# call after database update
def send_webhook_notification(mapper, connection, target):
        payload = {
            "event": "item_saved",
            "data": {
                "id": target.id,
                "name": target.name
            }
        }
        try:
            # placeholder URL
            requests.post("http://<java-app-ip>:<port>/api/webhook-reciever",
                          json=payload,
                          timeout=5
                          )
        #exceptions for connection errors
        except requests.exceptions.RequestException as e:
            print(f"Error sending webhook: []")

from sqlalchemy import event
event.listen(Item, 'after_insert', send_webhook_notification)

#placeholder route for triggering webhook
@app.route('/add_item/<name>')
def add_item(name):
    new_item = Item(name=name)
    db.session.add(new_item)
    db.session.commit()
    return f"Item {name} added and webhook sent"

if __name__ == '__main__':
    with app.app_context():
        db.create_tables()
    app.run(debug=True)