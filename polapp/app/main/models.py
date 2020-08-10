from app import db
from time import time
import json

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        print(f'{self.user_id}: {self.name}, {self.payload_json}')
        return json.loads(str(self.payload_json))
