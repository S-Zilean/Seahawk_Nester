class Harvester :
    def __init__(self, value):
        self.key = {
            "id" : value[0],
            "Etat" : value[1],
            "ip" : value[2],
            "Hostname" : value[3],
            "Version" : value[4],
            "Latency" : value[5],
            "Machine_count" : value[6]
        }

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)