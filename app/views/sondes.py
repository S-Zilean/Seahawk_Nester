from flask_socketio import emit
from flask import render_template, request
from app.helper import get_all_databases, get_table_data
from app.helper.user_session import login_required

# Initialisation de la route
def init_sondes(app, socketio):
    # Initialise les routes et les gestionnaires d'événements pour l'application.
    # Args:
    # - app: Instance de l'application Flask.
    # - socketio: Instance de Flask-SocketIO pour gérer les WebSockets.

    @app.route('/sondes', methods=['GET'])
    @login_required  # L'utilisateur doit être connecté pour accéder à cette route.
    def table_list():
        # Route pour afficher la liste des sondes.
        try:
            franchises = get_all_databases()  # Récupère toutes les franchises.
            table_dict = get_table_data('franchise_1', 'Harvester')  # Récupère les données de table pour 'franchise_1'.
            return render_template(
                'sondes.html',
                harvesters=[{'franchise': 'franchise_1', 'data': table_dict}],
                franchises=franchises
            )  # Rend le modèle HTML avec les données.
        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")

    @socketio.on('connect')
    def handle_connect():
        try:
            print(f"Client {request.sid} connecté")
        except Exception as e:
            print(f"Erreur lors de la connexion : {e}")

    @socketio.on('disconnect')
    def handle_disconnect():
        try:
            print(f"Client {request.sid} déconnecté")
        except Exception as e:
            print(f"Erreur lors de la déconnexion : {e}")

    @socketio.on('update_table')
    @login_required  # L'utilisateur doit être connecté pour déclencher cet événement.
    def handle_update_table(data):
        # Gestionnaire d'événements pour mettre à jour la table.
        try:
            franchises = data.get('franchises', [])  # Récupère la liste des franchises à partir des données reçues.
            all_tables = []  # Initialise une liste pour stocker les données de table.
            for franchise in franchises:
                table_dict = get_table_data(franchise, 'Harvester')  # Récupère les données de table pour chaque franchise.
                # Vérifie si les données sont nulles ou égales à 0.
                if any(cell is not None and cell != 0 for row in table_dict for cell in row):
                    all_tables.append({'franchise': franchise, 'data': table_dict})  # Ajoute les données à la liste.
            emit('table_updated', {'harvesters': all_tables})  # Émet l'événement avec les données mises à jour.
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la table : {e}")

