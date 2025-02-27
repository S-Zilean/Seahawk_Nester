from flask import Flask, render_template, abort

from app.fonctions.db_data import get_table_data
from app.fonctions.db_database import get_all_databases
from app.fonctions.db_query import do_request
from app.fonctions.db_table import get_table
from app.fonctions.user_session import login_required

app = Flask(__name__)

class Mytest :
    def __init__(self, value):
        self.key = {
            "Harvester_ID" : value[0],
            "Harvester_STATE" : value[1],
            "Harvester_IP" : value[2],
            "Harvester_HOSTNAME" : value[3],
            "Harvester_SUBNET" : value[4],
            "Harvester_NETMASK" : value[5],
            "Harvester_OS" : value[6],
            "Harvester_PORT" : value[7],
            "Harvester_VERSION" : value[8]
        }


def init_franchise(app):
    @app.route('/<nom_franchise>')
    @login_required
    def franchise(nom_franchise):
        # Récupération de toutes les franchises
        all_franchises = get_all_databases()

        # Vérifier si le nom de la franchise est valide
        if nom_franchise in all_franchises:
            
            test = get_table_data(nom_franchise, "Harvester")

            for key, value in test:
                print(key, value)

            # Récupération de la table Harvester                        
            return render_template('franchise.html',franchise_name=nom_franchise)

        # Si la franchise n'existe pas, retourner une erreur 404
        abort(404, description="Franchise non trouvée")

if __name__ == '__main__':
    app.run(debug=True)
