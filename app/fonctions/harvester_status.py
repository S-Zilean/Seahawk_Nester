import subprocess
from app.fonctions import db_connect
import mariadb

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
                    ["/usr/bin/sudo", "ping", "-c", "1", "-W", "0.3", ip_address],
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
