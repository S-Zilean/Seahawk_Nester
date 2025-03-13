from flask import render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, getall_NetworkScan_data
from app.fonctions.db_authentification import login_required

from app.fonctions.db_requests import db_connect


# Définition de la fonction init_harvester_dashboard qui prend 'app' comme argument
def init_harvester_dashboard(app):

    # Décorateur pour définir la route '/<nom_franchise>/<harvester_id>'
    @app.route('/<nom_franchise>/<harvester_id>')

    # Décorateur pour exiger que l'utilisateur soit authentifié
    @login_required

    # Définition de la fonction harvester_id qui prend 'nom_franchise' et 'harvester_id' comme arguments
    def harvester_id(nom_franchise, harvester_id):

        # Récupération de toutes les franchises disponibles
        all_franchises = get_all_franchises()

        # Vérification si le nom de la franchise est valide en le cherchant dans la liste des franchises
        if nom_franchise in all_franchises:

            # Récupération des rapports de scan pour la franchise spécifiée
            scan_reports = getall_NetworkScan_data(nom_franchise)

            # Vérification si la récupération des rapports de scan a échoué
            if scan_reports is None:
                # Retourner une erreur 500 si les données de scan ne peuvent pas être récupérées
                abort(500, description="Erreur lors de la récupération des données de scan")

            # Filtrage des données de scan pour ne conserver que celles du harvester spécifique
            scan_reports = {
                scan_id: details
                for scan_id, details in scan_reports.items()
                if details['Harvester_ID'] == int(harvester_id)
            }

            # Récupération des données de tous les harvesters pour la franchise spécifiée
            harvesters_data = getall_harvesters_data(nom_franchise)

            # Initialisation de la variable harvester_info à None
            harvester_info = None

            # Recherche des informations du harvester spécifique dans les données récupérées
            for harvester in harvesters_data.values():
                # Vérification si l'ID du harvester correspond à celui demandé
                if harvester.key['id'] == int(harvester_id):
                    # Stockage des informations du harvester trouvé
                    harvester_info = harvester.key
                    # Arrêt de la boucle une fois le harvester trouvé
                    break

            # Rendu du template 'harvester.html' avec les données récupérées
            return render_template('harvester.html', scan_reports=scan_reports, harvester_id=harvester_id, nom_franchise=nom_franchise, harvester_info=harvester_info)

        # Si la franchise n'existe pas, retourner une erreur 404
        abort(404, description="Franchise non trouvée")
