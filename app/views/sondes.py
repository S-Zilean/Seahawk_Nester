from flask_socketio import emit
from flask import render_template
from app.db_helper import get_all_franchises, get_table_data

# Initialisation de la route
def init_sondes(app, socketio):
    @app.route('/liste_sondes', methods=['GET'])
    def table_list():
        franchises = get_all_franchises()
        table_dict = get_table_data('franchise_1', 'Harvester')
        return render_template('liste_sondes.html', harvesters=[{'franchise': 'franchise_1', 'data': table_dict}], franchises=franchises)

    @socketio.on('update_table')
    def handle_update_table(data):
        franchises = data.get('franchises', [])
        all_tables = []
        for franchise in franchises:
            table_dict = get_table_data(franchise, 'Harvester')
            # Vérifiez si les données sont nulles ou égales à 0
            if any(cell is not None and cell != 0 for row in table_dict for cell in row):
                all_tables.append({'franchise': franchise, 'data': table_dict})
        emit('table_updated', {'harvesters': all_tables})