from flask import session, redirect, url_for, request, render_template
from functools import wraps
from app.db_helper.db_connection import db_connect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.html'))
        return f(*args, **kwargs)
    return decorated_function

def init_authentification(app):
    @app.route('/auth.html', methods=['GET', 'POST'])
    def authentification():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Vérification des informations d'identification dans la base de données

            cur = db_connect().cursor()
            cur.execute("USE Users")
            req = "SELECT * FROM Users WHERE username = %s AND password = %s"
            cur.execute(req, (username, password))
            user = cur.fetchone()            
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return 'Nom d\'utilisateur ou mot de passe incorrect'
        return render_template('auth.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('auth.html'))


