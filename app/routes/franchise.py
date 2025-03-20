from flask import render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, update_harvester_status
from app.fonctions.db_authentification import login_required


# ------------- Initialisation de la route pour les franchises -------------
#
# Description:
# Ce code initialise une route pour gérer les franchises dans une application web Flask.
# Il définit la route '/<nom_franchise>' pour accéder aux informations spécifiques d'une franchise.
# La fonction `franchise` vérifie la validité de la franchise, met à jour l'état des harvesters, et rend les données appropriées.
#
# Fonctionnement:
# 1. La fonction `init_franchise` configure une route pour les franchises dans l'application Flask.
# 2. La route '/<nom_franchise>' est définie pour gérer les requêtes spécifiques à une franchise.
# 3. La fonction `franchise` est décorée avec `@login_required` pour s'assurer que seuls les utilisateurs authentifiés peuvent accéder à cette route.
# 4. La fonction `franchise` récupère toutes les franchises disponibles en utilisant `get_all_franchises()`.
# 5. Elle vérifie si le nom de la franchise est valide en le cherchant dans la liste des franchises.
# 6. Si la franchise est valide, elle met à jour l'état des harvesters pour cette franchise en utilisant `update_harvester_status()`.
# 7. Elle tente de récupérer les données de tous les harvesters pour la franchise spécifiée en utilisant `getall_harvesters_data()`.
# 8. Si les données sont récupérées avec succès, elle rend le modèle 'franchise.html' avec les données des harvesters.
# 9. En cas d'erreur lors de la récupération des données, elle définit un message d'erreur et rend le modèle 'franchise.html' avec ce message.
# 10. Si la franchise n'existe pas, elle retourne une erreur 404.
#
# Exemple d'utilisation:
# init_franchise(app)
#
# Arguments:
# - app: L'objet Flask représentant l'application web.
#
# Retour:
# - Aucun retour explicite, mais configure la route pour les franchises dans l'application.
#
# ------------------------------------------------

def init_franchise(app):
    @app.route('/<nom_franchise>')
    @login_required
    def franchise(nom_franchise):
        all_franchises = get_all_franchises()

        if nom_franchise in all_franchises:
            update_harvester_status(nom_franchise)

            try:
                harvesters_data = getall_harvesters_data(nom_franchise)
                return render_template('franchise.html', harvester=harvesters_data, franchise_name=nom_franchise)
            except Exception as e:
                e = {"Hostname": "Erreur : Aucune donnée trouvée",
                    "ip": "Erreur : Aucune donnée trouvée",
                    "Etat": "Erreur : Aucune donnée trouvée"}

                return render_template('franchise.html', harvester=e, scan_report=e, franchise_name=nom_franchise)

        abort(404, description="Franchise non trouvée")

