from flask import  render_template ,request, send_from_directory, session, flash, redirect, url_for
from app import app, db
import os
from app.models import Theme, Eleve, Professeur, Item, Note
from app.helpers import tableau_note



# Le repertoire de travail
workingdir = os.path.abspath(os.getcwd())
import time
def get_timestamp():
    return int(time.time())
app.jinja_env.globals['timestamp'] = get_timestamp


workingdir = os.path.abspath(os.getcwd())

@app.route("/")
def index():
    if session.get("id_professeur"):
        professeur = Professeur.query.get(session["id_professeur"])
        return render_template("index.html", prof = professeur)
    else:
        return redirect(url_for('login'))
 

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        trigramme = request.form["trigramme"]
        professeur = Professeur.query.filter(Professeur.trigramme == trigramme).first()
        if professeur is None:
            flash("Ce trigramme n'est pas valable")
            return redirect(url_for("login")) 
        else:
            session["id_professeur"] = professeur.id
            return redirect(url_for('index'))


@app.route("/logout") 
def logout():
    if session.get("id_professeur"):
        session.pop("id_professeur")
    return render_template("logout.html")
    

@app.route("/items")
def items():
    items = Item.query.all()
    return render_template("item.html",items = items)



@app.route("/pagegardepdf")
def page_garde_pdf():
    return render_template("TODOS.html")


@app.route("/evaluationpdf/<id>/<time>")
def evaluationpdf(id,time):
    output_file_pdf = tableau_note(id)
    return send_from_directory(workingdir, output_file_pdf)




@app.route("/eleves")
def eleves():
    if session.get("id_professeur"):
        professeur = Professeur.query.get(session["id_professeur"])
        return render_template("eleves.html", Dict_eleves = professeur.eleves)        
    else:
        return redirect(url_for("login"))
        


@app.route("/note/<id>")
def note(id):
    options = [{"value":0,"texte":"Pas d'évaluation"},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]

    eleve = Eleve.query.get(id)
    items = Item.query.all()

    # Liste des notes vides
    selected_value = {}
    for item in items:
        selected_value[str(item.id)+"A"] = 0
        selected_value[str(item.id)+"B"] = 0
    

    # Liste des notes complétées avec la DB
    for x in eleve.notes:
        if x.niveau == 1:
            selected_value[str(x.id_item)+"A"] = x.note
        else:
            selected_value[str(x.id_item)+"B"] = x.note
    return render_template("note.html",Dict_eleve = eleve, Liste_chapitre = items, selected_value=selected_value, options=options)


@app.route("/update_note/<id>")
def update_note(id): 
    for x in request.args:
        notes = Note.query.filter(Note.id_eleve ==int(id))
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
