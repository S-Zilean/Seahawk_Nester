from app.db_helper.db_connection import db_connect
from app.models import Database


def get_franchise(identifier):
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des bases de données contenant "franchise"
    cur.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME LIKE '%franchise%' ORDER BY SCHEMA_NAME ASC;")
    req_result = cur.fetchall()
    

    db_dict = {}
    for key, value in enumerate(req_result):
        db_dict[key] = Database(*value)

    if isinstance(identifier, int):
        if identifier == 0:
            identifier = 1
        conn.close()
        return list(db_dict[identifier - 1].data.values())[0]

    elif isinstance(identifier, str):
        for db in db_dict.values():
            if identifier in db.data:
                conn.close()
                return db.data[identifier]

    else:
        conn.close()
        raise ValueError("L'identifiant doit être un entier ou une chaîne de caractères.")

    conn.close()

def get_all_franchises():
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des bases de données contenant "franchise"
    cur.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME LIKE '%franchise%' ORDER BY SCHEMA_NAME ASC;")
    req_result = cur.fetchall()

    franchises = []
    for value in req_result:
        franchises.append(value[0])
    conn.close()
    return franchises