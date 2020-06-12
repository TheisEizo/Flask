from app import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    sent_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read_time = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Message {self.body}>'


