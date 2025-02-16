# Importation des modules nécessaires de Flask et des fonctions utilitaires
from flask import session, redirect, url_for, request, render_template
from app.db_helper.db_connection import db_connect

# Définition d'un décorateur pour vérifier si l'utilisateur est connecté
from app.helper.user_session import login_required
login_required(any)


# Initialisation des routes d'authentification
def init_authentification(app):
    # Définition de la route pour la page de connexion
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
            cur.execute("USE Users")

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


