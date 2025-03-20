# ------------- Harvester Class -------------
#
# Description:
# La classe `Harvester` représente un collecteur (harvester) avec ses attributs associés.
# Elle est utilisée pour encapsuler les données d'un harvester et fournir une représentation textuelle de ces données.
#
# Fonctionnement:
# 1. Le constructeur `__init__` initialise un objet `Harvester` avec un dictionnaire `key` contenant les attributs du harvester.
# 2. Les méthodes `__str__` et `__repr__` fournissent une représentation sous forme de chaîne de caractères de l'objet `Harvester`.
#
# Attributs:
# - id: Identifiant unique du harvester.
# - Etat: État actuel du harvester (par exemple, connecté ou déconnecté).
# - ip: Adresse IP du harvester.
# - Hostname: Nom d'hôte du harvester.
# - Version: Version du logiciel ou du matériel du harvester.
# - Latency: Latence réseau du harvester.
# - Machine_count: Nombre de machines associées au harvester.
#
# Exemple d'utilisation:
# harvester = Harvester([1, 'Connected', '192.168.1.1', 'Harvester01', 'v1.0', 20, 5])
# print(harvester)
#
# Arguments:
# - value: Une liste ou un tuple contenant les valeurs des attributs du harvester dans l'ordre spécifié.
#
# Retour:
# - Les méthodes `__str__` et `__repr__` retournent une représentation sous forme de chaîne de caractères du dictionnaire `key`.
#
# ------------------------------------------------

class Harvester:
    def __init__(self, value):
        self.key = {
            "id": value[0],
            "Etat": value[1],
            "ip": value[2],
            "Hostname": value[3],
            "Version": value[4],
            "Latency": value[5],
            "Machine_count": value[6]
        }

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)
