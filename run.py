from app.routes import *
from app.fonctions import *
import sys  
import os
import redis    
from flask import Flask
from flask_socketio import SocketIO

sys.dont_write_bytecode = True

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configurations doivent être placées APRÈS initialisation de Flask
app.config["DEBUG"] = True
app.config["ENV"] = "development"

app.secret_key = 'super secret key'



# ------------- inject_franchises -------------
#
# Description:
# Ce processeur de contexte Flask injecte une liste de toutes les franchises
# dans le contexte de rendu des templates, permettant ainsi d'accéder à cette liste
# dans tous les templates sans avoir à la passer explicitement à chaque rendu.
#
# Fonctionnement:
# 1. Utilise la fonction get_all_franchises() pour récupérer toutes les franchises.
# 2. Retourne un dictionnaire contenant la liste des franchises sous la clé 'franchises'.
# 3. Le dictionnaire est automatiquement ajouté au contexte de rendu des templates Flask.
#
# Exemple d'utilisation:
# - Dans un template Jinja2, vous pouvez accéder à la liste des franchises avec {{ franchises }}.
#
# Retour:
# - Un dictionnaire contenant la liste des franchises sous la clé 'franchises'.
#
# ------------------------------------------------



@app.context_processor
def inject_franchises():
    # Récupération de toutes les franchises
    temp_franchises = get_all_franchises()
    return dict(franchises=temp_franchises)



socketio = SocketIO(app)
init_authentification(app)
init_dashboard(app)
init_base(app)
init_franchise(app)
init_harvester_dashboard(app)

if __name__ == '__main__':
    # Pour usage local / dev (avec le serveur gevent interne)
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

