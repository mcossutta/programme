from app import db
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(db.engine,reflect=True)
Chapitre = Base.classes.item
Sous_Chapitre = Base.classes.souschapitre_C
Objectifs = Base.classes.objectifs
Theme = Base.classes.theme
Eleves = Base.classes.eleves
Note = Base.classes.note
Professeur = Base.classes.professeur