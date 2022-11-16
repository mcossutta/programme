from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
load_dotenv(path.join(basedir, '.flaskenv'))

print('sqlite:///' + path.join(basedir, 'app.db'))
class Config(object):
    #TESTING = True
    #DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY') 
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI") or 'sqlite:///' + path.join(basedir, 'app.db')





