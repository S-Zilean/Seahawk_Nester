from flask import Flask, render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, getall_NetworkScan_data
from app.fonctions.db_authentification import login_required

app = Flask(__name__)




def init_franchise(app):
    @app.route('/<nom_franchise>')
    @login_required
    def franchise(nom_franchise):
        # Récupération de toutes les franchises
        all_franchises = get_all_franchises()


        # Vérifier si le nom de la franchise est valide
        if nom_franchise in all_franchises:
            
            try:
                harvesters_data = getall_harvesters_data(nom_franchise)
                networkscan_data = getall_NetworkScan_data(nom_franchise)
                print(harvesters_data)

                return render_template('franchise.html', harvester=harvesters_data, franchise_name=nom_franchise)
            except Exception as e:
                e = {"error" : "Erreur : Aucune donnée trouvée"}
                return render_template('franchise.html', harvester = e, franchise_name=nom_franchise)
            
        # Si la franchise n'existe pas, retourner une erreur 404
        abort(404, description="Franchise non trouvée")

if __name__ == '__main__':
    app.run(debug=True)
