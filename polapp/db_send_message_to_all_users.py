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
			db.session.add(thread)
			user.add_thread(thread)
			message = Message(
				sender = sender, 
				thread = thread,
				body = f'{content} {user.username}'
				)
			db.session.add(message)
			message.add_recipient(user)
			user.add_notification('unread_message_count', user.new_messages_count())
			db.session.commit()
