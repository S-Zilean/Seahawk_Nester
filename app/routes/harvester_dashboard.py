from flask import Flask, render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, getall_NetworkScan_data
from app.fonctions.db_authentification import login_required
import json

from app.fonctions.db_requests import db_connect


def init_harvester_dashboard(app):
    @app.route('/<nom_franchise>/<harvester_id>')
    @login_required
    def harvester_id(nom_franchise, harvester_id):
        # Récupération de toutes les franchises
        all_franchises = get_all_franchises()

        # Vérifier si le nom de la franchise est valide
        if nom_franchise in all_franchises:
            # Récupérer toutes les données de scan pour la franchise, déjà triées par date
            all_scan_data = getall_NetworkScan_data(nom_franchise)

            if all_scan_data is None:
                abort(500, description="Erreur lors de la récupération des données de scan")

            # Filtrer les données pour ne conserver que celles du harvester spécifique
            scan_reports = {
                scan_id: details
                for scan_id, details in all_scan_data.items()
                if details['Harvester_ID'] == int(harvester_id)
            }

            return render_template('harvester.html', scan_reports=scan_reports, harvester_id=harvester_id)

        # Si la franchise n'existe pas, retourner une erreur 404
        abort(404, description="Franchise non trouvée")
