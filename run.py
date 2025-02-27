from app.routes import *
from app.fonctions import *
import sys
sys.dont_write_bytecode = True

from flask import Flask, session, redirect, url_for
from functools import wraps

from flask_socketio import SocketIO


# Initialisation de l'application
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configurations doivent être placées APRÈS initialisation de Flask
app.config["DEBUG"] = True
app.config["ENV"] = "development"

app.secret_key = 'super secret key'



@app.context_processor
def inject_franchises():
    # Récupération de toutes les franchises
    temp_franchises = get_all_databases()
    return dict(franchises=temp_franchises)



socketio = SocketIO(app)
init_authentification(app)
init_dashboard(app)
init_base(app)
init_franchise(app)

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Lancer l'application avec SocketIO en mode debug
