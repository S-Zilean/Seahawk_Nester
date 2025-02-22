from flask import session, redirect, url_for, request, render_template, flash
from functools import wraps
from app.db_helper.db_connection import db_connect
import socket, platform, os

# Définition d'un décorateur pour vérifier si l'utilisateur est connecté
from app.helper.user_session import login_required

    
def init_dashboard(app):
    @app.route('/dashboard')
    @login_required

    def dashboard():        
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        fqdn = socket.getfqdn()
        os_name = platform.system()
        os_version = platform.version()

        return render_template('dashboard.html', ip_address = ip_address, hostname = hostname, fqdn = fqdn, os_name = os_name, os_version = os_version)
