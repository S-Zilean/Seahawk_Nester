from app.models import *
import mariadb, subprocess


# ------------- db_connect -------------
#
# Description:
# Cette fonction établit une connexion à une base de données MariaDB
# en utilisant les informations de connexion spécifiées.
#
# Fonctionnement:
# 1. Tente de se connecter à la base de données MariaDB avec les paramètres suivants :
#    - Utilisateur : "root"
#    - Mot de passe : "root"
#    - Adresse du serveur : "192.0.2.17"
#    - Port : 3306 (port par défaut de MariaDB)
#    - Base de données : "NFL_IT"
# 2. Si la connexion réussit, retourne l'objet de connexion.
# 3. En cas d'échec de la connexion, affiche un message d'erreur et retourne None.
#
# Exemple d'utilisation:
# conn = db_connect()
# - Si la connexion est réussie, 'conn' contiendra l'objet de connexion à la base de données.
# - Sinon, 'conn' sera None.
#
# Retour:
# - Un objet de connexion à la base de données MariaDB, ou None en cas d'échec.
#
# ------------------------------------------------

def db_connect():
    try:
        conn = mariadb.connect(
            user="root",
            password="root",
            host="192.0.2.17",  # L'adresse du serveur MariaDB
            port=3306,  # Port par défaut
        )
        return conn
    except mariadb.Error as e:
        print(f"Erreur de connexion à MariaDB : {e}")
        return None  # Retourne None en cas d'échec



# ------------- get_all_franchises -------------
#
# Description:
# Cette fonction récupère les noms de toutes les bases de données (franchises)
# contenant "fr" dans leur nom, à partir de la base de données MariaDB.
#
# Fonctionnement:
# 1. Se connecte à la base de données en utilisant db_connect().
# 2. Exécute une requête SQL pour récupérer les noms des bases de données
#    dont le nom contient "fr", en utilisant la table information_schema.SCHEMATA.
# 3. Stocke les résultats de la requête dans une liste.
# 4. Ferme proprement la connexion à la base de données.
# 5. Retourne la liste des noms de bases de données.
#
# Exemple d'utilisation:
# franchises = get_all_franchises()
# - 'franchises' contiendra une liste des noms de bases de données
#   contenant "fr" dans leur nom.
#
# Retour:
# - Une liste des noms de bases de données (franchises) contenant "fr".
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




# ------------- get_NetworkScan_data -------------
# ------------- get_Harvester_data -------------
#
# Description:
# Cette fonction récupère les données de la table 'NetworkScan'
# pour une franchise spécifiée dans une base de données MariaDB.
#
# Fonctionnement:
# 1. Connexion à la base de données en utilisant db_connect().
# 2. Sélection de la base de données correspondant à la franchise spécifiée.
# 3. Exécution d'une requête SQL pour récupérer toutes les données de la table 'NetworkScan'.
# 4. Stockage des résultats de la requête dans une variable.
# 5. Fermeture de la connexion à la base de données.
# 6. Création d'un dictionnaire pour stocker les données récupérées.
# 7. Parcours des résultats et création d'une instance de la classe NetworkScan pour chaque ligne.
# 8. Retourne un dictionnaire contenant les instances de NetworkScan.
#
# Exemple d'utilisation:
# data = get_NetworkScan_data(franchise)
# - data[0] contient la première ligne de la table 'NetworkScan'.
# - data[0].Hostname contient la valeur de la colonne 'Hostname' de la première ligne.
#
# Arguments:
# - franchise: Nom de la franchise (base de données) à utiliser.
# - franchise: Peut être le nom explicite d'une franchise ou une variable contenant ce nom.
#              l'argument n'est valide que si la franchise existe dans la base de données.
#
# Retour de fonction:
# - Dictionnaire contenant les données de la table 'NetworkScan'.
#
# ------------------------------------------------

import json


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
        cur.execute(" SELECT Scan_ID, Harvester_ID, Scan_Rapport, Scan_Date FROM NetworkScan ORDER BY Scan_Date DESC ")
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

            for entrees in rapport_de_scan:
                ports_ouverts = ", ".join(map(str, entrees['ports_ouverts']))
                formatted_entrees = (
                    f"IP: {entrees['ip']}, Nom d'Hôte: {entrees['nom_hote']}, "
                    f"Ports Ouverts: {ports_ouverts}"
                )
                entrees_formatees.append(formatted_entrees)

            data[scan['scan_id']] = {
                'Harvester_ID': scan['Harvester_id'],
                'Scan_Date': scan['scan_date'].strftime('%Y-%m-%d %H:%M:%S'),
                'entries': entrees_formatees
            }

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return data




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
