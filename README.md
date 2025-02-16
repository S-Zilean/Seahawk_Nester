# Nom du Projet
Brève description de ce que fait votre projet et de son objectif principal.

## Structure du Projet

### /SRC
Représente la racine pour les fichiers Python.

### /SRC/ROUTES
Ce dossier contient tous les fichiers `routes.py` qui gèrent les interactions avec les fichiers HTML.
Chaque fichier de route peut être nommé en fonction de la fonctionnalité ou de la page qu'il gère, par exemple `user_route.py`, `product_route.py`, etc.

### /SRC/CONTROLLERS
Ce dossier contient les fichiers qui gèrent la logique de la webapp.
Par exemple, `database_controller.py` contenant des fonctions de contrôle comme `connect`, `disconnect`, `get_table`, etc.

### /SRC/MODELS
Ce dossier contient les fichiers de classes qui représentent les structures de données ou les entités de la webapp.
Par exemple, `harvester_model.py` représente la table "Harvester" d'une base de données.

### /SRC/UTILS
Ce dossier contient des fichiers utilitaires ou des fonctions d'aide qui peuvent être utilisés à travers la webapp.
Par exemple, `helper_functions.py` pourrait contenir des fonctions de validation ou de formatage.

## Installation
Instructions pour installer les dépendances et configurer l'environnement.
pip install Flask
pip install mariadb
pip install flask_socketio

## Utilisation
Instructions pour exécuter le projet, par exemple :
<!-- ```bash
python nester.py -->
