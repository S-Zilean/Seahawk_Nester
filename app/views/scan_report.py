from flask import render_template, Blueprint, request
from app.helper import get_table_data, get_all_databases
from app.helper.db_connection import db_connect
from app.helper.user_session import login_required
import json

def init_scan_report(app):
    @app.route('/scan_report')
    @login_required
    def rapport_de_scan():
        # Récupération de toutes les bases de données (franchises)
        franchises = get_all_databases()

        # Récupération de la franchise sélectionnée depuis les paramètres de la requête
        selected_franchise = request.args.get('franchise')

        # Initialisation d'un dictionnaire pour stocker les rapports de scan par Scan_ID
        scan_reports_dict = {}

        # Boucle sur chaque franchise ou seulement la franchise sélectionnée
        for franchise in franchises:
            if selected_franchise and franchise != selected_franchise:
                continue

            # Connexion à la base de données
            conn = db_connect()

            # Création d'un curseur pour exécuter des requêtes SQL
            cursor = conn.cursor()

            # Sélection de la base de données de la franchise actuelle
            cursor.execute(f"USE {franchise}")

            # Exécution d'une requête SQL pour récupérer les informations de scan
            cursor.execute("SELECT Scan_ID, Harvester_ID, Scan_Rapport, Scan_Date FROM NetworkScan ORDER BY Scan_Date DESC")

            # Récupération de toutes les lignes résultantes de la requête
            rows = cursor.fetchall()

            # Boucle sur chaque ligne de résultat
            for row in rows:
                # Décomposition de chaque ligne en variables
                scan_id, harvester_id, scan_rapport, scan_date = row

                try:
                    # Tentative de conversion du rapport de scan en JSON
                    scan_report = json.loads(scan_rapport)

                    # Ajout des informations supplémentaires à chaque entrée
                    for entry in scan_report:
                        entry['franchise'] = franchise
                        entry['Scan_ID'] = scan_id
                        entry['Harvester_ID'] = harvester_id
                        entry['Scan_Date'] = scan_date.strftime('%Y-%m-%d %H:%M:%S')

                    # Ajout des entrées du rapport de scan au dictionnaire par Scan_ID
                    if scan_id not in scan_reports_dict:
                        scan_reports_dict[scan_id] = {
                            'franchise': franchise,
                            'Scan_ID': scan_id,
                            'Harvester_ID': harvester_id,
                            'Scan_Date': scan_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'entries': []
                        }
                    scan_reports_dict[scan_id]['entries'].extend(scan_report)

                except json.JSONDecodeError as e:
                    # Gestion des erreurs de décodage JSON
                    print(f"Error decoding JSON: {e}")

            # Fermeture de la connexion à la base de données
            conn.close()

        # Conversion du dictionnaire en liste pour le rendu du template
        scan_reports = list(scan_reports_dict.values())

        # Rendu du template HTML avec les rapports de scan et les franchises
        return render_template('scan_report.html', scan_reports=scan_reports, franchises=franchises, selected_franchise=selected_franchise)
