from flask import render_template, redirect, url_for, session

def init_remote_access(app):
    @app.route('/remote_access')
    def remote_access():
        if "username" in session:
            return render_template('remote_access.html')
        return redirect(url_for('authentification'))