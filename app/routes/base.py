from flask import  render_template
from app.fonctions.db_authentification import login_required
from app.fonctions import get_all_franchises

# ------------- Initialisation de la route de base -------------
#
# Description:
# Ce code initialise une route de base pour une application web Flask.
# Il gère les requêtes vers la racine ('/') et les chemins dynamiques ('/<path:path>').
# La fonction `base` vérifie si le chemin correspond à une franchise connue et rend les modèles appropriés.
#
# Fonctionnement:
# 1. La fonction `init_base` configure une route de base pour l'application Flask.
# 2. La route '/' et les routes dynamiques '/<path:path>' sont définies pour gérer les requêtes entrantes.
# 3. La fonction `base` est décorée avec `@login_required` pour s'assurer que seuls les utilisateurs authentifiés peuvent accéder à ces routes.
# 4. La fonction `base` récupère toutes les franchises disponibles en utilisant `get_all_franchises()`.
# 5. Si le chemin correspond à une franchise connue, le modèle 'franchise.html' est rendu avec le nom de la franchise.
# 6. Sinon, le modèle 'base.html' est rendu avec la liste de toutes les franchises.
#
# Exemple d'utilisation:
# init_base(app)
#
# Arguments:
# - app: L'objet Flask représentant l'application web.
#
# Retour:
# - Aucun retour explicite, mais configure la route de base pour l'application.
#
# ------------------------------------------------

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
        else:
            return render_template('base.html', franchises=all_franchises)
