from flask import  render_template ,request, session, flash, redirect, url_for, send_file
from app import app, db
import os, io
from app.models import Eleve, Professeur, Item, Note, Liste
from app.helpers import tableau_note
import time


def get_timestamp():
    return int(time.time())
app.jinja_env.globals['timestamp'] = get_timestamp

@app.context_processor
def listes():
    def Listes():
        return Liste.query.all()
    return  {"listes":Listes}

### Blue print logins

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
        professeur = Professeur.query.filter_by(trigramme = trigramme).first()
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
    


#### Blue print eleve ###


@app.route("/eleves")
def eleves():
    if not session.get("id_professeur"):
        return redirect(url_for("login"))

    professeur = Professeur.query.get(session["id_professeur"])
    return render_template("eleves.html", eleves = professeur.eleves)        
        
@app.route("/delete/<id>")
def delete_eleve(id):
    eleve = Eleve.query.get(id)
    db.session.delete(eleve)
    db.session.commit()
    return redirect(url_for("eleves"))




@app.route("/update_eleve/<id>", methods=["POST","GET"])
def update_eleve(id):
    if request.method == "GET":
        eleve = Eleve.query.get(id)
        listes = Liste.query.all()
        classes = Liste.query.all()
        return render_template("update_eleve.html",eleve = eleve, listes = listes, classes = classes)
        
    if request.method == "POST":
        eleve = Eleve.query.get(id)
        print(request.form)
        print(request.form["nom"])
        print(request.form["prenom"])
        print(request.form.get("liste"))
        eleve.nom = request.form["nom"]
        eleve.prenom = request.form["prenom"]
        eleve.id_liste = int(request.form.get("liste"))
        db.session.commit()
        return redirect(url_for("eleves"))


@app.route("/add_eleve", methods=["POST","GET"])
def add_eleve():

    if request.method == "GET":
        return render_template("add_eleve.html")
    if request.method == "POST":
        return redirect(url_for("eleves"))


#### Blue print evaluation ######



@app.route("/evaluationpdf/<id>/<time>")
def evaluationpdf(id,time):
    output_file_pdf = tableau_note(id)

    return_data = io.BytesIO()
    with open(output_file_pdf, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    os.remove(output_file_pdf)

    return send_file(return_data, mimetype='application/pdf',
                     attachment_filename='download_filename.pdf')





@app.route("/note/<id>")
def note(id):
    # check login
    if not session.get("id_professeur"):
        return redirect(url_for("login"))
    
    # texte des évaluations
    options = [{"value":0,"texte":"Pas d'évaluation"},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    

    # Eleve
    eleve = Eleve.query.get(id)
    if eleve.liste is None:
        items = Item.query.all()
    else:
        items = Item.query.filter_by(id_liste = eleve.liste.id)
    # Liste de l'élève
    
    # Filtre élève
    if request.args.get("liste") is not None:
        id_liste = request.args.get("liste")
        liste_filtre = Liste.query.get(id_liste)
        items = liste_filtre.items

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
    return render_template("note.html",eleve = eleve, items = items, selected_value=selected_value, options=options)


@app.route("/update_note/<id>")
def update_note(id): 
    Niveau = {"A":1,"B":2}
    x = request.args.get("id_change")
    niveau = Niveau[x[-1:]]
    id_item = int(x[:-1])
    note_el = int(request.args.get(x))
    notes = Note.query.filter_by(id_eleve =int(id),niveau = niveau,id_item=id_item)
    
    if notes.first() is not None:
        notes.first().note = note_el    
    else:
        note = Note()
        note.id_eleve = int(id)
        note.niveau = niveau
        note.id_item = id_item
        note.note = note_el
        db.session.add(note)
    
    db.session.commit()

    return redirect(url_for('note',id = id))



@app.route("/items")
def items():
    if not session.get("id_professeur"):
        return redirect(url_for("login"))
    items = Item.query.all()
    return render_template("item.html",items = items)

