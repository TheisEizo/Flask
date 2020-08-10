from app import db, create_app
from app.organization.models import Organization
from app.auth.models import User

username = 'theizo'
main = Organization(name = 'main_org')

if __name__ == "__main__":
	app = create_app()
	with app.app_context():
		db.session.add(main)
		db.session.commit()