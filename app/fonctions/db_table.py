from app.fonctions.db_connection import db_connect
from app.models.harvester import Harvester
import mariadb

def get_table(franchise, identifier):
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
        table_dict[index] = value[0]

    if isinstance(identifier, int):
        if identifier == 0:
            identifier = 1
        conn.close()
        return table_dict[identifier - 1]
    
    elif isinstance(identifier, str):
        for tbl in table_dict.values():
            if identifier == tbl:
                conn.close()
                return tbl
    else:
        conn.close()
        raise ValueError("L'identifiant doit être un entier ou une chaîne de caractères.")
    


# N'affiche que les noms des tables
# pas les données !

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



# ------------- get_all_row_in_table -------------
# 
# Détails: 
# Dans cette fonction, je commence par me connecter
# J'effectue ensuite une requête SQL 
#
# La requête récupère les données :
#       * d'une table spécifiée 
#       * d'une franchise spécifiée
#
# Le résultat de la requête est stocké dans une variable
# avec fetchall() qui récupère toutes les lignes de résultats
# contrairement à fetchone() qui récupère une seule ligne
#
# Ensuite, je ferme la connexion à la base de données
# La variable a conservée les résultats de la requête
#
# Je crée un dictionnaire vide pour stocker les données
# Je parcours ensuite les résultats de la requête avec une boucle
# J'ajoute chaque ligne de résultat dans le dictionnaire
# Le dictionnaire représente la classe Harvester
# dans ma boucle for index, value in enumerate(req_result)
# je crée une instance de la classe Harvester
#
# Enfin, je retourne le dictionnaire contenant les données
#
# Exemple du traitement de la variable data:
#
# data = get_all_row_in_table("NFL_IT", "Harvester")
#
# data[0] sera égal à la première ligne de la table Harvester
# data.[0].Hostname sera égal à la valeur de la colonne Hostname de la première ligne
#
# Arguments:
# franchise: nom de la franchise
# table: nom de la table
#
# Retour:
# Dictionnaire contenant les données de la table
#
# ------------------------------------------------


def get_harvesters_data(franchise, table):
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
    
    
    conn.close()

    data = {}
    for index, value in enumerate(req_result):
        data[index] = Harvester(req_result[index])

    return data