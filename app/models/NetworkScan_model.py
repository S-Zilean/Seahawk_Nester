class NetworkScan:
    def __init__(self, value):
        self.key = {
            "scan_id" : value[0],
            "Harvester_id" : value[1],
            "scan_report" : value[2],
            "scan_Date" : value[3]
        }

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)