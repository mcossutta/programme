from app import db

# Les thèmes du bulletin arithmétique, géométrie, algèbre et grandeur et mesure 
class Theme(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), unique=True)
    
    items = db.relationship('Item',backref="theme")

    def __repr__(self):
        return '<Theme : {}>'.format(self.nom)


# Les eleves
class Eleve(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    classe = db.Column(db.String(10))
    id_professeur = db.Column(db.Integer,db.ForeignKey('professeur.id'))
    id_liste = db.Column(db.Integer,db.ForeignKey('liste.id'))
    notes = db.relationship('Note',backref="eleve")

# Les professeurs
class Professeur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    trigramme = db.Column(db.String(100))
    
    abonnements = db.relationship('Abonnement',backref="professeur")
    eleves = db.relationship('Eleve',backref="professeur")
    notes = db.relationship('Note',backref="professeur")


# Les listes auxquelles le prof est abonné --> seulement une table ?
class Abonnement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_professeur = db.Column(db.Integer,db.ForeignKey('professeur.id'))
    id_liste = db.Column(db.Integer,db.ForeignKey('liste.id'))


# Les listes d'items 
class Liste(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(100), unique = True)
    
    abonnements = db.relationship("Abonnement",backref="liste")
    items = db.relationship("Item",backref="liste")
    eleves = db.relationship("Eleve",backref="liste")

# les items du bulletin
class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    nom = db.Column(db.String(128))
    id_theme = db.Column(db.Integer,db.ForeignKey('theme.id'))
    id_liste = db.Column(db.Integer,db.ForeignKey('liste.id'))

    notes = db.relationship("Note",backref="item")
    

# Les notes du bulletin
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    niveau = db.Column(db.Integer)
    note = db.Column(db.Integer)
    id_item = db.Column(db.Integer,db.ForeignKey('item.id'))
    id_eleve = db.Column(db.Integer,db.ForeignKey('eleve.id'))
    id_professeur = db.Column(db.Integer,db.ForeignKey('professeur.id'))


