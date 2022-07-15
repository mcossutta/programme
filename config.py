from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
print(basedir)
load_dotenv(path.join(basedir, '.env'))

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = environ.get('SECRET_KEY') or 'secret_key'

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' + path.join(basedir, 'data/base_chapitre.db')
SQLALCHEMY_TRACK_MODIFICATION = False
UPLOAD_FOLDER = path.join(basedir,"/output")


