import pandas as pd
from latex import build_pdf
from app.models import Theme, Eleve, Professeur, Item, Note


def produce_pdf(dict_pdf = {"objectifs":[],"num_chapter":"","chapitre":"","theme":"","sous_chapitre":"", "trigramme":""}):
    print(dict_pdf["chapitre"] == dict_pdf["sous_chapitre"])
    if dict_pdf["chapitre"] == dict_pdf["sous_chapitre"]:
        dict_pdf["sous_chapitre"] =""
    
    # liste des objectifs    
    objectifs_item_string = ""
    for objectif in dict_pdf["objectifs"] :
        objectifs_item_string = objectifs_item_string + "\n\item " + objectif
    objectifs_item_string = "\\begin{itemize}" + objectifs_item_string + "\end{itemize}"
    if objectifs_item_string == "\\begin{itemize}\end{itemize}":
        objectifs_item_string = "A COMPLETER"
   
    # Modification des templates
    with open("app/templates/page_de_garde_template.tex", "r") as myfile :
        text = myfile.read()
        text = text.replace("$CHAPITRE$", dict_pdf["num_chapter"] +" " + dict_pdf["chapitre"])
        text = text.replace("$OBJECTIF$",objectifs_item_string)
        text = text.replace("$THEME$", dict_pdf["theme"])
        text = text.replace("$SOUS_CHAPITRE$",dict_pdf["sous_chapitre"] )
        text = text.replace("$TRIGRAMME$",dict_pdf["trigramme"] )
    output_file_tex = "app/output/chapitre"+ dict_pdf["num_chapter"] +".tex"
    output_file_pdf = "app/output/chapitre"+ dict_pdf["num_chapter"] +".pdf"
    with open(output_file_tex,"w") as output :
        output.write(text)
    pdf = build_pdf(open(output_file_tex))
    pdf.save_to(output_file_pdf)
    return output_file_pdf





def tableau_note(id_eleve):
    options = [{"value":0,"texte":""},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    eleve = Eleve.query.get(id_eleve)
    eleve_text = eleve.prenom + " " + eleve.nom +" ("+eleve.classe+")"
    prof = eleve.professeur
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
    with open("app/templates/feuille_template_modele.tex", "r") as myfile :
        text = myfile.read()
        #text = text.replace("$ELEVE$",eleve_text)
        text = text.replace("$PROF$",prof.prenom + " " +prof.nom)
        text = text.replace("exemple&A&A\\\\", texte_final)
    output_file_tex = "app/output/evaluation"+ str(id_eleve) +".tex"
    output_file_pdf = "app/output/evaluation"+ str(id_eleve) +".pdf"
    with open(output_file_tex,"w") as output :
        output.write(text)
    pdf = build_pdf(open(output_file_tex))
    pdf.save_to(output_file_pdf)
    return output_file_pdf