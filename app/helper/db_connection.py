import mariadb 

def db_connect():
    # Établit une connexion avec la base de données MariaDB.
    # Retourne un objet connexion en cas de succès, sinon None.

    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="192.0.2.17",  # L'adresse server hébergé chez adil
            port=3306  # Ajout explicite du port par défaut de MariaDB
        )
        return conn
    except mariadb.Error as e:
        conn.close()
        print(f"Erreur de connexion à MariaDB : {e}")
        return None  # On retourne None en cas d'échec