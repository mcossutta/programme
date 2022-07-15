import pandas as pd
from latex import build_pdf


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
    with open("templates/page_de_garde_template.tex", "r") as myfile :
        text = myfile.read()
        text = text.replace("$CHAPITRE$", dict_pdf["num_chapter"] +" " + dict_pdf["chapitre"])
        text = text.replace("$OBJECTIF$",objectifs_item_string)
        text = text.replace("$THEME$", dict_pdf["theme"])
        text = text.replace("$SOUS_CHAPITRE$",dict_pdf["sous_chapitre"] )
        text = text.replace("$TRIGRAMME$",dict_pdf["trigramme"] )
    output_file_tex = "output/chapitre"+ dict_pdf["num_chapter"] +".tex"
    output_file_pdf = "output/chapitre"+ dict_pdf["num_chapter"] +".pdf"
    with open(output_file_tex,"w") as output :
        output.write(text)
    pdf = build_pdf(open(output_file_tex))
    pdf.save_to(output_file_pdf)
    return output_file_pdf





def tableau_note_1(id_eleve,conn,Eleves,Professeur,Note,Theme,Chapitre):
    options = [{"value":0,"texte":""},{"value":1,"texte":"NA"},{"value":2,"texte":"EA"},{"value":3,"texte":"A"},{"value":4,"texte":"M"}]
    eleve = conn.query(Eleves).filter(Eleves.ID==id_eleve).first()
    eleve_text = eleve.Prenom + " " + eleve.Nom +" ("+eleve.classe+")"
    prof = conn.query(Professeur).filter(Professeur.trigramme == eleve.trigramme).first()
    texte_initial = {"1":"","2":"\n\multicolumn{3}{l}{\\textbf{Espace}}\\\\\n\\hline","3":"\multicolumn{3}{l}{\\textbf{Algèbre}}\\\\\n\\hline","4":"\multicolumn{3}{l}{\\textbf{Grandeurs et mesures}}\\\\\n\\hline"}
    texte_final = {"1":"","2":"\n\multicolumn{3}{l}{\\textbf{Espace}}\\\\\n\\hline","3":"\multicolumn{3}{l}{\\textbf{Algèbre}}\\\\\n\\hline","4":"\multicolumn{3}{l}{\\textbf{Grandeurs et mesures}}\\\\\n\\hline"}
    for name,id_chapitre,id_theme in conn.query(Chapitre.name,Chapitre.id,Theme.id).join(Theme).all():
        note1 = conn.query(Note).filter(Note.id_eleve == id_eleve).\
                filter(Note.id_item == id_chapitre).filter(Note.niveau == 1).first().note
        note2 = conn.query(Note).filter(Note.id_eleve == id_eleve).\
                filter(Note.id_item == id_chapitre).filter(Note.niveau == 2).first().note
        if options[note1]["texte"]+options[note2]["texte"] != "":
            texte_final[str(id_theme)]+="\n"+name+"&"+options[note1]["texte"]+"&"+options[note2]["texte"]+"\\\\"+"\n\\hline"    
    for x in texte_initial.keys():
        if texte_final[x] == texte_initial[x]:
            texte_final[x] = ""
    texte_final = "".join(texte_final.values())
    # Complète le texte :
    with open("templates/feuille_template_modele.tex", "r") as myfile :
        text = myfile.read()
        text = text.replace("$ELEVE$",eleve_text)
        text = text.replace("$PROF$",prof.prenom + " " +prof.nom)
        text = text.replace("exemple&A&A\\\\", texte_final)
    output_file_tex = "output/evaluation"+ str(id) +".tex"
    output_file_pdf = "output/evaluation"+ str(id) +".pdf"
    with open(output_file_tex,"w") as output :
        output.write(text)
    pdf = build_pdf(open(output_file_tex))
    pdf.save_to(output_file_pdf)
    return output_file_pdf