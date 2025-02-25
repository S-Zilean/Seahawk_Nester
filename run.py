
import sys
sys.dont_write_bytecode = True

from flask import Flask, session, redirect, url_for
from functools import wraps

from flask_socketio import SocketIO

from app.views import init_dashboard, init_authentification, init_sondes, init_scan_report, init_admin_tools



# Initialisation de l'application
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configurations doivent être placées APRÈS initialisation de Flask
app.config["DEBUG"] = True
app.config["ENV"] = "development"

app.secret_key = 'super secret key'

init_authentification(app)
init_dashboard(app)
init_sondes(app, SocketIO(app))
init_scan_report(app)
init_admin_tools(app)


if __name__ == '__main__':
    app.run(debug=True)  # Lancer l'application en mode debug
    # socketio.run(app, debug=True)  # Lancer l'application avec SocketIO en mode debug










