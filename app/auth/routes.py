from flask import  render_template ,request, session, flash, redirect, url_for
from app.auth import bp
from app.models import Professeur




 

@bp.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    if request.method == "POST":
        trigramme = request.form["trigramme"]
        professeur = Professeur.query.filter_by(trigramme = trigramme).first()
        if professeur is None:
            flash("Ce trigramme n'est pas valable")
            return redirect(url_for("auth.login")) 
        else:
            session["id_professeur"] = professeur.id
            return redirect(url_for('index'))


@bp.route("/logout") 
def logout():
    if session.get("id_professeur"):
        session.pop("id_professeur")
    return render_template("logout.html")
    

