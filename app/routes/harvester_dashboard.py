from flask import render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, getall_NetworkScan_data
from app.fonctions.db_authentification import login_required

from app.fonctions.db_requests import db_connect


# ------------- Initialisation du tableau de bord des harvesters -------------
#
# Description:
# Ce code initialise une route pour le tableau de bord des harvesters dans une application web Flask.
# Il définit la route '/<nom_franchise>/<harvester_id>' pour accéder aux informations spécifiques d'un harvester au sein d'une franchise.
# La fonction `harvester_id` vérifie la validité de la franchise et du harvester, récupère les rapports de scan, et rend les données appropriées.
#
# Fonctionnement:
# 1. La fonction `init_harvester_dashboard` configure une route pour le tableau de bord des harvesters dans l'application Flask.
# 2. La route '/<nom_franchise>/<harvester_id>' est définie pour gérer les requêtes spécifiques à un harvester au sein d'une franchise.
# 3. La fonction `harvester_id` est décorée avec `@login_required` pour s'assurer que seuls les utilisateurs authentifiés peuvent accéder à cette route.
# 4. La fonction `harvester_id` récupère toutes les franchises disponibles en utilisant `get_all_franchises()`.
# 5. Elle vérifie si le nom de la franchise est valide en le cherchant dans la liste des franchises.
# 6. Si la franchise est valide, elle récupère les rapports de scan pour cette franchise en utilisant `getall_NetworkScan_data()`.
# 7. Si la récupération des rapports de scan échoue, elle retourne une erreur 500.
# 8. Elle filtre les données de scan pour ne conserver que celles du harvester spécifique.
# 9. Elle récupère les données de tous les harvesters pour la franchise spécifiée en utilisant `getall_harvesters_data()`.
# 10. Elle recherche les informations du harvester spécifique dans les données récupérées.
# 11. Elle rend le modèle 'harvester.html' avec les données des rapports de scan et les informations du harvester.
# 12. Si la franchise n'existe pas, elle retourne une erreur 404.
#
# Exemple d'utilisation:
# init_harvester_dashboard(app)
#
# Arguments:
# - app: L'objet Flask représentant l'application web.
#
# Retour:
# - Aucun retour explicite, mais configure la route pour le tableau de bord des harvesters dans l'application.
#
# ------------------------------------------------

def init_harvester_dashboard(app):
    @app.route('/<nom_franchise>/<harvester_id>')
    @login_required
    def harvester_id(nom_franchise, harvester_id):
        all_franchises = get_all_franchises()

        if nom_franchise in all_franchises:
            scan_reports = getall_NetworkScan_data(nom_franchise)

            if scan_reports is None:
                abort(500, description="Erreur lors de la récupération des données de scan")

            scan_reports = {
                scan_id: details
                for scan_id, details in scan_reports.items()
                if details['Harvester_ID'] == int(harvester_id)
            }

            harvesters_data = getall_harvesters_data(nom_franchise)
            harvester_info = None

            for harvester in harvesters_data.values():
                if harvester.key['id'] == int(harvester_id):
                    harvester_info = harvester.key
                    break

            return render_template('harvester.html', scan_reports=scan_reports, harvester_id=harvester_id, nom_franchise=nom_franchise, harvester_info=harvester_info)

        abort(404, description="Franchise non trouvée")
