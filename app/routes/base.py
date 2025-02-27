from flask import render_template
from app.fonctions.user_session import login_required
from app.fonctions.db_database import get_all_databases

def init_base(app):
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    @login_required
    def base(path):

        # Récupération de toutes les franchises
        all_franchises = get_all_databases()

        # Vérifier si le chemin correspond à une franchise
        if path in all_franchises:
            # Ici, vous pouvez ajouter une logique pour récupérer des données spécifiques à la franchise si nécessaire
            # Pour l'instant, nous passons simplement le nom de la franchise
            return render_template('franchise.html', franchise_name=path)

        return render_template('base.html', franchises=all_franchises)
