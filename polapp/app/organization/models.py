from app import app, db
from app.search.models import SearchableMixin

org_to_org = db.Table('org_to_org',
    db.Column('sub_org_id', db.Integer, db.ForeignKey('organization.id')),
    db.Column('main_org_id', db.Integer, db.ForeignKey('organization.id'))
)

event_to_org = db.Table('event_to_org',
    db.Column('org_id', db.Integer, db.ForeignKey('organization.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

resource_to_event = db.Table('resource_to_event',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
)

class Organization(SearchableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    img = db.Column(db.String(140))

    main_orgs = db.relationship(
        'Organization', secondary=org_to_org,
        primaryjoin=(org_to_org.c.sub_org_id == id),
        secondaryjoin=(org_to_org.c.main_org_id == id),
        backref=db.backref('sub_orgs', lazy='dynamic'), lazy='dynamic')

    def add_organization(self, org):
        if not self.is_in_org(org):
            self.main_orgs.append(org)

    def is_in_org(self, org):
        return self.main_orgs.filter(
            org_to_org.c.main_org_id == org.id).count() > 0

    events = db.relationship(
        'Event', secondary=event_to_org, 
         backref=db.backref('events', lazy='dynamic'), lazy='dynamic')

    def add_event(self, event):
        if not self.is_in_event(event):
            self.events.append(event)

    def is_in_event(self, event):
        return self.events.filter(
            event_to_org.c.event_id == event.id).count() > 0

class Event(SearchableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    img = db.Column(db.String(140))

    start_time = db.Column(db.DateTime, index=True, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    votes = db.relationship('Vote', backref='event', lazy=True)

    resources = db.relationship(
        'Resource', secondary=resource_to_event, 
         backref=db.backref('resources', lazy='dynamic'), lazy='dynamic')

class Resource(SearchableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    img = db.Column(db.String(140))

    file = db.Column(db.Boolean)
    place = db.Column(db.Boolean)
    location = db.Column(db.String(140))

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    


    




