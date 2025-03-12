from flask import  render_template
from app.fonctions.db_authentification import login_required
from app.fonctions import get_all_franchises


# ------------- init_base -------------
#
# Description:
# Cette fonction initialise les routes de base pour une application Flask,
# en définissant le comportement pour la route principale et les sous-chemins.
#
# Fonctionnement:
# 1. Définit deux routes :
#    - La route principale '/' pour afficher la page de base.
#    - La route '/<path:path>' pour gérer les sous-chemins dynamiques.
# 2. Utilise le décorateur @login_required pour protéger l'accès à ces routes.
# 3. Récupère toutes les franchises en utilisant la fonction get_all_franchises().
# 4. Vérifie si le chemin (path) correspond à une franchise :
#    - Si oui, rend le template 'franchise.html' avec le nom de la franchise.
#    - Sinon, rend le template 'base.html' avec la liste des franchises.
#
# Exemple d'utilisation:
# - Accéder à la route '/' affiche la page de base avec toutes les franchises.
# - Accéder à la route '/NFL_IT' affiche la page de la franchise 'NFL_IT' si elle existe.
#
# Arguments:
# - app: L'instance de l'application Flask.
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
            update_harvester_status(nom_franchise)

        


        return render_template('base.html', franchises=all_franchises)
