from app.models import *
import mariadb, subprocess
import json



# ------------- db_connect -------------
#
# Description:
# Cette fonction établit une connexion à une base de données MariaDB en utilisant les informations d'identification fournies.
# Elle retourne un objet de connexion si la connexion est réussie, sinon elle retourne `None`.
#
# Fonctionnement:
# 1. Tente de se connecter à la base de données MariaDB en utilisant les paramètres spécifiés (utilisateur, mot de passe, hôte, port).
# 2. Si la connexion échoue, elle imprime un message d'erreur et retourne `None`.
#
# Exemple d'utilisation:
# conn = db_connect()
# if conn is not None:
#     # Utiliser la connexion
#
# Arguments:
# - Aucun argument requis.
#
# Retour:
# - Un objet de connexion MariaDB en cas de succès.
# - `None` en cas d'échec de la connexion.
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
# Cette fonction récupère les noms de toutes les bases de données contenant le mot-clé "fr" (probablement pour "franchise")
# depuis le système d'information de la base de données. Elle retourne une liste de ces noms.
#
# Fonctionnement:
# 1. Se connecte à la base de données en utilisant la fonction `db_connect()`.
# 2. Exécute une requête pour récupérer les noms des schémas (bases de données) contenant "fr" dans leur nom.
# 3. Parcourt les résultats de la requête et ajoute chaque nom de base de données à une liste.
# 4. Ferme la connexion à la base de données et retourne la liste des noms de bases de données.
#
# Exemple d'utilisation:
# franchises = get_all_franchises()
#
# Arguments:
# - Aucun argument requis.
#
# Retour:
# - Une liste contenant les noms des bases de données qui incluent "fr" dans leur nom.
#
# ------------------------------------------------

def get_all_franchises():
    conn = db_connect()
    cur = conn.cursor()

    # Récupérer les noms des bases de données contenant "fr"
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
# Cette fonction récupère toutes les données des scans réseau pour une franchise spécifiée depuis une base de données.
# Elle retourne ces données sous forme d'un dictionnaire contenant des informations formatées sur chaque scan.
#
# Fonctionnement:
# 1. Se connecte à la base de données en utilisant la fonction `db_connect()`.
# 2. Sélectionne la base de données spécifique à la franchise.
# 3. Exécute une requête pour récupérer les données de la table `NetworkScan`, triées par date décroissante.
# 4. Parcourt les résultats de la requête et formate les données JSON des rapports de scan.
# 5. Gère les exceptions et ferme les connexions à la base de données.
#
# Exemple d'utilisation:
# network_scan_data = getall_NetworkScan_data('nom_de_la_franchise')
#
# Arguments:
# - franchise: Le nom de la franchise dont la base de données doit être utilisée.
#
# Retour:
# - Un dictionnaire contenant les données des scans réseau, indexées par `Scan_ID`.
# - Chaque entrée contient l'ID du harvester, la date du scan, et les entrées formatées du rapport de scan.
# - Retourne `None` en cas d'erreur de programmation avec la base de données.
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
# Cette fonction récupère toutes les données des harvesters (collecteurs) pour une franchise spécifiée depuis une base de données.
# Elle retourne ces données sous forme d'un dictionnaire d'objets `Harvester`.
#
# Fonctionnement:
# 1. Se connecte à la base de données en utilisant la fonction `db_connect()`.
# 2. Sélectionne la base de données spécifique à la franchise.
# 3. Exécute une requête pour récupérer toutes les données de la table `Harvester`.
# 4. Parcourt les résultats de la requête et crée un dictionnaire d'objets `Harvester`.
# 5. Gère les exceptions et ferme les connexions à la base de données.
#
# Exemple d'utilisation:
# harvesters_data = getall_harvesters_data('nom_de_la_franchise')
#
# Arguments:
# - franchise: Le nom de la franchise dont la base de données doit être utilisée.
#
# Retour:
# - Un dictionnaire contenant les objets `Harvester` indexés par leur position dans les résultats de la requête.
# - Retourne `None` en cas d'erreur de programmation avec la base de données.
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
