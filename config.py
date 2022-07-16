from os import environ, path


basedir = path.abspath(path.dirname(__file__))
print(basedir)


TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY') or 'secret_key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app/data/base_chapitre.db')
SQLALCHEMY_TRACK_MODIFICATION = False
UPLOAD_FOLDER = path.join(basedir,"/output")


