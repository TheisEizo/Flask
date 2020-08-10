from app import db
from datetime import datetime
from flask_login import current_user

user_to_message = db.Table('user_to_message',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    db.Column('read_time', db.DateTime),
)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    body = db.Column(db.String(140))
    sent_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    recipients = db.relationship(
        'User', secondary=user_to_message, 
         backref=db.backref('messages_received', lazy='dynamic'), lazy='dynamic')

    def add_recipient(self, user):
        if not self.is_in_message(user):
            self.recipients.append(user)
    def is_in_message(self, user):
        return self.recipients.filter(
            user_to_message.c.user_id == user.id).count() > 0

    def get_read_time(self, user):
        u2m = db.session.query(user_to_message).filter_by(message_id=self.id).filter_by(user_id=user.id).first()
        if u2m: 
           return u2m.read_time 
        else: 
           return None

    def set_read_time(self, user, time):
        stmt = user_to_message.update().where(user_to_message.c.message_id==self.id).where(user_to_message.c.user_id==user.id).values(read_time=time)
        db.engine.execute(stmt)

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

    def get_img(self, user, size=60):
        if self.last_message().sender != current_user:
           return self.last_message().sender.avatar(size)
        else:
           return f'https://www.gravatar.com/avatar/{self.id}?d=identicon&s={size}'

    def new_messages_count(self, user):
        q = self.messages.filter(
                    user_to_message.c.user_id == user.id).filter(
                    user_to_message.c.read_time.is_(None))
        #print(q.all())
        return q.count()

    def new_alerts_count(self, user):
        return self.alerts.filter(Alert.recipient_id==user.id).filter(Alert.read_time.is_(None)).count()

    def __repr__(self):
        return f'<Thread {self.messages.all()} {self.alerts.all()}>'
