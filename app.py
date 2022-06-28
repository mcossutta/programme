from flask import Flask, render_template ,request, send_from_directory, session, flash, redirect, url_for
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from code1.helpers import produce_pdf
from latex import build_pdf


# Fonction pour la production du tex de page de garde.



#  export FLASK_ENV=development pour mode development dans le shell
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['TESTING'] = True

    


workingdir = os.path.abspath(os.getcwd())



# Connection à la base de donnée et définition des tables pour sqlalchemy
engine = create_engine('sqlite:///data/base_chapitre.db', convert_unicode=True, echo=False,connect_args={"check_same_thread": False})
Base = declarative_base()
Base.metadata.reflect(engine)
class Chapitre(Base):
    __table__ = Base.metadata.tables['items_C']
class Sous_Chapitre(Base):
    __table__ = Base.metadata.tables['souschapitre_C']
class Objectifs(Base):
    __table__ = Base.metadata.tables['objectifs_C']
class Theme(Base):
    __table__ = Base.metadata.tables["theme"]
class Eleves(Base):
    __table__ = Base.metadata.tables["eleves"]
class Note(Base):
    __table__ = Base.metadata.tables["note"]

# Connection la base de donnée
db_session = scoped_session(sessionmaker(bind=engine))



# page par défaut login si pas loguer sinon une dashboard
@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/logout") 
def logout():
    session.pop("username")
    return render_template("index.html")
    

@app.route("/chapitres")
def chapitres():
    #Liste des chapitres 
    L = [{"name":item.name, "id":str(item.id)} for item in db_session.query(Chapitre)]
    
    #Liste des sous-chapitre
    L1 = [{"name":item.name,"id":str(item.id)} for item in db_session.query(Sous_Chapitre)]
    
    # Tableau chapitre-sous-chapitre theme
    L2 = [{"name_sc": item1.name, "name_c":item2.name, "theme":item3.name } for item1,item2,item3 in db_session.\
        query(Sous_Chapitre,Chapitre,Theme).filter(Sous_Chapitre.id_item == Chapitre.id).\
            filter(Chapitre.id_theme==Theme.id)]
    db_session.close()
    return render_template("chapitres.html", liste_chapitre = L,liste_sous_chapitre =L1,liste_objectif =L2)



# Cette page devrait exporter un chapitre à partir du sous-chapitre.
@app.route("/pagegardepdf")
def page_garde_pdf():
    sous_chapitre = request.args.get("sous_chapitre")
    if sous_chapitre == "0":
        flash("Choisir un chapitre")
        return redirect(url_for("chapitres"))
    filepath = workingdir
    dict_pdf = {"objectifs":[],"num_chapter":"","chapitre":"","theme":"","sous_chapitre":""}
    dict_pdf["num_chapter"] = str(db_session.query(Sous_Chapitre).\
        filter(Sous_Chapitre.id ==sous_chapitre)[0].id_item)
    dict_pdf["chapitre"] = db_session.query(Chapitre).\
        filter(Chapitre.id == dict_pdf["num_chapter"])[0].name
    dict_pdf["sous_chapitre"] = db_session.query(Sous_Chapitre).\
        filter(Sous_Chapitre.id ==sous_chapitre)[0].name
    id_theme = db_session.query(Chapitre).\
        filter((Chapitre.id == dict_pdf["num_chapter"]))[0].id_theme
    dict_pdf["theme"] = db_session.query(Theme).filter(Theme.id == id_theme)[0].name
    dict_pdf["objectifs"] = [obj.objectifs for obj in db_session.query(Objectifs).\
        filter(Objectifs.id_sc ==sous_chapitre)]
    dict_pdf["trigramme"] = session["username"]
    db_session.close()
    return send_from_directory(filepath, produce_pdf(dict_pdf))


