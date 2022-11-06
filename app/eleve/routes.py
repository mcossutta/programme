from flask import  render_template ,request, session, redirect, url_for
from app.eleve import bp
from app import db
from app.models import Eleve, Professeur
from app.eleve.forms import AddEleve, UpdateEleve





@bp.route("/eleves")
def eleves():
    
    if not session.get("id_professeur"):
        return redirect(url_for("auth.login"))
    professeur = Professeur.query.get(session["id_professeur"])
    eleves = professeur.get_eleves()
    return render_template("eleve/eleves.html", eleves = eleves)        
    
@bp.route("/delete/<id>")
def delete_eleve(id):
    eleve = Eleve.query.get(id)
    db.session.delete(eleve)
    db.session.commit()
    return redirect(url_for("eleve.eleves"))




@bp.route("/update_eleve/<id>", methods=["POST","GET"])
def update_eleve(id):
    eleve = Eleve.query.get(id)
    classes = Professeur.query.get(session["id_professeur"]).classes
    form = UpdateEleve(obj=eleve)
    form.id_classe.choices = [(classe.id,classe.nom) for classe in classes]
    
    if request.method == "GET":       
        return render_template("eleve/update_eleve.html",eleve = eleve,form=form)

    if form.validate_on_submit:
        form.populate_obj(eleve)
        db.session.add(eleve)
        db.session.commit()
        return redirect(url_for("eleve.eleves"))
   
@bp.route("/add_eleve", methods=["POST","GET"])
def add_eleve():
    form = AddEleve()   
    if request.method == "GET":
        classes = Professeur.query.get(session["id_professeur"]).classes
        form.id_classe.choices = [(classe.id,classe.nom) for classe in classes]
        return render_template("eleve/add_eleve.html",form=form)

    if form.validate_on_submit:
        eleve = Eleve()
        eleve.id_professeur = session["id_professeur"]
        form.populate_obj(eleve)
        db.session.add(eleve)
        db.session.commit()
        return redirect(url_for("eleve.eleves"))

