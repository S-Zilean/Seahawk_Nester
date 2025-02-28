# Importation des modules nécessaires de Flask et des fonctions utilitaires
from flask import session, redirect, url_for, request, render_template
from app.fonctions import db_connect

# Définition d'un décorateur pour vérifier si l'utilisateur est connecté
from app.fonctions.db_authentification import login_required



# ------------- init_authentification -------------
#
# Description:
# Cette fonction initialise les routes d'authentification pour une application Flask,
# en définissant les comportements pour la connexion et la déconnexion des utilisateurs.
#
# Fonctionnement:
# 1. Définit la route '/' pour la page de connexion, accessible via les méthodes GET et POST.
# 2. Utilise le décorateur @login_required pour protéger l'accès à certaines routes.
# 3. Si l'utilisateur est déjà connecté, redirige vers le tableau de bord.
# 4. Si la méthode de la requête est POST, traite le formulaire de connexion :
#    - Récupère le nom d'utilisateur et le mot de passe du formulaire.
#    - Vérifie les informations d'identification dans la base de données.
#    - Si les informations sont correctes, stocke le nom d'utilisateur et le rôle dans la session.
#    - Redirige vers le tableau de bord ou affiche un message d'erreur en cas d'échec.
# 5. Si la méthode de la requête est GET, affiche le formulaire de connexion.
# 6. Définit la route '/logout' pour la déconnexion :
#    - Supprime le nom d'utilisateur de la session.
#    - Redirige vers la page de connexion.
#
# Exemple d'utilisation:
# - Accéder à la route '/' affiche le formulaire de connexion.
# - Soumettre le formulaire avec des informations valides redirige vers '/dashboard'.
# - Accéder à la route '/logout' déconnecte l'utilisateur.
#
# Arguments:
# - app: L'instance de l'application Flask.
#
# ------------------------------------------------



# Initialisation des routes d'authentification
def init_authentification(app):
    # Définition de la route pour la page de connexion
    @login_required
    @app.route('/', methods=['GET', 'POST'])
    def authentification():
        # Si l'utilisateur est déjà connecté, rediriger vers le tableau de bord
        if 'username' in session:
            return redirect('/dashboard')

        # Si la méthode de la requête est POST, traiter le formulaire de connexion
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Création d'un curseur pour exécuter des requêtes SQL
            cur = db_connect().cursor()

            # Utilisation de la base de données Users
            cur.execute("USE NFL_IT")

            # Requête pour vérifier si l'utilisateur existe dans la base de données
            # la fonction PASSWORD(%s) est utilisée pour comparer le mot de passe haché sur MariaDB
            # SELECT * FROM Users WHERE username = %s AND PASSWORD(%s) = password
            # %s est utilisé pour éviter les attaques par injection SQL
            # Les valeurs de username et password sont passées en tant que paramètres à la requête           
            req = "SELECT * FROM Users WHERE username = %s AND PASSWORD(%s) = password"
            cur.execute(req, (username, password))

            # La fonction fetchone() récupère la première ligne de résultat de la requête.
            # On utilise fetchone() car on s'attend à un seul utilisateur avec le même nom d'utilisateur.
            # L'utilisation de fetchall() ne changerait pas la logique de vérification du mot de passe.
            # Si la requête est correctement écrite, elle ne retournera des résultats que si le nom d'utilisateur et le mot de passe sont corrects.
            user = cur.fetchone()

            # Fermeture du curseur après usage pour libérer les ressources de la BDD
            # Cela évite les fuites de mémoire et les problèmes de performances            
            cur.close() 


            if user:
                session['username'] = username
                session['role'] = user[3]  # Assurez-vous que l'index correspond à la colonne 'role'
                return redirect('/dashboard')
            else:
                error = 'Nom d\'utilisateur ou mot de passe incorrect'
                return render_template('authentification.html', error=error)
        # Si la méthode de la requête est GET, afficher le formulaire de connexion
        return render_template('authentification.html')

    # Définition de la route pour la déconnexion
    @app.route('/logout')
    def logout():
        # Supprimer le nom d'utilisateur de la session
        session.pop('username', None)
        # Rediriger vers la page de connexion
        return redirect(url_for('authentification'))


