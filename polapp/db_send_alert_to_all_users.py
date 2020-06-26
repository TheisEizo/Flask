from app import db, create_app
from app.auth.models import User
from app.messages.models import Alert, Thread

content = 'WARNING'
background = 'bg-success'
icon = 'fa-exclamation-triangle'

if __name__ == "__main__":
	app = create_app()
	with app.app_context():
		all_users = User.query.all()
		for user in all_users:
			thread = Thread()
			db.session.add(thread)
			user.add_thread(thread)
			
			#db.session.commit()
			#thread = Thread.query.filter_by(id=thread.id).first()
			alert = Alert(
				thread = thread,
				recipient = user,
				body = f'{content} {user.username}',
				icon = icon,
				background = background)
			db.session.add(alert)
			db.session.commit()
