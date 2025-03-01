import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.fonctions.db_requests import get_all_franchises, getall_NetworkScan_data
import json

all_franchises = get_all_franchises()

def test_getall_NetworkScan_data(all_franchises):

    for nom_franchise in all_franchises:
        scans = getall_NetworkScan_data(nom_franchise)

        scan_convert = json.loads(scans.get(2).key["scan_report"])
        for entry in scan_convert:
            entry['ip'] = 'ip'
            entry['nom_dhote'] = "nom d'hôte"
            entry['ports_ouverts'] = 'ports ouverts'
            print(entry)

    


test_getall_NetworkScan_data(all_franchises)