from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisation des extensions
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

# Initialisation de l'application Flask
def create_app():
    app = Flask(__name__)

    # Configuration Flask
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuration Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    # Dossier d'upload
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # Initialisation des extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Enregistrement des Blueprints
    from app.routes.views_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.routes.admin_routes import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app

# Création de l'application
app = create_app()
