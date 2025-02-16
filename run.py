from flask import Flask, session, redirect, url_for
from functools import wraps

from flask_socketio import SocketIO
import mariadb

from app.db_helper import db_connect, get_franchise
from app.views import init_dashboard, init_sondes, init_authentification
from app.helper.user_session import login_required


# Initialisation de l'application
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')



def init(f, app):

    test = SocketIO(app)

    app.secret_key = 'super secret key'

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
        if 'username' not in session:
            return redirect(url_for('authentification'))
        # init_sondes(app,test)
        # Sinon, exécuter la fonction protégée
        return f(*args, **kwargs)

    init_authentification(app)
    init_dashboard(app)

    return decorated_function

init(any, app)


if __name__ == '__main__':
    app.run(debug=True)  # Lancer l'application en mode debug
    # socketio.run(app, debug=True)  # Lancer l'application avec SocketIO en mode debug

# Définition de la route pour la page d'accueil








