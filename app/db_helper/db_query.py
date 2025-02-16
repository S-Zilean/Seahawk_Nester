from app.db_helper import db_connect
import mariadb


def do_request(query, params=None, fetch=False):
    """
    Exécute une requête SQL de manière sécurisée.
    
    - query : requête SQL sous forme de chaîne de caractères.
    - params : tuple contenant les valeurs des paramètres à injecter dans la requête.
    - fetch : booléen, True si on veut récupérer des résultats, False sinon.

    Retourne :
    - Les résultats sous forme de liste de tuples si fetch=True.
    - None en cas d'erreur ou si fetch=False.
    """
    conn = db_connect()
    if not conn:
        return None

    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        result = cur.fetchall() if fetch else None
        conn.commit()
        cur.close()
        conn.close()  # Fermer la connexion proprement
        return result
    except mariadb.Error as e:
        print(f"❌ Erreur SQL : {e}")
        conn.close()  # Fermer la connexion en cas d'erreur
        return None

def db_get_table(nom_table):
    """
    Récupère toutes les données d'une table spécifique.
    """
    query = f"SELECT * FROM {nom_table}"
    return do_request(query, fetch=True)