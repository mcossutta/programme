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


def evalution_pdf(id):
    with open("templates/feuille_template_modele.tex", "r") as myfile :
        text = myfile.read()
    output_file_tex = "output/evaluation"+ str(id) +".tex"
    output_file_pdf = "output/evaluation"+ str(id) +".pdf"
    with open(output_file_tex,"w") as output :
        output.write(text)
    pdf = build_pdf(open(output_file_tex))
    pdf.save_to(output_file_pdf)
    return output_file_pdf