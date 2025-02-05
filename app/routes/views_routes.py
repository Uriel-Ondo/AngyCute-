from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Message
from app import mail, db
from functools import wraps
from app.utils import login_required
from app.models import Produit, Utilisateur, Panier, db
import os
from app.routes.forms_routes import ConnexionForm, InscriptionForm, MotDePasseOublieForm, ReinitialisationMotDePasseForm, ContactForm


main = Blueprint('main', __name__)

# Route principale
@main.route('/')
def index():
    produits_populaires = Produit.query.filter_by(populaire=True).all()
    return render_template('index.html', produits_populaires=produits_populaires)

# Route produits
@main.route('/produits')
def produits():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    produits = Produit.query.paginate(page=page, per_page=per_page, error_out=False)
    total_pages = produits.pages

    # Organisation des produits par catégorie pour affichage
    produits_par_categorie = {}
    for produit in produits.items:
        categorie = produit.categorie
        if categorie not in produits_par_categorie:
            produits_par_categorie[categorie] = []
        produits_par_categorie[categorie].append(produit)

    return render_template('produits.html', produits_par_categorie=produits_par_categorie, page=page, total_pages=total_pages)

# Barre de recherche
@main.route('/recherche', methods=['GET'])
def recherche():
    query = request.args.get('q', '')  # Récupère le paramètre de recherche 'q'
    if not query:
        flash("Veuillez entrer un terme de recherche.", 'warning')
        return redirect(url_for('main.produits'))

    # Requête SQL pour rechercher des produits par nom ou description
    produits = Produit.query.filter(
        (Produit.nom.ilike(f"%{query}%")) | 
        (Produit.description.ilike(f"%{query}%"))
    ).all()

    return render_template('recherche.html', produits=produits, query=query)
# Routes pour Mode (généralisation avec paramètre de genre)
@main.route('/produits/mode/<genre>')
def produits_mode(genre):
    produits = Produit.query.filter_by(categorie=f'Mode ({genre.capitalize()})').all()
    return render_template('categorie.html', produits=produits, categorie=f'Mode ({genre.capitalize()})')
# Routes pour soins & beauté
@main.route('/produits/sante-beaute/maquillage')
def produits_sante_beaute_maquillage():
    produits = Produit.query.filter_by(categorie='Santé & Beauté (Maquillage)').all()
    return render_template('categorie.html', produits=produits, categorie='Santé & Beauté (Maquillage)')

@main.route('/produits/sante-beaute/soins')
def produits_sante_beaute_soins():
    produits = Produit.query.filter_by(categorie='Santé & Beauté (Soins)').all()
    return render_template('categorie.html', produits=produits, categorie='Santé & Beauté (Soins)')

@main.route('/produits/sante-beaute/parfum')
def produits_sante_beaute_parfum():
    produits = Produit.query.filter_by(categorie='Santé & Beauté (Parfum)').all()
    return render_template('categorie.html', produits=produits, categorie='Santé & Beauté (Parfum)')

# Route pour produit Maison & Bureau
@main.route('/produits/maison-bureau')
def produits_maison_bureau():
    produits = Produit.query.filter_by(categorie='Maison & Bureau').all()
    return render_template('categorie.html', produits=produits, categorie='Maison & Bureau')

# Inscription, connexion et déconnexion
@main.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        # Vérifier si l'email existe déjà
        if Utilisateur.query.filter_by(email=form.email.data).first():
            flash("Cet email est déjà utilisé.", 'danger')
            return redirect(url_for('main.inscription'))
        
        # Enregistrer l'utilisateur
        utilisateur = Utilisateur(
            email=form.email.data,
            nom=form.nom.data,
            prenom=form.prenom.data,
            telephone=form.telephone.data,
            adresse=form.adresse.data,
            mot_de_passe=generate_password_hash(form.mot_de_passe.data)
        )
        db.session.add(utilisateur)
        db.session.commit()
        
        flash("Inscription réussie !", 'success')
        return redirect(url_for('main.connexion'))
    
    return render_template('inscription.html', form=form)

@main.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = ConnexionForm()
    if form.validate_on_submit():
        email = form.email.data
        mot_de_passe = form.mot_de_passe.data
        user = Utilisateur.query.filter_by(email=email).first()
        if user and check_password_hash(user.mot_de_passe, mot_de_passe):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash("Connexion réussie !", 'success')
            return redirect(url_for('main.produits'))
        flash("Email ou mot de passe incorrect.", 'error')
    return render_template('connexion.html', form=form)


@main.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Déconnexion réussie.", 'success')
    return redirect(url_for('main.index'))

#mot de passe oublie
@main.route('/mot_de_passe_oublie', methods=['GET', 'POST'])
def mot_de_passe_oublie():
    form = MotDePasseOublieForm()
    if form.validate_on_submit():
        email = form.email.data
        user = Utilisateur.query.filter_by(email=email).first()

        if user:
            token = generate_password_hash(email)  # Générer un token sécurisé
            reset_url = url_for('main.reinitialiser_mot_de_passe', token=token, _external=True)
            msg = Message(
                'Réinitialisation de votre mot de passe',
                sender='noreply@demo.com',
                recipients=[email]
            )
            msg.body = f"Pour réinitialiser votre mot de passe, cliquez sur ce lien : {reset_url}"
            mail.send(msg)

            flash("Un email avec les instructions de réinitialisation a été envoyé.", 'success')
        else:
            flash("Aucun compte trouvé avec cet email.", 'danger')

        return redirect(url_for('main.mot_de_passe_oublie'))

    return render_template('mot_de_passe_oublie.html', form=form)

