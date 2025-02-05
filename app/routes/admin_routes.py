from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Message
from functools import wraps
from app.utils import login_required, admin_required, allowed_file
from app.models import Produit, Utilisateur, Panier, db
import os


admin = Blueprint('admin', __name__)

# Tableau de bord
@admin.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    utilisateurs = Utilisateur.query.paginate(page=page, per_page=per_page, error_out=False)
    total_utilisateurs = utilisateurs.pages
    return render_template('admin_dashboard.html', utilisateurs=utilisateurs.items, total_utilisateurs=total_utilisateurs, page=page)

# Route pour créer un utilisateur
@admin.route('/admin/create-user', methods=['POST'])
@login_required
@admin_required
def create_user():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    telephone = request.form['telephone']
    adresse = request.form['adresse']
    role = request.form['role']
    mot_de_passe = request.form['mot_de_passe']
    confirmation_mot_de_passe = request.form['confirmation_mot_de_passe']

    if mot_de_passe != confirmation_mot_de_passe:
        flash("Les mots de passe ne correspondent pas.", 'error')
        return redirect(url_for('admin.admin_dashboard'))

    mot_de_passe_hashed = generate_password_hash(mot_de_passe)

    utilisateur = Utilisateur(
        nom=nom,
        prenom=prenom,
        email=email,
        telephone=telephone,
        adresse=adresse,
        role=role,
        mot_de_passe=mot_de_passe_hashed
    )
    db.session.add(utilisateur)
    db.session.commit()

    flash("Utilisateur créé avec succès.", 'success')
    return redirect(url_for('admin.admin_dashboard'))

# Route pour supprimer un utilisateur
@admin.route('/admin/supprimer-utilisateur/<int:id>', methods=['POST'])
@login_required
@admin_required
def supprimer_utilisateur(id):
    utilisateur = Utilisateur.query.get(id)
    if utilisateur:
        db.session.delete(utilisateur)
        db.session.commit()
        flash("Utilisateur supprimé avec succès.", 'success')
    else:
        flash("Utilisateur introuvable.", 'error')
    return redirect(url_for('admin.admin_dashboard'))

# Route pour ajouter un produit (accessible par admin)
@admin.route('/ajouter-produit', methods=['POST'])
@login_required
@admin_required
def ajouter_produit():
    # Récupération des données du formulaire
    nom = request.form['nom']
    prix = request.form['prix']
    description = request.form['description']
    categorie = request.form.get('categorie')
    image = request.files.get('image')

    # Vérification de l'image
    if not image or not allowed_file(image.filename):
        flash("Format d'image non autorisé ou image absente.")
        return redirect(url_for('main.produits'))

    # Sauvegarde de l'image
    filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    # Récupération de l'ID de l'administrateur connecté depuis la session
    admin_id = session.get('user_id')
    if not admin_id:
        flash("Une erreur est survenue. Veuillez vous reconnecter.", 'error')
        return redirect(url_for('main.produits'))

    # Création du produit avec admin_id
    produit = Produit(
        nom=nom,
        prix=prix,
        description=description,
        image_path=filename,
        categorie=categorie,
        admin_id=admin_id  # Ajout de l'administrateur
    )
    db.session.add(produit)
    db.session.commit()

    flash("Produit ajouté avec succès.", 'success')
    return redirect(url_for('main.produits'))

# Fonction pour modifier produit
@admin.route('/modifier-produit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def modifier_produit(id):
    produit = Produit.query.get(id)
    if not produit:
        flash("Produit introuvable.", 'error')
        return redirect(url_for('main.produits'))

    if request.method == 'POST':
        produit.nom = request.form['nom']
        produit.prix = request.form['prix']
        produit.description = request.form['description']
        image = request.files.get('image')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            produit.image_path = filename

        db.session.commit()
        flash("Produit mis à jour avec succès.", 'success')
        return redirect(url_for('main.produits'))

    return render_template('modifier_produit.html', produit=produit)

# Route pour supprimer un produit
@admin.route('/supprimer-produit/<int:id>')
@login_required
@admin_required
def supprimer_produit(id):
    produit = Produit.query.get(id)
    if produit:
        db.session.delete(produit)
        db.session.commit()
        flash("Produit supprimé avec succès.", 'success')
    else:
        flash("Produit introuvable.", 'error')
    return redirect(url_for('main.produits'))

# Route pour rendre un produit populaire
@admin.route('/rendre-populaire/<int:id>')
@login_required
@admin_required
def rendre_populaire(id):
    produit = Produit.query.get(id)
    if produit:
        produit.populaire = True
        db.session.commit()
        flash("Produit rendu populaire avec succès", 'success')
    else:
        flash("Produit introuvable.", 'error')
    return redirect(url_for('main.produits'))

# Route pour rendre un produit non populaire
@admin.route('/rendre-non-populaire/<int:id>')
@login_required
@admin_required
def rendre_non_populaire(id):
    produit = Produit.query.get(id)
    if produit:
        produit.populaire = False
        db.session.commit()
        flash("Produit rendu non populaire avec succès", 'success')
    else:
        flash("Produit introuvable.", 'error')
    return redirect(url_for('main.produits'))

# Route pour supprimer un produit des produits populaires
@admin.route('/supprimer-produit-populaire/<int:id>')
@login_required
@admin_required
def supprimer_produit_populaire(id):
    produit = Produit.query.get(id)
    if produit:
        produit.populaire = False
        db.session.commit()
        flash("Produit retiré des produits populaires avec succès.", 'success')
    else:
        flash("Produit introuvable.", 'error')
    return redirect(url_for('main.index'))