@app.route("/evaluationpdf/<id>")
def evaluationpdf(id):
    options = [{"value":0,"texte":""},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    filepath = workingdir
    # Eleve
    eleve = db_session.query(Eleves).filter(Eleves.ID==id).all()[0]
    eleve_text = eleve.Prenom + " " + eleve.Nom +" ("+eleve.classe+")"
    # Arithmétique
    ari = ""
    for item in range(5):
        name = db_session.query(Chapitre).filter(Chapitre.id == item+1)[0].name
        note1 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+1).filter(Note.niveau == 1).all()[0].note
        note2 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+1).filter(Note.niveau == 2).all()[0].note
        if options[note1]["texte"]+options[note2]["texte"] != "":
            ari=ari+"\n"+name+"&"+options[note1]["texte"]+"&"+options[note2]["texte"]+"\\\\"+"\n\\hline"
    # Espace
    espace = "\n\multicolumn{3}{l}{\\textbf{Espace}}\\\\\n\\hline"
    for item in range(4):
        name =db_session.query(Chapitre).filter(Chapitre.id == item + 6)[0].name
        note1 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+6).filter(Note.niveau == 1).all()[0].note
        note2 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+6).filter(Note.niveau == 2).all()[0].note
        if options[note1]["texte"]+options[note2]["texte"] != "":
            espace=espace+"\n"+name+"&"+options[note1]["texte"]+"&"+options[note2]["texte"]+"\\\\"+"\n\\hline"
    if espace == "\n\multicolumn{3}{l}{\\textbf{Espace}}\\\\\n\\hline":
            espace = ""
    # Algèbre
    algebre = "\multicolumn{3}{l}{\\textbf{Algèbre}}\\\\\n\\hline"
    for item in range(3):
        name =db_session.query(Chapitre).filter(Chapitre.id == item + 10)[0].name
        note1 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+10).filter(Note.niveau == 1).all()[0].note
        note2 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+10).filter(Note.niveau == 2).all()[0].note
        if options[note1]["texte"]+options[note2]["texte"] != "":
            algebre=algebre+"\n"+name+"&"+options[note1]["texte"]+"&"+options[note2]["texte"]+"\\\\"+"\n\\hline"
        if algebre == "\multicolumn{3}{l}{\\textbf{Algèbre}}\\\\\n\\hline":
            algebre = ""
    # Grandeur et mesure
    gm = "\multicolumn{3}{l}{\\textbf{Grandeurs et mesures}}\\\\\n\\hline"
    for item in range(4):
        name =db_session.query(Chapitre).filter(Chapitre.id == item + 13)[0].name
        note1 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+13).filter(Note.niveau == 1).all()[0].note
        note2 = db_session.query(Note).filter(Note.id_eleve == id).\
            filter(Note.id_item == item+13).filter(Note.niveau == 2).all()[0].note
        if options[note1]["texte"]+options[note2]["texte"] != "":
            gm=gm+"\n"+name+"&"+options[note1]["texte"]+"&"+options[note2]["texte"]+"\\\\"+"\n\\hline"
        if gm == "\multicolumn{3}{l}{\\textbf{Grandeurs et mesures}}\\\\\n\\hline":
            gm = ""
    with open("templates/feuille_template_modele.tex", "r") as myfile :
        text = myfile.read()
        text = text.replace("$ELEVE$",eleve_text)
        text = text.replace("exemple&A&A\\\\", ari+espace+algebre+gm)
    output_file_tex = "output/evaluation"+ str(id) +".tex"
    output_file_pdf = "output/evaluation"+ str(id) +".pdf"
    with open(output_file_tex,"w") as output :
        output.write(text)
    pdf = build_pdf(open(output_file_tex))
    pdf.save_to(output_file_pdf)
    db_session.close()
    return send_from_directory(filepath, output_file_pdf)




@app.route("/eleves")
def eleves():
    Dict_eleves =[{"Nom":item.Nom, "Prenom":item.Prenom, "classe":item.classe, "id":item.ID} for item in db_session.query(Eleves)]
    print(Dict_eleves)
    return render_template("eleves.html", Dict_eleves = Dict_eleves)


@app.route("/note/<id>")
def note(id):
    options = [{"value":0,"texte":"Pas d'évaluation"},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    Dict_eleve = {}
    Dict_eleve["id"] = id
    Dict_eleve["nom"] = db_session.query(Eleves).filter(Eleves.ID == Dict_eleve["id"])[0].Nom
    Dict_eleve["prenom"] = db_session.query(Eleves).filter(Eleves.ID == Dict_eleve["id"])[0].Prenom
    Liste_chapitre = [{"name":item.name,"id":item.id} for item in db_session.query(Chapitre)]
    
    # Liste des notes vides
    selected_value = {}
    for x in Liste_chapitre:
        selected_value[str(x["id"])+"A"] = 0
        selected_value[str(x["id"])+"B"] = 0
    
    # Liste des notes complétées avec la DB
    for x in db_session.query(Note).filter(Note.id_eleve==int(Dict_eleve["id"])).all():
        if x.niveau == 1:
            selected_value[str(x.id_item)+"A"] = x.note
        else:
            selected_value[str(x.id_item)+"B"] = x.note
    db_session.close()
    return render_template("note.html",Dict_eleve = Dict_eleve, Liste_chapitre = Liste_chapitre, selected_value=selected_value, options=options)


@app.route("/update_note/<id>")
def update_note(id): 
    for x in request.args:
        notes = db_session.query(Note).filter(Note.id_eleve ==int(id))
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
            db_session.add(note)
            db_session.commit()
        else:
            notes.first().note = int(request.args.get(x))
            db_session.commit()
       
    return redirect(url_for('eleves'))


if app.name =="__main__":
    app.run(debug=True)