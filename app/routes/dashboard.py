from flask import render_template
from app.fonctions.user_session import login_required
from app.fonctions.db_database import get_all_databases

def init_dashboard(app):
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Récupération de toutes les franchises
        temp_franchises = get_all_databases()

        # Création de la liste des franchises
        list_franchises = [franchise for franchise in temp_franchises]

        return render_template('dashboard.html')
