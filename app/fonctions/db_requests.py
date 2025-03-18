from app.models import *
import mariadb, subprocess
import json

# ------------- db_connect -------------
#
# Description:
# Cette fonction établit une connexion à une base de données MariaDB
# en utilisant les informations de connexion spécifiées.
#
# ------------------------------------------------
def db_connect():
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="192.0.2.17",  # L'adresse du serveur MariaDB
            port=3306,         # Port par défaut de MariaDB
        )
        return conn
    except mariadb.Error as e:
        print(f"Erreur de connexion à MariaDB : {e}")
        return None  # Retourne None en cas d'échec

# ------------- get_all_franchises -------------
#
# Description:
# Cette fonction récupère les noms de toutes les bases de données (franchises)
# contenant "fr" dans leur nom.
#
# ------------------------------------------------
def get_all_franchises():
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des bases de données contenant "franchise"
    cur.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME LIKE '%fr%' ORDER BY SCHEMA_NAME ASC;")
    resultat_requete = cur.fetchall()

    database = []
    for valeur in resultat_requete:
        database.append(valeur[0])
    conn.close()
    return database

# ------------- getall_NetworkScan_data -------------
#
# Description:
# Cette fonction récupère les données de la table 'NetworkScan' pour une franchise
# spécifiée et renvoie un dictionnaire structuré avec les rapports de scan.
#
# ------------------------------------------------
def getall_NetworkScan_data(franchise):

    conn = db_connect()
    cur = conn.cursor()

    try:
        cur.execute(f"USE {franchise}")
    except mariadb.ProgrammingError:
        conn.close()
        return None

    try:
        # Modifier la requête pour trier par date décroissante
        cur.execute("SELECT Scan_ID, Harvester_ID, Scan_Rapport, Scan_Date FROM NetworkScan ORDER BY Scan_Date DESC")
        resultat_requete = cur.fetchall()
        conn.close()
    except mariadb.ProgrammingError:
        conn.close()
        return None

    data = {}
    for valeur in resultat_requete:
        scan = NetworkScan(valeur)

        try:
            rapport_de_scan = json.loads(scan['scan_report'])
            entrees_formatees = []
            
            for entree in rapport_de_scan:
                # Au lieu de formater en chaîne, on crée un dictionnaire
                data_entry = {
                    'ip': entree['ip'],
                    'nom_hote': entree['nom_hote'],
                    'ports_ouverts': entree['ports_ouverts']  # Conserve la liste des ports
                }
                entrees_formatees.append(data_entry)

            data[scan['scan_id']] = {
                'Harvester_ID': scan['Harvester_id'],
                'Scan_Date': scan['scan_date'].strftime('%Y-%m-%d %H:%M:%S'),
                'entries': entrees_formatees
            }

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return data

# ------------- getall_harvesters_data -------------
#
# Description:
# Cette fonction récupère les données de la table 'Harvester' pour une franchise
# spécifiée et renvoie un dictionnaire des harvesters.
#
# ------------------------------------------------
def getall_harvesters_data(franchise):
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
        cur.execute(f"SELECT * FROM Harvester")
        resultat_requete = cur.fetchall()
    except mariadb.ProgrammingError:
        conn.close()
        return None

    data = {}
    for index, valeur in enumerate(resultat_requete):
        data[index] = Harvester(resultat_requete[index])

    conn.close()

    return data
