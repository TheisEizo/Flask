from app import db, create_app
if __name__ == "__main__":
	app = create_app()
	db.drop_all(app=app)
	db.create_all(app=app)
