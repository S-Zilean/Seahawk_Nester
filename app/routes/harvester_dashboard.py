from flask import Flask, render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, getall_NetworkScan_data
from app.fonctions.db_authentification import login_required
import json

from app.fonctions.db_requests import db_connect



app = Flask(__name__)

def init_franchise(app):
    @app.route('/<nom_franchise>/<harvester_id>')
    @login_required
    def harvester_id(nom_franchise,harvester_id):

        # Récupération de toutes les franchises
        all_franchises = get_all_franchises()



        # Vérifier si le nom de la franchise est valide
        if nom_franchise in all_franchises:
            db = db_connect()
            cur = db.cursor()
            req = "USE {nom_franchise}"
            cur.execute(req)


            
        # Si la franchise n'existe pas, retourner une erreur 404
        abort(404, description="Franchise non trouvée")

if __name__ == '__main__':
    app.run(debug=True)
