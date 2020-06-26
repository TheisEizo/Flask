from app import db, create_app
from app.auth.models import User
from werkzeug.security import generate_password_hash

admin = User(
	username='theizo', 
	email='theizo.bedsted@gmail.com', 
	password_hash = generate_password_hash('123'),
	email_validated = True,
	)

guest = User(
	username='theis123', 
	email='theizo.bedsted.junk@gmail.com', 
	password_hash = generate_password_hash('123'),
	email_validated = True,
	)

if __name__ == "__main__":
	app = create_app()
	with app.app_context():
		db.session.add(admin)
		db.session.add(guest)
		db.session.commit()
