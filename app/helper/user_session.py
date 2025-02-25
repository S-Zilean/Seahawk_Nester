from functools import wraps
from flask import redirect, url_for, session
from app.helper import db_connection

def login_required(f):
    """
    Décorateur pour restreindre l'accès aux utilisateurs connectés.
    Si l'utilisateur n'est pas authentifié (pas de session active),
    il est redirigé vers la page de connexion.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:  # Vérifie si l'utilisateur est connecté
            return redirect(url_for('authentification'))  # Redirige vers la connexion
        return f(*args, **kwargs)  # Exécute la fonction protégée normalement
    return decorated_function

def get_user_role():
    """
    Récupère le rôle de l'utilisateur à partir de la base de données.

    Retourne :
        - Le rôle de l'utilisateur s'il est trouvé
        - None si l'utilisateur n'est pas connecté ou si aucune donnée n'est trouvée
    """
    if "username" not in session:
        return None  # L'utilisateur n'est pas connecté

    try:
        # Connexion à la base de données
        con = db_connection.db_connect()
        cur = con.cursor()
        
        # Sélectionne la base de données
        cur.execute("USE NFL_IT")
        
        # Exécute la requête pour récupérer le rôle de l'utilisateur
        req = "SELECT role FROM Users WHERE username = %s"
        cur.execute(req, (session['username'],))
        user_data = cur.fetchone()  # Récupère la première ligne du résultat
        
        # Ferme proprement la connexion après la requête
        cur.close()
        con.close()

        # Vérifie que l'on a bien reçu une réponse et retourne le rôle
        return user_data[0] if user_data else None

    except Exception as e:
        print(f"❌ Erreur lors de la récupération du rôle : {e}")
        return None  # En cas d'erreur, on retourne None pour éviter un crash

