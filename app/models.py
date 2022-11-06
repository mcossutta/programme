from app import db
from sqlalchemy.orm import object_session

# Les thèmes du bulletin arithmétique, géométrie, algèbre et grandeur et mesure 
class Theme(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), unique=True)
    
    items = db.relationship('Item',backref="theme",lazy="dynamic")

    def __repr__(self):
        return '<Theme : {}>'.format(self.nom)


# Les eleves
class Eleve(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    id_liste = db.Column(db.Integer,db.ForeignKey('liste.id'))
    id_classe = db.Column(db.Integer,db.ForeignKey('classe.id'))    
    notes = db.relationship('Note',backref="eleve",lazy="dynamic")

    def __repr__(self):
        return '<id : {} Nom : {}>'.format(self.id,self.nom)
    
# Les professeurs
class Professeur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    trigramme = db.Column(db.String(100))
    abonnements = db.relationship('Abonnement',backref="professeur",lazy="dynamic")
    notes = db.relationship('Note',backref="professeur",lazy="dynamic")
    classes = db.relationship('Classe',backref="professeur",lazy="dynamic")
    # Methode pour la requêtes des élèves
    def get_eleves(self):
        return Eleve.query.\
            join(Classe).filter(
                Classe.id_professeur == self.id,
                Eleve.id_classe == Classe.id
            ).order_by(Eleve.id_classe,Eleve.nom)
    def __repr__(self):
        return '<id : {} Trigramme : {}>'.format(self.id,self.trigramme)

# Les listes auxquelles le prof est abonné --> seulement une table ?
class Abonnement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_professeur = db.Column(db.Integer,db.ForeignKey('professeur.id'))
    id_liste = db.Column(db.Integer,db.ForeignKey('liste.id'))


# Les listes d'items 
class Liste(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(100), unique = True)
    
    abonnements = db.relationship("Abonnement",backref="liste",lazy="dynamic")
    items = db.relationship("Item",backref="liste",lazy="dynamic")
    eleves = db.relationship("Eleve",backref="liste",lazy="dynamic")
    
    def __repr__(self):
        return '<id : {} nom : {}>'.format(self.id,self.nom)


# les items du bulletin
class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    nom = db.Column(db.String(128))
    id_theme = db.Column(db.Integer,db.ForeignKey('theme.id'))
    id_liste = db.Column(db.Integer,db.ForeignKey('liste.id'))
    notes = db.relationship("Note",backref="item",lazy="dynamic")

    def __repr__(self):
        return '<id : {} Nom : {}>'.format(self.id,self.nom)

# Les notes du bulletin
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    niveau = db.Column(db.Integer)
    note = db.Column(db.Integer)
    id_item = db.Column(db.Integer,db.ForeignKey('item.id'))
    id_eleve = db.Column(db.Integer,db.ForeignKey('eleve.id'))
    id_professeur = db.Column(db.Integer,db.ForeignKey('professeur.id'))

    def __repr__(self):
        return '<niveau : {} id item : {} note : {}>'.format(self.niveau,self.id_item,self.note)

# les classes de l'école
class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique = True)
    id_professeur = db.Column(db.Integer,db.ForeignKey('professeur.id'))
    eleves = db.relationship("Eleve",backref="classe",lazy="dynamic")

    def __repr__(self):
        return '<id : {} Nom : {}>'.format(self.id,self.nom)