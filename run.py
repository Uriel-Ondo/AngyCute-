from app import create_app, db
from flask_migrate import Migrate

# Création de l'application Flask
app = create_app()

# Configuration de Flask-Migrate pour gérer les migrations de la base de données
migrate = Migrate(app, db)

# Point d'entrée principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
