from functools import wraps
from flask import redirect, url_for, session

from app.db_helper import db_connection

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
        if 'username' not in session:
            return redirect(url_for('authentification'))
        # Sinon, exécuter la fonction protégée
        return f(*args, **kwargs)
    return decorated_function

def get_user_role():
    # Récupérer le groupe de l'utilisateur depuis la base de données
    con = db_connection.db_connect()
    cur = con.cursor()
    cur.execute("USE NFL_IT")
    req = "SELECT role FROM Users WHERE username = %s"
    cur.execute(req, (session['username'],))
    user_data = cur.fetchone()
    user_role = user_data[0]
    return user_role

