import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.fonctions.db_requests import get_all_franchises, getall_NetworkScan_data
import json

all_franchises = get_all_franchises()


import json

all_franchises = get_all_franchises()

# def test_getall_NetworkScan_data(all_franchises):
#     for nom_franchise in all_franchises:
#         scans = getall_NetworkScan_data(nom_franchise)
#         scan = scans.get(2)
#         if scan is not None:
#             # Assurez-vous que scan.key est un dictionnaire
#             if hasattr(scan, 'key') and isinstance(scan.key, dict) and "scan_report" in scan.key:
#                 test = scan.key["scan_report"]
#                 scan_convert = json.loads(test)
#                 for entry in scan_convert:
#                     print(entry.get("ip"), entry.get("nom_hote"), entry.get("ports_ouverts"))
#             else:
#                 print(f"No valid scan data found for franchise: {nom_franchise}")
#         else:
#             print(f"No scan data found for franchise: {nom_franchise}")

# test_getall_NetworkScan_data(all_franchises)




def test_getall_NetworkScan_data(all_franchises):

    for nom_franchise in all_franchises:
        scans = getall_NetworkScan_data(nom_franchise)

        test = scans.get(2).key["scan_report"]
        
        scan_convert = json.loads(scans.get(2).key["scan_report"])
        for entry in scan_convert:
            print(entry.get("ip"), entry.get("nom_hote"), entry.get("ports_ouverts"))


test_getall_NetworkScan_data(all_franchises)

