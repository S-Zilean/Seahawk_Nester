from flask import session, redirect, url_for, request, render_template, flash
from functools import wraps
import socket, platform, os

# Définition d'un décorateur pour vérifier si l'utilisateur est connecté
from app.helper.user_session import get_user_role, login_required

    
def init_dashboard(app):
    @app.route('/dashboard')
    @login_required

    def dashboard():        
        if get_user_role() not in ["admin", "technicien"]:
            flash("Accès réservé à l'administrateur.", "error")
            return redirect(url_for('logout'))
        elif get_user_role() in ["admin", "technicien"]:
            return render_template('dashboard.html')