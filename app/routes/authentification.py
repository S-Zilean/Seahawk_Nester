# Importation des modules nécessaires de Flask et des fonctions utilitaires
from flask import session, redirect, url_for, request, render_template
from app.fonctions import db_connect

# Définition d'un décorateur pour vérifier si l'utilisateur est connecté
from app.fonctions.db_authentification import login_required


# ------------- Initialisation des routes d'authentification -------------
#
# Description:
# Ce code initialise les routes d'authentification pour une application web Flask.
# Il définit les routes pour la page de connexion et la déconnexion, et gère l'authentification des utilisateurs.
#
# Fonctionnement:
# 1. La fonction `init_authentification` configure les routes d'authentification pour l'application Flask.
# 2. La route '/' est définie pour gérer la connexion des utilisateurs.
#    - Si l'utilisateur est déjà connecté, il est redirigé vers le tableau de bord.
#    - Si une requête POST est reçue, le formulaire de connexion est traité :
#      - Les informations d'identification (nom d'utilisateur et mot de passe) sont récupérées.
#      - Une connexion à la base de données est établie pour vérifier les informations d'identification.
#      - Si les informations sont correctes, une session est créée pour l'utilisateur, et il est redirigé vers le tableau de bord.
#      - Si les informations sont incorrectes, un message d'erreur est affiché.
#    - Si une requête GET est reçue, le formulaire de connexion est affiché.
# 3. La route '/logout' est définie pour gérer la déconnexion des utilisateurs.
#    - Le nom d'utilisateur est supprimé de la session, et l'utilisateur est redirigé vers la page de connexion.
#
# Exemple d'utilisation:
# init_authentification(app)
#
# Arguments:
# - app: L'objet Flask représentant l'application web.
#
# Retour:
# - Aucun retour explicite, mais configure les routes d'authentification pour l'application.
#
# ------------------------------------------------

def init_authentification(app):
    @login_required
    @app.route('/', methods=['GET', 'POST'])
    def authentification():
        if 'username' in session:
            return redirect('/dashboard')

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            cur = db_connect().cursor()
            cur.execute("USE NFL_IT")

            req = "SELECT * FROM Users WHERE username = %s AND PASSWORD(%s) = password"
            cur.execute(req, (username, password))

            user = cur.fetchone()
            cur.close()

            if user:
                session['username'] = username
                session['role'] = user[3]
                return redirect('/dashboard')
            else:
                error = 'Nom d\'utilisateur ou mot de passe incorrect'
                return render_template('authentification.html', error=error)

        return render_template('authentification.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('authentification'))

