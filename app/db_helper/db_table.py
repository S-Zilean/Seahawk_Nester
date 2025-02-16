from app.db_helper.db_connection import db_connect
import mariadb
from app.models import Table

def table(franchise, identifier):
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des tables de la franchise spécifiée
    try:
        cur.execute(f"SHOW TABLES FROM {franchise}")
        req_result = cur.fetchall()
    except mariadb.ProgrammingError:
        conn.close()
        return None

    table_dict = {}
    for index, value in enumerate(req_result):
        table_dict[index] = Table(*value)

    if isinstance(identifier, int):
        if identifier == 0:
            identifier = 1
        conn.close()
        return list(table_dict[identifier - 1].data.values())[0]
    
    elif isinstance(identifier, str):
        for tbl in table_dict.values():
            if identifier in tbl.data:
                conn.close()
                return tbl.data[identifier]
    else:
        conn.close()
        raise ValueError("L'identifiant doit être un entier ou une chaîne de caractères.")
    

def get_all_tables(franchise):
    conn = db_connect()
    cur = conn.cursor()

    # Utiliser la franchise spécifiée
    try:
        cur.execute(f"USE {franchise}")
    except mariadb.ProgrammingError:
        conn.close()
        return None

    # Récupérer les noms des tables de la franchise spécifiée
    try:
        cur.execute("SHOW TABLES")
        req_result = cur.fetchall()
    except mariadb.ProgrammingError:
        conn.close()
        return None

    tables = []
    for value in req_result:
        tables.append(value[0])
    conn.close()
    return tables