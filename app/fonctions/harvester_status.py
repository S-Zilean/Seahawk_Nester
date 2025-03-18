# Importe le module subprocess pour exécuter des commandes système
import subprocess

# Importe la fonction db_connect depuis le module fonctions dans le package app
from app.fonctions import db_connect

# Importe le module mariadb pour interagir avec la base de données MariaDB
import mariadb

# Définition de la fonction update_harvester_status
def update_harvester_status(franchise):

    # Connexion à la base de données
    conn = db_connect()

    # Crée un curseur pour exécuter des requêtes SQL
    cur = conn.cursor()

    try:

        # Utilise la base de données spécifiée par le paramètre franchise
        cur.execute(f"USE {franchise}")

        # Exécute une requête SQL pour obtenir les IDs et IPs des harvesters
        cur.execute("SELECT Harvester_ID, Harvester_IP FROM Harvester")

        # Récupère tous les résultats de la requête
        harvesters = cur.fetchall()

        # Parcourt chaque harvester
        for harvester in harvesters:

            # Décompose chaque tuple en ID et adresse IP
            harvester_id, ip_address = harvester

            # Affiche un message indiquant que le ping commence
            print(f"Envoi d'un ping à {ip_address}...")

            # Exécute la commande ping avec un timeout de 1 seconde
            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "1", ip_address]
                )

                # Vérifie si le ping a réussi
                if result.returncode == 0:

                    # Connected
                    harvester_state = 1

                    # Affiche un message de succès
                    print(f"Ping réussi pour {ip_address} - Connected")
                else:

                    # Disconnected
                    harvester_state = 0

                    # Affiche un message d'échec
                    print(f"Ping échoué pour {ip_address} - Disconnected")

            # Capture toute exception qui pourrait survenir
            except Exception as e:

                # Affiche un message d'erreur
                print(f"Erreur lors du ping de {ip_address}: {e}")

                # Disconnected
                harvester_state = 0

            # Met à jour l'état du harvester dans la base de données
            cur.execute("UPDATE Harvester SET Harvester_State = %s WHERE Harvester_ID = %s", (harvester_state, harvester_id))

            # Valide la transaction
            conn.commit()

    # Capture les erreurs spécifiques à MariaDB
    except mariadb.Error as e:

        # Affiche un message d'erreur
        print(f"Erreur de base de données: {e}")

    finally:

        # Ferme le curseur
        cur.close()

        # Ferme la connexion à la base de données
        conn.close()
