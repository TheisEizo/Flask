import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig:
    SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL = False
    MAIL_USERNAME='theizo.bedsted.db@gmail.com'
    MAIL_PASSWORD='PythonPassword'
    MAIL_DEFAULT_SENDER='theizo.bedsted.db@gmail.com'
