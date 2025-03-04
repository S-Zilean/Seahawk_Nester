from flask import render_template
from app.fonctions import login_required

def init_dashboard(app):
    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
