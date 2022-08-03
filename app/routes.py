from flask import  render_template ,request, session, flash, redirect, url_for, send_file
from app import app, db
import os, io
from app.models import Eleve, Professeur, Item, Note
from app.helpers import tableau_note



# Le repertoire de travail
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
    

@app.route("/items")
def items():
    if not session.get("id_professeur"):
        return redirect(url_for("login"))
    items = Item.query.all()
    return render_template("item.html",items = items)




@app.route("/evaluationpdf/<id>")
def evaluationpdf(id):
    output_file_pdf = tableau_note(id)

    return_data = io.BytesIO()
    with open(output_file_pdf, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    os.remove(output_file_pdf)

    return send_file(return_data, mimetype='application/pdf',
                     attachment_filename='download_filename.pdf')





@app.route("/eleves")
def eleves():
    if not session.get("id_professeur"):
        return redirect(url_for("login"))

    professeur = Professeur.query.get(session["id_professeur"])
    return render_template("eleves.html", Dict_eleves = professeur.eleves)        
        
        


@app.route("/note/<id>")
def note(id):
    if not session.get("id_professeur"):
        return redirect(url_for("login"))
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
