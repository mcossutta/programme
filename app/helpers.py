from urllib.request import ProxyBasicAuthHandler
from latex import build_pdf
from flask import session,request
from app.models import Eleve, Item, Note, Professeur,Liste, Classe
import os, time


def Filtre():

  # Filtre des items par liste
    id_liste = request.args.get("liste")
    if id_liste is not None:
        items = Liste.query.get(id_liste).items
        liste_selected = Liste.query.get(id_liste)
    
    else:
        items = Item.query.all()
        print(items)
        liste_selected = None
    return {"items":items,"liste_selected":liste_selected}


def feuille_note_eleve(id_eleve):
    options = [{"value":0,"texte":""},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    eleve = Eleve.query.get(id_eleve)
    eleve_text = eleve.prenom + " " + eleve.nom +" ("+eleve.classe.nom+")"
    prof = Professeur.query.get(session["id_professeur"])
    texte_initial = {"1":"","2":"\n\multicolumn{3}{l}{\\textbf{Espace}}\\\\\n\\hline","3":"\multicolumn{3}{l}{\\textbf{Algèbre}}\\\\\n\\hline","4":"\multicolumn{3}{l}{\\textbf{Grandeurs et mesures}}\\\\\n\\hline"}
    texte_final = {"1":"","2":"\n\multicolumn{3}{l}{\\textbf{Espace}}\\\\\n\\hline","3":"\multicolumn{3}{l}{\\textbf{Algèbre}}\\\\\n\\hline","4":"\multicolumn{3}{l}{\\textbf{Grandeurs et mesures}}\\\\\n\\hline"}
  
    # pour chaque item on vérifie les notes
    for item in Item.query.all():
        note1 = Note.query.filter_by(id_eleve = id_eleve,id_item = item.id,niveau = 1).first()
        if note1 is None:
            note1 = 0
        else:
            note1 = note1.note
        note2 = Note.query.filter_by(id_eleve = id_eleve, id_item = item.id,niveau = 2).first()
        if note2 is None:
            note2 = 0
        else:
            note2 = note2.note
    # Si les notes ne sont pas vides on ajoute une ligne dans le bon theme
        if options[note1]["texte"]+options[note2]["texte"] != "":
            texte_final[str(item.theme.id)]+="\n"+item.nom+"&"+options[note1]["texte"]+"&"+options[note2]["texte"]+"\\\\"+"\n\\hline"    

    # On crée le texte final
    for x in texte_initial.keys():
        if texte_final[x] == texte_initial[x]:
            texte_final[x] = ""
    texte_final = "".join(texte_final.values())

    # Complète le texte :
    with open("app/templates_latex/contenu.tex", "r") as myfile :
        text = myfile.read()
        text = text.replace("$ELEVE$",eleve_text)
        text = text.replace("$PROF$",prof.prenom + " " +prof.nom)
        text = text.replace("exemple&A&A\\\\", texte_final)
    return text

def insert_text(text):
    output_file_tex = "evaluation"+ str(int(time.time())) +".tex"
    output_file_pdf = "evaluation"+ str(int(time.time()))     +".pdf"

    with open("app/templates_latex/feuille_template_modele.tex", "r") as myfile :
        text_base = myfile.read()
        text_base = text_base.replace("\\include{contenu}",text)
        print(text_base)
    with open(output_file_tex,"w") as output :
            output.write(text_base)
    pdf = build_pdf(open(output_file_tex))
    os.remove(output_file_tex)
    pdf.save_to(output_file_pdf)
    return output_file_pdf

def tableau_note(id_eleve):
    text = feuille_note_eleve(id_eleve)
    return insert_text(text)

def tableau_note_classe(id_classe):
    classe = Classe.query.get(id_classe)
    eleves = classe.eleves
    text="\n\\newpage\n".join([feuille_note_eleve(eleve.id) for eleve in eleves])
    output_file_tex = "evaluation"+ str(int(time.time())) +".tex"
    output_file_pdf = "evaluation"+ str(int(time.time()))     +".pdf"

    with open("app/templates_latex/feuille_template_modele.tex", "r") as myfile :
        text_base = myfile.read()
        text_base = text_base.replace("\\include{contenu}",text)
        print(text_base)
    with open(output_file_tex,"w") as output :
            output.write(text_base)
    pdf = build_pdf(open(output_file_tex))
    os.remove(output_file_tex)
    pdf.save_to(output_file_pdf)
    return output_file_pdf