from .index import init_index
from .auth import init_authentification
from .sondes import init_sondes

def init_routes(app):
    # Initialisation des routes
    init_authentification(app)
    init_sondes(app)
    init_index(app)