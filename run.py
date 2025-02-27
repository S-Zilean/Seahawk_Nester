import sys
import os
import redis
from flask import Flask, session, redirect, url_for
from functools import wraps
from flask_socketio import SocketIO
# import eventlet  # <-- On supprime l'import eventlet
# eventlet.monkey_patch()  # <-- On supprime le monkey_patch eventlet

from gevent import monkey   # <-- On ajoute l’import gevent
monkey.patch_all()          # <-- Patch global (optionnel mais souvent utile)

from flask_session import Session
from app.views import init_dashboard, init_authentification, init_sondes, init_scan_report, init_admin_tools

sys.dont_write_bytecode = True

# Initialisation de l'application Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# ✅ Définition d'une clé secrète robuste
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "une_clé_ultra_secrète")

# ✅ Configuration de Redis pour stocker les sessions
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # Sécurisation des sessions
app.config['SESSION_KEY_PREFIX'] = 'seahawk_nester_'
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)

# Initialisation des sessions Flask
Session(app)

# ✅ Configuration de SocketIO en mode gevent (avec logs activés)
socketio = SocketIO(
    app,
    async_mode="gevent",      # <-- Changer "eventlet" en "gevent"
    cors_allowed_origins="*",
    logger=True,              # active les logs du côté SocketIO
    engineio_logger=True      # active les logs côté Engine.IO
)

# ✅ Initialisation des modules de l'application
init_authentification(app)
init_dashboard(app)
init_sondes(app, socketio)
init_scan_report(app)
init_admin_tools(app)

if __name__ == '__main__':
    # Pour usage local / dev (avec le serveur gevent interne)
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

