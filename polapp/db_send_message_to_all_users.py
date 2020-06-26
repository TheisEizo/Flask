from app import db, create_app
from app.auth.models import User
from app.messages.models import Message, Thread

sender = 'theis123'
content = 'Hi'


if __name__ == "__main__":
	app = create_app()
	with app.app_context():
		sender = User.query.filter_by(username=sender).first()
		all_users = User.query.all()
		for user in all_users:
			thread = Thread()
			#sender.add_thread(thread)
			
			db.session.add(thread)
			user.add_thread(thread)
			#db.session.commit()
			#thread = Thread.query.filter_by(id=thread.id).first()
			message = Message(
				sender = sender, 
				recipient = user,
				thread = thread,
				body = f'{content} {user.username}'
				)
			db.session.add(message)
			db.session.commit()
