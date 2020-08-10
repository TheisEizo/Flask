from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.main.models import Notification
from app.search.models import SearchableMixin
from app.messages.models import Message, Alert, Thread
from app.organization.models import Organization, Event

from hashlib import md5
import jwt
from sqlalchemy import or_
from datetime import datetime
from time import time
import json

thread_to_user = db.Table('thread_to_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('thread_id', db.Integer, db.ForeignKey('thread.id'))
)

org_to_user = db.Table('org_to_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('org_id', db.Integer, db.ForeignKey('organization.id'))
)

event_to_user = db.Table('event_to_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(UserMixin, SearchableMixin, db.Model):
    #Basic information 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    about_me = db.Column(db.String(140))
    def __repr__(self):
        return f'<User {self.username}>'

    #Email and avatar
    email = db.Column(db.String(120), index=True, unique=True)
    email_validated = db.Column(db.Boolean, index=True, default=False)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    #Last seen
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    def is_online(self):
        duration = datetime.now() - self.last_seen
        return duration.total_seconds() > 300

    #Password handling
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, key, expires_in=600):
        return jwt.encode(
            {key: self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_token(key, token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])[key]
        except:
            return
        return User.query.get(id)

    #Make searchable
    __searchable__ = ['username', 'email', 'about_me']

    #Message and Alert integration
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='sender', lazy='dynamic')

    alerts_received = db.relationship('Alert',
                                    foreign_keys='Alert.recipient_id',
                                    backref='recipient', lazy='dynamic')
    #Thread integration
    threads = db.relationship(
        'Thread', secondary=thread_to_user, 
         backref=db.backref('threads', lazy='dynamic'), lazy='dynamic')

    def navbar_messages(self):
        return self.threads.filter(Thread.messages != None).order_by(Thread.last_updated.desc()).limit(5)
    def navbar_alerts(self):
        return self.threads.filter(Thread.alerts != None).order_by(Thread.last_updated.desc()).limit(5)

    def new_messages_count(self):
        threads = self.threads.all()
        return sum([t.new_messages_count(self) for t in threads])

    def new_alerts_count(self):
        threads = self.threads.all()
        return sum([t.new_alerts_count(self) for t in threads])

    def add_thread(self, thread):
        if not self.is_in_thread(thread):
            self.threads.append(thread)
    def is_in_thread(self, thread):
        return self.threads.filter(
            thread_to_user.c.thread_id == thread.id).count() > 0

    #Organization intregration
    orgs = db.relationship(
        'Organization', secondary=org_to_user, 
         backref=db.backref('members', lazy='dynamic'), lazy='dynamic')
    
    events = db.relationship(
        'Event', secondary=event_to_user, 
         backref=db.backref('participants', lazy='dynamic'), lazy='dynamic')

    votes = db.relationship('Vote', backref='user', lazy=True)

    def add_organization(self, org):
        if not self.is_in_org(org):
            self.orgs.append(org)
    def is_in_org(self, org):
        return self.orgs.filter(
            org_to_user.c.org_id == org.id).count() > 0

    def add_event(self, event):
        if not self.is_in_event(event):
            self.events.append(event)
    def is_in_event(self, event):
        return self.events.filter(
            event_to_user.c.event_id == event.id).count() > 0

    #Notification integration
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
