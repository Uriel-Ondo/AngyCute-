from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db  # Assurez-vous que db est importé correctement

class Produit(db.Model):
    __tablename__ = 'produits'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    prix = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    categorie = db.Column(db.String(255), nullable=False)
    populaire = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Produit {self.nom}>"

class Commande(db.Model):
    __tablename__ = 'commandes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_total = db.Column(db.Numeric(10, 2), nullable=False)
    date_commande = db.Column(db.DateTime, default=datetime.utcnow)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Commande {self.id} - {self.nom}>"

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(15), unique=True, nullable=False)
    adresse = db.Column(db.Text, nullable=False)
    email_verifie = db.Column(db.Boolean, default=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='role_enum'), default='user')
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    commandes = db.relationship('Commande', backref='utilisateur', lazy=True)
    panier = db.relationship('Panier', backref='utilisateur', lazy=True)

    def __repr__(self):
        return f"<Utilisateur {self.nom} {self.prenom}>"

class Panier(db.Model):
    __tablename__ = 'paniers'

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)

    produit = db.relationship('Produit', backref='paniers')

    def __repr__(self):
        return f"<Panier {self.id} - {self.quantite}>"
