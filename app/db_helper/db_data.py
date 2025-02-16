from .db_connection import db_connect
from app.models import Harvester, NetworkScan, RemoteAccessLogs, Users
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

    data_dict = {}
    for index, value in enumerate(req_result):
        if value == 'Harvester':
            tmp = Harvester(*value)
        elif value == 'NetworkScan':
            tmp = NetworkScan(*value)
        elif value == 'RemoteAccessLogs':
            tmp = RemoteAccessLogs(*value)
        elif value == 'Users':
            tmp = Users(*value)
        else:
            tmp = value
        data_dict[index] = tmp
    conn.close()
    return data_dict

# --------------------------------------------------------------------------------------------
# Fonctions retournant toutes les valeurs d'un type
# --------------------------------------------------------------------------------------------

def get_table_data(franchise, table):
    conn = db_connect()
    cur = conn.cursor()

    # Utiliser la franchise spécifiée
    try:
        cur.execute(f"USE {franchise}")
    except mariadb.ProgrammingError:
        conn.close()        
        return None

    # Récupérer toutes les données de la table spécifiée
    try:
        cur.execute(f"SELECT * FROM {table}")
        req_result = cur.fetchall()
    except mariadb.ProgrammingError:
        conn.close()
        return None

    data = []
    for row in req_result:
        data.append(list(row))
    conn.close()
    return data


def get_specific_data(franchise, table, column, identifier):
    conn = db_connect()
    cur = conn.cursor()

    # Utiliser la franchise spécifiée
    try:
        cur.execute(f"USE {franchise}")
    except mariadb.ProgrammingError:
        conn.close()
        return None

    # Récupérer toutes les données de la table spécifiée
    try:
        cur.execute(f"SELECT * FROM {table}")
        req_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
    except mariadb.ProgrammingError:
        conn.close()
        return None

    if isinstance(identifier, int):
        if identifier < 0 or identifier >= len(req_result):
            raise IndexError("L'index est hors des limites des résultats de la requête.")
        conn.close()
        return req_result[identifier][column_names.index(column)]
    elif isinstance(identifier, str):
        for row in req_result:
            if identifier in row:
                return row[column_names.index(column)]
        conn.close()
        raise ValueError("La valeur spécifiée n'a pas été trouvée dans les résultats de la requête.")
    else:
        conn.close()
        raise ValueError("L'identifiant doit être un entier ou une chaîne de caractères.")
    


