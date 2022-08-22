
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField, Form




options = [{"value":0,"texte":"Pas d'évaluation"},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]

class CellForm(Form):
    # Note pour le niveau 1
    note_1 = SelectField("note1",choices = [(option["value"],option["texte"]) for option in options])
    # Note pour le niveau 2
    note_2 = SelectField("note2",choices = [(option["value"],option["texte"]) for option in options])


class TableNote(FlaskForm):
    id_change = StringField("id_change")
    name_change = StringField("name_change")
    notes = FieldList(FormField(CellForm))


    