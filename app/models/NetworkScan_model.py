# ------------- NetworkScan Class -------------
#
# Description:
# La classe `NetworkScan` représente un scan réseau avec ses attributs associés.
# Elle est utilisée pour encapsuler les données d'un scan réseau et fournir une représentation textuelle de ces données.
#
# Fonctionnement:
# 1. Le constructeur `__init__` initialise un objet `NetworkScan` avec un dictionnaire `key` contenant les attributs du scan.
# 2. La méthode `__getitem__` permet d'accéder aux valeurs du dictionnaire `key` en utilisant la syntaxe de l'indexation.
# 3. Les méthodes `__str__` et `__repr__` fournissent une représentation sous forme de chaîne de caractères de l'objet `NetworkScan`.
#
# Attributs:
# - scan_id: Identifiant unique du scan réseau.
# - Harvester_id: Identifiant du harvester associé au scan.
# - scan_report: Rapport du scan, généralement sous forme de chaîne JSON.
# - scan_date: Date et heure à laquelle le scan a été effectué.
#
# Exemple d'utilisation:
# network_scan = NetworkScan([1, 101, '{"ip": "192.168.1.1", "ports": [22, 80]}', '2023-10-01 12:00:00'])
# print(network_scan)
# print(network_scan['scan_id'])
#
# Arguments:
# - value: Une liste ou un tuple contenant les valeurs des attributs du scan réseau dans l'ordre spécifié.
#
# Retour:
# - Les méthodes `__str__` et `__repr__` retournent une représentation sous forme de chaîne de caractères du dictionnaire `key`.
# - La méthode `__getitem__` retourne la valeur associée à la clé spécifiée dans le dictionnaire `key`.
#
# ------------------------------------------------

class NetworkScan:
    def __init__(self, value):
        self.key = {
            "scan_id": value[0],
            "Harvester_id": value[1],
            "scan_report": value[2],
            "scan_date": value[3]
        }

    def __getitem__(self, key):
        return self.key[key]

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)
