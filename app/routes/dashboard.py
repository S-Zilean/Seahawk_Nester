from flask import render_template
from app.fonctions import login_required, get_all_franchises

def init_dashboard(app):
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Récupération de toutes les franchises
        temp_franchises = get_all_franchises()

        # Création de la liste des franchises
        list_franchises = [franchise for franchise in temp_franchises]

        return render_template('dashboard.html')
