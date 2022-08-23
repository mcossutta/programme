# Run the script in flask shell

from app  import app, db
from app.models import Theme, Liste, Item , Professeur, Eleve, Classe
import csv 

# Création des thèmes
with open("data/theme.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if Theme.query.get(row["id"]) is None:
            theme = Theme(id = row["id"],nom = row["nom"])
            db.session.add(theme)

# Création des listes
with open("data/liste.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if Liste.query.get(row["id"]) is None:
            liste = Liste(id = row["id"],nom = row["nom"])
            db.session.add(liste)

# Création des items A,B,C
with open("data/item.csv")  as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if Item.query.get(row["id"]) is None:
            item = Item(id = row["id"],nom = row["nom"],id_theme=row["id_theme"],id_liste=row["id_liste"])
            db.session.add(item)

# Création des professeurs
with open("data/professeur.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if Professeur.query.get(row["id"]) is None:
            professeur = Professeur(id = row["id"], nom = row["nom"], prenom = row["prenom"], trigramme = row["trigramme"])
            db.session.add(professeur)


# Création des classes
with open("data/classe.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if Classe.query.get(row["id"]) is None:
            classe = Classe(id = row["id"], nom = row["nom"], id_professeur = row["id_professeur"])
        else:
            classe = Classe.query.get(row["id"])
            classe.id_professeur = row["id_professeur"]
            classe.nom = row["nom"]
            db.session.add(classe)

# Création des élèves test
with open("data/eleve_test.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if Eleve.query.get(row["id"]) is None:
            eleve = Eleve(id = row["id"], nom = row["nom"], prenom = row["prenom"], id_classe= row["id_classe"], id_professeur = row["id_professeur"])
            db.session.add(eleve)
        else:
            eleve = Eleve.query.get(row["id"])
            eleve.nom = row["nom"]
            eleve.prenom = row["prenom"]
            



# Commit des changements
db.session.commit()
