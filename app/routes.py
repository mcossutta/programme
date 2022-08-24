from flask import  render_template , session, redirect, url_for, request
from app import app
from app.models import  Professeur, Item,  Liste 

import time


def get_timestamp():
    return int(time.time())
app.jinja_env.globals['timestamp'] = get_timestamp
app.jinja_env.globals.update(zip=zip)

@app.context_processor
def listes():
    def Listes():
        return Liste.query.all()
    return  {"listes":Listes}


@app.route("/")
def index():
    if session.get("id_professeur"):
        professeur = Professeur.query.get(session["id_professeur"])
        return render_template("index.html", prof = professeur)
    else:
        return redirect(url_for('auth.login'))
 

@app.route("/items")
def items():
    if not session.get("id_professeur"):
        return redirect(url_for("auth.login"))
    
    # Filtre items
    id_liste = request.args.get("liste")
    if id_liste is not None:
        items = Liste.query.get(id_liste).items
    else:
        items = Item.query.all()
    
    return render_template("item.html",items = items)

