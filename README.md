Une application de supervision réseau permettant de collecter et d’afficher les données de plusieurs sondes (Harvesters). L’objectif est de fournir un tableau de bord centralisé pour visualiser l’état, les rapports de scan et les informations clés de chaque Harvester.

Structure du Projet
/SRC
Représente la racine pour les fichiers Python.

/SRC/ROUTES
Contient les différents fichiers de routes Flask, chacun gérant une section ou une fonctionnalité de l’application (ex. harvester_route.py, dashboard_route.py).
Ces routes chargent les templates HTML et interagissent avec la logique métier depuis les controllers.

/SRC/CONTROLLERS
Regroupe les fichiers qui implémentent la logique de la webapp (accès base de données, opérations CRUD, etc.).
Par exemple, database_controller.py pour la connexion à la base de données, la récupération et la mise à jour des informations.

/SRC/MODELS
Stocke les classes qui représentent les entités de l’application (tables de la base, objets métiers).
Exemple : harvester_model.py décrit la structure d’un Harvester (champs, propriétés, méthodes associées).

/SRC/UTILS
Contient les fichiers de fonctions utilitaires ou “helpers” utiles dans différents modules.
Exemple : helper_functions.py pour la validation de données, le formatage, ou d’autres outils réutilisables.

Installation
Cloner le dépôt ou récupérer le code source.
Créer et activer un environnement virtuel :
python3 -m venv venv
source venv/bin/activate

Installer les dépendances :
pip install -r requirements.txt
Les principales bibliothèques sont :
Flask
mariadb
flask_socketio
gunicorn
gevent (optionnel si peu d'utilisateurs) 
redis (si les sessions ou SocketIO sont utilisés à plus grande échelle)

Utilisation
Mode Développement :
Lancez simplement le fichier principal, 
python run.py
Rendez-vous ensuite à l’adresse http://127.0.0.1:5000/ dans votre navigateur.

Mode Production (recommandé) :
Exécutez Gunicorn avec, par exemple :
gunicorn -w 4 -b 0.0.0.0:80 run:app