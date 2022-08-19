from flask import Blueprint

bp = Blueprint("eleve",__name__)

from app.eleve import routes