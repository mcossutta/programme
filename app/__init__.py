from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# le fichier config.py contient les variables de configuration
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.eleve import bp as eleve_bp
app.register_blueprint(eleve_bp)

from app.note import bp as note_bp
app.register_blueprint(note_bp)



from app import routes, models