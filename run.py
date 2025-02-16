from flask import Flask
from flask_socketio import SocketIO
import mariadb

from app.views.index import init_index
from app.views.sondes import init_sondes
from app.views.auth import init_authentification
from app.db_helper import db_connect, get_franchise

# Initialisation de l'application
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Clé secrète pour les sessions Flask
app.secret_key = "une_cle_secrete_complexe_et_unique_1234#ABcd!"
test = SocketIO(app)


# Initialisation des routes
init_index(app)
init_sondes(app,test)
init_authentification(app)

if __name__ == '__main__':
    app.run(debug=True)  # Lancer l'application en mode debug
    # socketio.run(app, debug=True)  # Lancer l'application avec SocketIO en mode debug