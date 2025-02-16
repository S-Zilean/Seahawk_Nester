# Importation des modules nécessaires de Flask et des fonctions utilitaires
from flask import session, redirect, url_for, request, render_template, flash
from functools import wraps
from app.db_helper.db_connection import db_connect

# Définition d'un décorateur pour vérifier si l'utilisateur est connecté
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si l'utilisateur n'est pas connecté, rediriger vers la page de connexion
        if 'username' not in session:
            return redirect(url_for('authentification'))
        # Sinon, exécuter la fonction protégée
        return f(*args, **kwargs)
    return decorated_function

# Initialisation des routes d'authentification
def init_authentification(app):
    # Définition de la route pour la page de connexion
    @app.route('/', methods=['GET', 'POST'])
    def authentification():
        # Si la méthode de la requête est POST, traiter le formulaire de connexion
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Vérification des informations d'identification dans la base de données
            # Connexion à la base de données et exécution de la requête
            cur = db_connect().cursor()
            cur.execute("USE Users")
            req = "SELECT * FROM Users WHERE username = %s AND password = %s"
            cur.execute(req, (username, password))
            user = cur.fetchone()
            cur.close()  # Fermer le curseur après utilisation
            # Si l'utilisateur est trouvé, enregistrer le nom d'utilisateur dans la session
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                # Sinon, retourner un message d'erreur dans la page de connexion
                error = 'Nom d\'utilisateur ou mot de passe incorrect'
                return render_template('auth.html', error=error)
        # Si la méthode de la requête est GET, afficher le formulaire de connexion
        return render_template('auth.html')

    # Définition de la route pour la déconnexion
    @app.route('/')
    def logout():
        # Supprimer le nom d'utilisateur de la session
        session.pop('username', None)
        # Rediriger vers la page de connexion
        return redirect(url_for('auth'))


