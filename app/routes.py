from flask import  render_template , session, redirect, url_for
from app import app
from app.models import  Professeur,  Liste 
from app.helpers import Filtre
import time


def get_timestamp():
    return int(time.time())



app.jinja_env.globals['timestamp'] = get_timestamp
app.jinja_env.globals.update(zip=zip)


# utiliser pour créer les boutons de filtre
@app.context_processor
def filtre():
    def listes():
        return Liste.query.all()
    def professeurs():
        return Professeur.query.all()
    return  {"listes":listes,"professeurs":professeurs}


@app.add_template_filter
def format_eleve(eleve):
    return "{} {} {} {}".format(eleve.prenom,eleve.nom,eleve.classe.nom, eleve.liste.nom if eleve.liste is not None else "")





# Un blue print pour les classes.
@app.route("/")
def index():
    if session.get("id_professeur"):
        professeur = Professeur.query.get(session["id_professeur"])
        classes = professeur.classes
        return render_template("index.html", prof = professeur, classes = classes)
    else:
        return redirect(url_for('auth.login'))
 



# Un blue print eleve pour la page de la modification des items.
@app.route("/items")
def items():
    if not session.get("id_professeur"):
        return redirect(url_for("auth.login"))
    
    # Filtre liste
    filtre = Filtre()
    
    return render_template("item.html",items = filtre["items"],liste_selected=filtre["liste_selected"])

