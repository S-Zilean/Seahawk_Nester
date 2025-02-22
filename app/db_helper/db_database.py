from app.db_helper import db_connect
from app.models import Database


def get_database(identifier):
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des bases de données contenant "franchise"
    cur.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME LIKE '%franchise%' OR SCHEMA_NAME LIKE '%NFL%'ORDER BY SCHEMA_NAME ASC;")
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

def get_all_databases():
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des bases de données contenant "franchise"
    cur.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME LIKE '%franchise%' ORDER BY SCHEMA_NAME ASC;")
    req_result = cur.fetchall()

    database = []
    for value in req_result:
        database.append(value[0])
    conn.close()
    return database