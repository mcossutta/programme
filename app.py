from flask import Flask, render_template ,request, send_from_directory, session, flash, redirect, url_for
import os
from code1.helpers import produce_pdf, tableau_note_1
from flask_sqlalchemy import SQLAlchemy
import time


#  export FLASK_ENV=development pour mode development dans le shell
app = Flask(__name__)
# le fichier config.py contient les variables de configuration
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
# Le fichier models.py contient les definitions de la base de données
# Le repertoire de travail
workingdir = os.path.abspath(os.getcwd())

def get_timestamp():
    return int(time.time())
app.jinja_env.globals['timestamp'] = get_timestamp


