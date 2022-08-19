from flask import  render_template ,request, session, flash, redirect, url_for, send_file, after_this_request
from app.eleve import bp
from app import db

from app.models import Eleve, Professeur, Item, Note, Liste, Classe
from app.helpers import tableau_note
import time

@bp.route("/eleves")
def eleves():
    if not session.get("id_professeur"):
        return redirect(url_for("login"))
    eleves = Eleve.query.filter_by(id_professeur=session["id_professeur"]).order_by(Eleve.id_classe,Eleve.nom)
    return render_template("eleve/eleves.html", eleves = eleves)        
        
@bp.route("/delete/<id>")
def delete_eleve(id):
    eleve = Eleve.query.get(id)
    db.session.delete(eleve)
    db.session.commit()
    return redirect(url_for("eleve.eleves"))




@bp.route("/update_eleve/<id>", methods=["POST","GET"])
def update_eleve(id):
    if request.method == "GET":
        eleve = Eleve.query.get(id)
        listes = Liste.query.all()
        classes = Professeur.query.get(session["id_professeur"]).classes
        return render_template("eleve/update_eleve.html",eleve = eleve, listes = listes, classes = classes)

    if request.method == "POST":
        eleve = Eleve.query.get(id)
        eleve.nom = request.form["nom"]
        eleve.prenom = request.form["prenom"]
        eleve.id_liste = int(request.form.get("liste"))
        eleve.id_classe = int(request.form.get("classe"))
        db.session.commit()
        return redirect(url_for("eleve.eleves"))


@bp.route("/add_eleve", methods=["POST","GET"])
def add_eleve():
    classes = Professeur.query.get(session["id_professeur"]).classes
    if request.method == "GET":
        return render_template("eleve/add_eleve.html", classes = classes)
    if request.method == "POST":
        eleve = Eleve()
        eleve.nom = request.form["nom"]
        eleve.prenom = request.form["prenom"]
        eleve.id_liste = int(request.form.get("liste"))
        eleve.id_professeur = session["id_professeur"]
        eleve.id_classe = int(request.form.get("classe"))
        db.session.add(eleve)
        db.session.commit()
        return redirect(url_for("eleve.eleves"))

