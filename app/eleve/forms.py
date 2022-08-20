from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import Liste


    
class AddEleve(FlaskForm):
    nom = StringField("Nom",[DataRequired()])
    prenom = StringField("Prenom",[DataRequired()])
    id_liste = SelectField("Liste",choices = [(liste.id,liste.nom) for liste in Liste.query.all()])
    id_classe = SelectField("Classe")
    submit = SubmitField("Créer l'élève")


class UpdateEleve(FlaskForm):
    nom = StringField("Nom",[DataRequired()])
    prenom = StringField("Prenom",[DataRequired()])
    id_liste = SelectField("Liste",choices = [(liste.id,liste.nom) for liste in Liste.query.all()])
    id_classe = SelectField("Classe")
    submit = SubmitField("Mettre à jour")
