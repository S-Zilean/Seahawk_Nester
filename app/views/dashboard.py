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
        return render_template('dashboard.html')
