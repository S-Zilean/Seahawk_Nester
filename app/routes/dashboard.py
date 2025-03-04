from flask import render_template
from app.fonctions import login_required, get_all_franchises

def init_dashboard(app):
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
