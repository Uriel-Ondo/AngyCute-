from flask import Blueprint, render_template, current_app
from app import db

# Définir un blueprint pour les erreurs
errors = Blueprint('errors', __name__)

# Gestionnaire d'erreur 404
@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Gestionnaire d'erreur générale
@errors.app_errorhandler(Exception)
def handle_exception(e):
    db.session.rollback()  # Annuler les transactions en cas d'erreur
    current_app.logger.error(f"Erreur : {e}")
    return render_template('500.html'), 500
