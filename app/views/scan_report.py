from flask import render_template
from app.helper.user_session import login_required
from app.db_helper import get_database


def init_rapport_de_scan(app):
    @app.route('/scan_report')
    @login_required
    def rapport_de_scan():
        return render_template('scan_report.html')