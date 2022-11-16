import csv
from app import app,db
from app.models import Eleve
# Création des élèves test
with open("data/hello.tab") as csv_file:
    csv_reader = csv.DictReader(csv_file,delimiter="\t")
    for row in csv_reader:
        
        classe = int(row["classe"][-2:])
        nom = row["nom"].capitalize()
        prenom = row["prenom"].capitalize()
        eleve = Eleve(nom=nom,prenom=prenom,id_classe=classe)
        db.session.add(eleve)
db.session.commit()

