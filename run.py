from flask import Flask, session, redirect, url_for
from functools import wraps

from flask_socketio import SocketIO


from app.views import init_dashboard, init_authentification, init_sondes



# Initialisation de l'application
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.secret_key = 'super secret key'

init_authentification(app)
init_dashboard(app)
init_sondes(app, SocketIO(app))



if __name__ == '__main__':
    app.run(debug=True)  # Lancer l'application en mode debug
    # socketio.run(app, debug=True)  # Lancer l'application avec SocketIO en mode debug

# Définition de la route pour la page d'accueil








