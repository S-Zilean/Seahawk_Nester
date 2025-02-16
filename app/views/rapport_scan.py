from flask import render_template, redirect, url_for, session
from db_helper.db_data import get_all_franchises

def init_rapport_scan(app):
    @app.route('/rapport_scan')
    def rapport_scan():
        
        list = []
        for value in get_all_franchises():
            list.append(value)


        if "username" in session:
            return render_template('rapport_scan.html', franchises=list)
        return redirect(url_for('authentification'))