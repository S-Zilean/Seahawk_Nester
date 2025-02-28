from flask import redirect, render_template
from app.fonctions.user_session import login_required
from app.fonctions import get_all_franchises


def init_base(app):
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    @login_required
    def base(path):

        # Récupération de toutes les franchises
        all_franchises = get_all_franchises()

        # Vérifier si le chemin correspond à une franchise
        if path in all_franchises:
            return render_template('franchise.html', franchise_name=path)


        return render_template('base.html', franchises=all_franchises)
