import sys
sys.dont_write_bytecode = True
from flask import *
from flask import render_template, session, redirect, url_for
from .auth import login_required

def init_index(app):
    @app.route('/')
    def index():
        return redirect(url_for('authentification'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')