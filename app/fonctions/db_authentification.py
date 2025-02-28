from functools import wraps
from flask import redirect, url_for, session
from app.fonctions import db_connect




# ------------- login_required -------------
#
# Description:
# Ce décorateur vérifie si un utilisateur est connecté avant d'exécuter une fonction protégée.
# S'il n'est pas connecté, il redirige l'utilisateur vers la page d'authentification.
#
# Fonctionnement:
# 1. Utilise le décorateur @wraps pour préserver les métadonnées de la fonction originale.
# 2. Vérifie si 'username' est présent dans la session, indiquant que l'utilisateur est connecté.
# 3. Si l'utilisateur n'est pas connecté, redirige vers la page d'authentification.
# 4. Si l'utilisateur est connecté, exécute la fonction protégée normalement.
#
# Exemple d'utilisation:
# @login_required
# def ma_fonction_protegee():
#     # Code de la fonction protégée
#
# - Si l'utilisateur est connecté, 'ma_fonction_protegee' sera exécutée.
# - Sinon, l'utilisateur sera redirigé vers la page d'authentification.
#
# Arguments:
# - f: La fonction à protéger.
#
# Retour:
# - La fonction décorée qui vérifie l'authentification avant d'exécuter la fonction originale.
#
# ------------------------------------------------



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:  # Vérifie si l'utilisateur est connecté
            return redirect(url_for('authentification'))  # Redirige vers la connexion
        return f(*args, **kwargs)  # Exécute la fonction protégée normalement
    return decorated_function





# ------------- get_user_role -------------
#
# Description:
# Cette fonction récupère le rôle d'un utilisateur à partir de la base de données,
# en utilisant le nom d'utilisateur stocké dans la session.
# Cette fonction est dédiée à l'authentification
#
# Fonctionnement:
# 1. Vérifie si l'utilisateur est connecté en recherchant 'username' dans la session.
# 2. Si l'utilisateur n'est pas connecté, retourne None.
# 3. Se connecte à la base de données en utilisant db_connection.db_connect().
# 4. Sélectionne la base de données 'NFL_IT'.
# 5. Exécute une requête SQL pour récupérer le rôle de l'utilisateur à partir de la table 'Users'.
# 6. Ferme proprement la connexion à la base de données.
# 7. Retourne le rôle de l'utilisateur si trouvé, sinon retourne None.
# 8. En cas d'erreur, affiche un message d'erreur et retourne None.
#
# Exemple d'utilisation:
# role = get_user_role()
# - Si l'utilisateur est connecté et existe dans la base de données, 'role' contiendra son rôle.
# - Sinon, 'role' sera None.
#
# Retour:
# - Le rôle de l'utilisateur sous forme de chaîne de caractères, ou None si l'utilisateur n'est pas trouvé ou en cas d'erreur.
#
# ------------------------------------------------



def get_user_role():
    
    if "username" not in session:
        return None  # L'utilisateur n'est pas connecté

    try:
        # Connexion à la base de données
        con = db_connect()
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
        print(f" Erreur lors de la récupération du rôle : {e}")
        return None # En cas d'erreur, on retourne None pour éviter un crash

