from functools import wraps
from flask import session, flash, redirect, url_for, current_app

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Vous devez être connecté pour effectuer cette action.", 'warning')
            return redirect(url_for('main.connexion'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash("Action non autorisée, vous n'êtes pas administrateur.", 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Vérification des extensions d'upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