# Réinitialiser mot de passe
@main.route('/reinitialiser_mot_de_passe/<token>', methods=['GET', 'POST'])
def reinitialiser_mot_de_passe(token):
    form = ReinitialisationMotDePasseForm()

    if form.validate_on_submit():
        email = form.email.data
        mot_de_passe = form.mot_de_passe.data

        utilisateur = Utilisateur.query.filter_by(email=email).first()

        if utilisateur:
            utilisateur.mot_de_passe = generate_password_hash(mot_de_passe)
            db.session.commit()
            flash("Votre mot de passe a été réinitialisé avec succès.", 'success')
            return redirect(url_for('main.connexion'))
        else:
            flash("Utilisateur non trouvé.", 'danger')

    return render_template('reinitialiser_mot_de_passe.html', form=form, token=token)

# Route pour afficher le panier
@main.route('/panier')
@login_required
def panier():
    panier_items = Panier.query.filter_by(utilisateur_id=session.get('user_id')).all()
    total_general = sum(item.produit.prix * item.quantite for item in panier_items)
    return render_template('panier.html', panier=panier_items, total_general=total_general)

# Route pour ajouter un produit au panier
@main.route('/ajouter-panier/<int:produit_id>')
@login_required
def ajouter_panier(produit_id):
    produit = Produit.query.get(produit_id)
    if produit:
        panier_item = Panier.query.filter_by(utilisateur_id=session.get('user_id'), produit_id=produit.id).first()
        if panier_item:
            panier_item.quantite += 1
        else:
            panier_item = Panier(utilisateur_id=session.get('user_id'), produit_id=produit.id, quantite=1)
            db.session.add(panier_item)
        db.session.commit()
        flash("Produit ajouté au panier.", 'success')
    else:
        flash("Produit introuvable.", 'error')
    return redirect(url_for('main.produits'))

# Route pour supprimer un produit du panier
@main.route('/supprimer-panier/<int:id>')
@login_required
def supprimer_panier(id):
    panier_item = Panier.query.filter_by(id=id, utilisateur_id=session['user_id']).first()
    if panier_item:
        db.session.delete(panier_item)
        db.session.commit()
        flash("Produit supprimé du panier.", 'success')
    else:
        flash("Produit introuvable dans le panier.", 'error')
    return redirect(url_for('main.panier'))

# Route pour passer une commande
@main.route('/commander', methods=['POST'])
@login_required
def commander():
    panier_items = Panier.query.filter_by(utilisateur_id=session.get('user_id')).all()
    
    if not panier_items:
        flash("Votre panier est vide.", 'error')
        return redirect(url_for('main.panier'))
    
    # Récupérer les informations de l'utilisateur
    utilisateur = Utilisateur.query.get(session['user_id'])
    user_email = utilisateur.email
    admin_email = 'ondondoutoumouuriel@gmail.com'  # Remplacez par l'email de l'admin

    # Récupérer les détails des produits dans le panier
    panier_details = []
    for item in panier_items:
        produit = item.produit
        panier_details.append({
            'nom': produit.nom,
            'description': produit.description,
            'prix': float(produit.prix),
            'quantite': item.quantite,
            'total': float(produit.prix) * item.quantite
        })

    # Calcul du total général de la commande
    total_general = sum(item['total'] for item in panier_details)

    # Détails de la commande à envoyer à l'utilisateur
    commande_details = {
        'utilisateur': {
            'nom': utilisateur.nom,
            'prenom': utilisateur.prenom,
            'email': user_email,
            'telephone': utilisateur.telephone,
            'adresse': utilisateur.adresse
        },
        'panier': panier_details,
        'total_general': total_general
    }

    # Envoyer l'email de confirmation à l'utilisateur
    msg_user = Message('Confirmation de votre commande', sender='noreply@demo.com', recipients=[user_email])
    msg_user.html = render_template('confirmation_commande.html', **commande_details)
    mail.send(msg_user)

    # Envoyer l'email d'avis de commande à l'admin (détails inclus)
    msg_admin = Message('Nouvelle commande reçue', sender='noreply@demo.com', recipients=[admin_email])
    msg_admin.body = f"""
    Nouvelle commande reçue :
    
    Utilisateur : {utilisateur.nom} {utilisateur.prenom}
    Email : {user_email}
    Téléphone : {utilisateur.telephone}
    Adresse : {utilisateur.adresse}
    
    Détails du panier :
    """
    for item in panier_details:
        msg_admin.body += (
            f"\n- Produit : {item['nom']}\n"
            f"  Description : {item['description']}\n"
            f"  Quantité : {item['quantite']}\n"
            f"  Prix unitaire : {item['prix']}XAF\n"
            f"  Total : {item['total']}XAF\n"
        )
    
    msg_admin.body += f"\n\nTotal général : {total_general}XAF"
    mail.send(msg_admin)

    # Nettoyer le panier après la commande
    Panier.query.filter_by(utilisateur_id=session['user_id']).delete()
    db.session.commit()

    flash("Commande passée avec succès.", 'success')
    return render_template('confirmation_commande.html', **commande_details)

# Route pour nous contacter
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        nom = form.nom.data
        email = form.email.data
        sujet = form.sujet.data
        message = form.message.data

        # Envoi d'un email
        msg = Message(sujet, sender=email, recipients=['contact@visitech.com'])
        msg.body = f"Message de {nom} ({email}):\n\n{message}"
        mail.send(msg)

        flash("Votre message a été envoyé avec succès.", 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html', form=form)

# A propos
@main.route('/a-propos')
def a_propos():
    return render_template('a_propos.html')
