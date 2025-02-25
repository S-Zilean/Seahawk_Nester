from flask import render_template, Blueprint
from app.helper import get_table_data, get_all_databases
from app.helper.db_connection import db_connect
from app.helper.user_session import login_required
import json

def init_scan_report(app):
    @app.route('/scan_report')
    @login_required

    # Définition de la fonction rapport_de_scan
    def rapport_de_scan():
        # Récupération de toutes les bases de données (franchises)
        franchises = get_all_databases()

        # Initialisation d'une liste pour stocker les rapports de scan
        scan_reports = []

        # Boucle sur chaque franchise
        for franchise in franchises:
            # Connexion à la base de données
            conn = db_connect()

            # Création d'un curseur pour exécuter des requêtes SQL
            cursor = conn.cursor()

            # Sélection de la base de données de la franchise actuelle
            cursor.execute(f"USE {franchise}")

            # Exécution d'une requête SQL pour récupérer les informations de scan
            cursor.execute("SELECT Scan_ID, Harvester_ID, Scan_Rapport, Scan_Date FROM NetworkScan")

            # Récupération de toutes les lignes résultantes de la requête
            rows = cursor.fetchall()

            # Boucle sur chaque ligne de résultat
            for row in rows:
                # Décomposition de chaque ligne en variables
                scan_id, harvester_id, scan_rapport, scan_date = row

                try:
                    # Tentative de conversion du rapport de scan en JSON
                    scan_report = json.loads(scan_rapport)

                    # Boucle sur chaque entrée du rapport de scan
                    for entry in scan_report:
                        # Ajout du nom de la franchise à chaque entrée
                        entry['franchise'] = franchise

                        # Ajout de l'ID du scan à chaque entrée
                        entry['Scan_ID'] = scan_id

                        # Ajout de l'ID du harvester à chaque entrée
                        entry['Harvester_ID'] = harvester_id

                        # Ajout de la date du scan formatée à chaque entrée
                        entry['Scan_Date'] = scan_date.strftime('%Y-%m-%d %H:%M:%S')

                    # Ajout des entrées du rapport de scan à la liste globale
                    scan_reports.extend(scan_report)

                except json.JSONDecodeError as e:
                    # Gestion des erreurs de décodage JSON
                    print(f"Error decoding JSON: {e}")

            # Fermeture de la connexion à la base de données
            conn.close()

        # Rendu du template HTML avec les rapports de scan
        return render_template('scan_report.html', scan_reports=scan_reports)
