from flask_socketio import emit
from flask import render_template
from app.db_helper import get_all_franchises, get_table_data
from app.helper.user_session  import login_required

login_required(any)  # Cette ligne semble incorrecte. `login_required` est un décorateur et ne doit pas être appelé directement avec un argument.

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
        franchises = get_all_franchises()  # Récupère toutes les franchises.
        table_dict = get_table_data('franchise_1', 'Harvester')  # Récupère les données de table pour 'franchise_1'.
        return render_template(
            'sondes.html',
            harvesters=[{'franchise': 'franchise_1', 'data': table_dict}],
            franchises=franchises
        )  # Rend le modèle HTML avec les données.

    @socketio.on('update_table')
    @login_required  # L'utilisateur doit être connecté pour déclencher cet événement.
    def handle_update_table(data):
        # Gestionnaire d'événements pour mettre à jour la table.
        franchises = data.get('franchises', [])  # Récupère la liste des franchises à partir des données reçues.
        all_tables = []  # Initialise une liste pour stocker les données de table.
        for franchise in franchises:
            table_dict = get_table_data(franchise, 'Harvester')  # Récupère les données de table pour chaque franchise.
            # Vérifie si les données sont nulles ou égales à 0.
            if any(cell is not None and cell != 0 for row in table_dict for cell in row):
                all_tables.append({'franchise': franchise, 'data': table_dict})  # Ajoute les données à la liste.
        emit('table_updated', {'harvesters': all_tables})  # Émet l'événement avec les données mises à jour.
