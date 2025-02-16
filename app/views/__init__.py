from .sondes import init_sondes
from .authentification import init_authentification
from .dashboard import init_dashboard

def init_routes(app):
    # Initialisation des routes
    init_authentification(app)
    init_sondes(app)
    init_dashboard