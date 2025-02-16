from functools import wraps
from flask import redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
        if 'username' not in session:
            return redirect(url_for('authentification'))
        # Sinon, exécuter la fonction protégée
        return f(*args, **kwargs)
    return decorated_function
