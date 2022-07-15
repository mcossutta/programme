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
from models import *
# Le repertoire de travail
workingdir = os.path.abspath(os.getcwd())



def get_timestamp():
    return int(time.time())
app.jinja_env.globals['timestamp'] = get_timestamp


@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        session["username"] = request.form["username"]
        prof = db.session.query(Professeur).filter(Professeur.trigramme == session["username"]).first()
        return render_template("index.html", prof=prof)
    else:
        return render_template("index.html", prof={"prenom":"","nom":""})

@app.route("/logout") 
def logout():
    session.pop("username")
    return render_template("index.html")
    

@app.route("/chapitres")
def chapitres():
    #Liste des chapitres 
    L = [{"name":item.name, "id":str(item.id)} for item in db.session.query(Chapitre)]
    print(L) 

    #Liste des sous-chapitre
    L1 = [{"name":item.name,"id":str(item.id)} for item in db.session.query(Sous_Chapitre)]

    # Tableau chapitre-sous-chapitre theme
    L2 = [{"name_sc": item1.name, "name_c":item2.name, "theme":item3.name } for item1,item2,item3 in db.session.\
        query(Sous_Chapitre,Chapitre,Theme).filter(Sous_Chapitre.id_item == Chapitre.id).\
            filter(Chapitre.id_theme==Theme.id)]
    return render_template("chapitres.html", liste_chapitre = L,liste_sous_chapitre =L1,liste_objectif =L2)




@app.route("/pagegardepdf")
def page_garde_pdf():
# message d'erreur si pas de selection
    sous_chapitre = request.args.get("sous_chapitre")
    if sous_chapitre == "0":
        flash("Choisir un chapitre")
        return redirect(url_for("chapitres"))
# Rempli le dicionnaire avec des requêtes à la db pour appeler la fonction produce_pdf 
    dict_pdf = {"objectifs":[],"num_chapter":"","chapitre":"","theme":"","sous_chapitre":""}
    dict_pdf["num_chapter"] = str(db.session.query(Sous_Chapitre).\
        filter(Sous_Chapitre.id ==sous_chapitre).first().id_item)
    dict_pdf["chapitre"] = db.session.query(Chapitre).\
        filter(Chapitre.id == dict_pdf["num_chapter"]).first().name
    dict_pdf["sous_chapitre"] = db.session.query(Sous_Chapitre).\
        filter(Sous_Chapitre.id ==sous_chapitre).first().name
    id_theme = db.session.query(Chapitre).\
        filter((Chapitre.id == dict_pdf["num_chapter"])).first().id_theme
    dict_pdf["theme"] = db.session.query(Theme).filter(Theme.id == id_theme).first().name
    dict_pdf["objectifs"] = [obj.objectifs for obj in db.session.query(Objectifs).\
        filter(Objectifs.id_sc ==sous_chapitre)]
    dict_pdf["trigramme"] = session["username"]
    return send_from_directory(workingdir, produce_pdf(dict_pdf))


@app.route("/evaluationpdf/<id>/<time>")
# La variable time permet de ne pas utiliser le cache pour le pdf
def evaluationpdf(id,time):

    output_file_pdf = tableau_note_1(id,db.session,Eleves,Professeur,Note,Theme,Chapitre)
    return send_from_directory(workingdir, output_file_pdf)




@app.route("/eleves")
def eleves():
    Dict_eleves =[{"Nom":item.Nom, "Prenom":item.Prenom, "classe":item.classe, "id":item.ID} for item in db.session.query(Eleves).\
    filter(Eleves.trigramme == session["username"])]
    return render_template("eleves.html", Dict_eleves = Dict_eleves)


@app.route("/note/<id>")
def note(id):
    options = [{"value":0,"texte":"Pas d'évaluation"},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    Dict_eleve = {}
    Dict_eleve["id"] = id
    Dict_eleve["nom"] = db.session.query(Eleves).filter(Eleves.ID == Dict_eleve["id"]).first().Nom
    Dict_eleve["prenom"] = db.session.query(Eleves).filter(Eleves.ID == Dict_eleve["id"]).first().Prenom
    Liste_chapitre = [{"name":item.name,"id":item.id} for item in db.session.query(Chapitre)]
    
    # Liste des notes vides
    selected_value = {}
    for x in Liste_chapitre:
        selected_value[str(x["id"])+"A"] = 0
        selected_value[str(x["id"])+"B"] = 0
    
    # Liste des notes complétées avec la DB
    for x in db.session.query(Note).filter(Note.id_eleve==int(Dict_eleve["id"])).all():
        if x.niveau == 1:
            selected_value[str(x.id_item)+"A"] = x.note
        else:
            selected_value[str(x.id_item)+"B"] = x.note
    return render_template("note.html",Dict_eleve = Dict_eleve, Liste_chapitre = Liste_chapitre, selected_value=selected_value, options=options)


@app.route("/update_note/<id>")
def update_note(id): 
    for x in request.args:
        notes = db.session.query(Note).filter(Note.id_eleve ==int(id))
        note = Note()
        note.id_eleve = int(id)
        if x[-1:] == "A":
            notes = notes.filter(Note.niveau ==1)
            note.niveau =1
        else:
            notes = notes.filter(Note.niveau == 2)
            note.niveau = 2
        notes =notes.filter( Note.id_item == int(x[:-1]))
        note.id_item = int(x[:-1])
        if notes.first() == None:
            note.note = int(request.args.get(x))
            db.session.add(note)
            db.session.commit()
        else:
            notes.first().note = int(request.args.get(x))
            db.session.commit()
       
    return redirect(url_for('eleves'))


