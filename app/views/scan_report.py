from flask import render_template, Blueprint
from app.helper import get_table_data, get_all_databases
from app.helper.user_session import login_required
import logging


def init_scan_report(app):
    @app.route('/scan_report')
    @login_required

    def rapport_de_scan():
        franchises = get_all_databases()

        for i in franchises:
            print(i)
            report = get_table_data(i, 'NetworkScan')
            print(report)


        # Afficher les rapports de scan
        return render_template('scan_report.html', rapport = report)
