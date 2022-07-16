from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# le fichier config.py contient les variables de configuration
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models