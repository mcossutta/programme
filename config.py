from os import environ, path
basedir = path.abspath(path.dirname(__file__))


class Config(object):
    TESTING = True
    DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False
    UPLOAD_FOLDER = path.join(basedir,"/output")


