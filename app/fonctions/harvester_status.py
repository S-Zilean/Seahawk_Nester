import subprocess
from app.fonctions import db_connect
import mariadb

# ------------- update_harvester_status -------------
#
# Description:
# Cette fonction met à jour l'état des harvesters (collecteurs) dans une base de données en fonction de leur réponse à une requête ping.
# Elle vérifie si chaque harvester est accessible via son adresse IP et met à jour son état (connecté ou déconnecté) dans la base de données.
#
# Fonctionnement:
# 1. Se connecte à la base de données en utilisant la fonction `db_connect()`.
# 2. Sélectionne la base de données spécifique à la franchise.
# 3. Récupère les adresses IP des harvesters depuis la table `Harvester`.
# 4. Pour chaque harvester, envoie une requête ping à son adresse IP.
# 5. Met à jour l'état du harvester dans la base de données en fonction du résultat du ping.
# 6. Gère les exceptions et ferme les connexions à la base de données.
#
# Exemple d'utilisation:
# update_harvester_status('nom_de_la_franchise')
#
# Arguments:
# - franchise: Le nom de la franchise dont la base de données doit être utilisée.
#
# Retour:
# - Aucun retour explicite, mais imprime des messages indiquant le statut du ping et les erreurs éventuelles.
#
# ------------------------------------------------

def update_harvester_status(franchise):
    # Connexion à la base de données
    conn = db_connect()
    if conn is None:
        print("Échec de la connexion à la base de données.")
        return

    cur = conn.cursor()

    try:
        # Sélectionner la base de données de la franchise
        cur.execute(f"USE {franchise}")

        # Récupérer les adresses IP des harvesters
        cur.execute("SELECT Harvester_ID, Harvester_IP FROM Harvester")
        harvesters = cur.fetchall()

        for harvester in harvesters:
            harvester_id, ip_address = harvester

            # Message indiquant le début du ping
            print(f"Envoi d'un ping à {ip_address}...")

            # Envoyer une requête ping avec un timeout de 1 seconde
            try:
                result = subprocess.run(
                    ["/usr/bin/sudo", "ping", "-c", "1", "-W", "1", ip_address],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                if result.returncode == 0:
                    harvester_state = 1  # Connected
                    print(f"Ping réussi pour {ip_address} - Connected")
                else:
                    harvester_state = 0  # Disconnected
                    print(f"Ping échoué pour {ip_address} - Disconnected")
            except Exception as e:
                print(f"Erreur lors du ping de {ip_address}: {e}")
                harvester_state = 0  # Disconnected

            # Mettre à jour l'état du harvester dans la base de données
            cur.execute("UPDATE Harvester SET Harvester_State = %s WHERE Harvester_ID = %s", (harvester_state, harvester_id))
            conn.commit()

    except mariadb.Error as e:
        print(f"Erreur de base de données: {e}")

    finally:
        cur.close()
        conn.close()
