from flask import render_template, abort
from app.fonctions import getall_harvesters_data, get_all_franchises, update_harvester_status
from app.fonctions.db_authentification import login_required


# Définition de la fonction init_franchise qui prend 'app' comme argument
def init_franchise(app):

    # Décorateur pour définir la route '/<nom_franchise>'
    @app.route('/<nom_franchise>')

    # Décorateur pour exiger que l'utilisateur soit authentifié
    @login_required

    # Définition de la fonction franchise qui prend 'nom_franchise' comme argument
    def franchise(nom_franchise):

        # Récupération de toutes les franchises disponibles
        all_franchises = get_all_franchises()

        # Vérification si le nom de la franchise est valide en le cherchant dans la liste des franchises
        if nom_franchise in all_franchises:

            # Mise à jour de l'état des harvesters pour la franchise spécifiée
            update_harvester_status(nom_franchise)

            try:
                # Récupération des données de tous les harvesters pour la franchise spécifiée
                harvesters_data = getall_harvesters_data(nom_franchise)

                # Rendu du template 'franchise.html' avec les données récupérées
                return render_template('franchise.html', harvester=harvesters_data, franchise_name=nom_franchise)
            except Exception as e:
                # En cas d'erreur, définir un message d'erreur pour les données du harvester
                e = {"Hostname": "Erreur : Aucune donnée trouvée",
                    "ip": "Erreur : Aucune donnée trouvée",
                    "Etat": "Erreur : Aucune donnée trouvée"}

                # Rendu du template 'franchise.html' avec le message d'erreur
                return render_template('franchise.html', harvester=e, scan_report=e, franchise_name=nom_franchise)

        # Si la franchise n'existe pas, retourner une erreur 404
        abort(404, description="Franchise non trouvée")
