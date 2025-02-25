import mariadb

def db_connect():
    """
    Établit une connexion avec la base de données MariaDB et sélectionne la base NFL_IT.
    Retourne un objet connexion en cas de succès, sinon None.
    """

    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="192.0.2.17",  # L'adresse du serveur MariaDB
            port=3306,  # Port par défaut
            database="NFL_IT"  # Sélectionne directement la base de données
        )
        return conn
    except mariadb.Error as e:
        print(f"❌ Erreur de connexion à MariaDB : {e}")
        return None  # Retourne None en cas d'échec