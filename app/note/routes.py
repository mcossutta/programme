from flask import  render_template ,request, session, redirect, url_for, send_file, after_this_request
from app import db
from app.note import bp
import os
from app.models import Eleve, Item, Note, Liste, Professeur
from app.helpers import tableau_note, Filtre
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
    

    professeur = Professeur.query.get(session["id_professeur"])
        
    # Si id est rempli un seul élève
    id = request.args.get("id")
    if id is not None:
        eleves = Eleve.query.filter_by(id=id)
    else:
        eleves = professeur.eleves.order_by(Eleve.id_classe,Eleve.nom)
  
    # On introduit une pagination
    page = request.args.get('page', 1, type=int)
    eleves = eleves.paginate(page=page, per_page=1)
   

    # definition des filtres
    filtre = Filtre()

    # Eleve courant
    if len(eleves.items) == 0:
        return "CAS VIDE" 
        #"render_template("note/notes.html",eleves=eleves,id=id,items = filtre["items"],liste_selected=filtre["liste_selected"])"
    else:
        eleve = eleves.items[0]
     
    # Choix des items tous ou ceux de l'élève
    if eleve.liste is None:
        items = Item.query.all()
    else:
        items = Item.query.filter_by(id_liste = eleve.liste.id)
    
    # Si un filtre est selectionné cela surpasse le premier choix
    id_liste = request.args.get("liste")
    if id_liste is not None:
        items = Liste.query.get(id_liste).items

    
    # Remplis la form avec les notes existantes.
    form = TableNote()
    query = Note.query.filter_by(id_eleve=eleve.id)
    for item in items:
        noteform = CellForm()
        n1 = query.filter_by(id_item=item.id,niveau=1).first()
        n2 = query.filter_by(id_item=item.id,niveau=2).first()
        noteform.note_1 = n1.note if n1 is not None else 0
        noteform.note_2 = n2.note if n2 is not None else 0        
        form.notes.append_entry(noteform)

   
    return render_template("note/notes.html",eleves = eleves,id=id,form=form,items = items,liste_selected=filtre["liste_selected"])



@bp.route("/update_note/<id>")
def update_note(id): 
    id_item = int(request.args.get("id_change"))
    y = request.args.get("name_change")
    niveau = int(y[-1:])
    note_el = int(request.args.get(y))    
    
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