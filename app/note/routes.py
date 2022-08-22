from flask import  render_template ,request, session, redirect, url_for, send_file, after_this_request
from app import db
from app.note import bp
import os
from app.models import Eleve, Item, Note, Liste, Professeur
from app.helpers import tableau_note
from app.note.forms import CellForm, TableNote

@bp.route("/evaluationpdf/<id>")
def evaluationpdf(id):
    output_file_pdf = tableau_note(id)
    @after_this_request
    def remove_file(response):
        os.remove(output_file_pdf)
        print(output_file_pdf)
        return response
    return send_file("../"+output_file_pdf, mimetype='application/pdf', attachment_filename=output_file_pdf,as_attachment=True)


@bp.route("/notes")
def notes():
    # check login
    if not session.get("id_professeur"):
        return redirect(url_for("auth.login"))
    

    # texte des évaluations
    options = [{"value":0,"texte":"Pas d'évaluation"},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]

    professeur = Professeur.query.get(session["id_professeur"])
    id = request.args.get("id")
    

    if id is not None:
        eleves = Eleve.query.filter_by(id=id)
    else:
        eleves = professeur.eleves.order_by(Eleve.id_classe,Eleve.nom)
  
    # On introduit une pagination
    page = request.args.get('page', 1, type=int)
    eleves = eleves.paginate(page=page, per_page=1)

    # Eleve
    eleve = eleves.items[0]
    if eleve.liste is None:
        items = Item.query.all()
    else:
        items = Item.query.filter_by(id_liste = eleve.liste.id)
    
    
    # Filtre élève
    id_liste = request.args.get("liste")
    if id_liste is not None:
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
    

    form = TableNote()
   

    for item in items:
        noteform = CellForm()
        noteform.note_1.default = selected_value[str(item.id)+"A"]
        noteform.note_2.default = selected_value[str(item.id)+"B"]
       
        form.notes.append_entry(noteform)


    return render_template("note/notes.html",eleves = eleves,eleve = eleve, items = items, selected_value=selected_value, options=options,id=id,form=form, zipped=form.notes)







@bp.route("/update_note/<id>")
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

    return redirect(request.referrer)