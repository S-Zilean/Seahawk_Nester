from .db_connection import db_connect
from app.models.harvester import Harvester
import mariadb

def get_data(franchise, table):
    conn = db_connect()
    cur = conn.cursor()

    # Utiliser la franchise spécifiée
    try:
        cur.execute(f"USE {franchise}")
    except mariadb.ProgrammingError:
        return None

    # Récupérer toutes les données de la table spécifiée
    try:
        cur.execute(f"SELECT * FROM {table}")
        req_result = cur.fetchall()
    except mariadb.ProgrammingError:
        return None
    conn.close()

    data_dict = {}
    for index, value in enumerate(req_result):
        data_dict[index] = value

    return data_dict


# --------------------------------------------------------------------------------------------
# Fonctions retournant toutes les valeurs d'un type
# --------------------------------------------------------------------------------------------



