from app import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    body = db.Column(db.String(140))
    sent_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read_time = db.Column(db.DateTime)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f'<Message {self.body}>'

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    body = db.Column(db.String(140))
    icon = db.Column(db.String(140), default="fa-exclamation-triangle")
    background = db.Column(db.String(140), default="bg-warning")
    sent_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read_time = db.Column(db.DateTime)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return f'<Alert {self.body}>'

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    messages = db.relationship('Message', backref='thread', lazy='dynamic')
    alerts = db.relationship('Alert', backref='thread', lazy='dynamic')

    def last_message(self):
        return self.messages.order_by(Message.sent_time.desc()).first()
    def last_alert(self):
        return self.alerts.order_by(Alert.sent_time.desc()).first()
    def new_messages_count(self):
        return self.messages.filter(Message.read_time.is_(None)).count()
    def new_alerts_count(self):
        return self.alerts.filter(Alert.read_time.is_(None)).count()

    def __repr__(self):
        return f'<Thread {self.messages.all()} {self.alerts.all()}>'
