from flask import render_template, request, session, flash, redirect, url_for
from app.db_helper import db_connection, db_query
from app.db_helper.db_data import get_table_data

def init_admin_tools(app):
    @app.route('/gestion_acces', methods=['GET', 'POST'])
    def gestion_acces():
        # Vérifier si l'utilisateur est connecté
        if "username" not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "error")
            return redirect(url_for('authentification'))

        # Récupérer le groupe de l'utilisateur depuis la base de données
        con = db_connection()
        if not con:
            flash("Erreur de connexion à la base de données.", "error")
            return redirect(url_for('index'))
        
        cur = con.cursor()
        cur.execute("USE Users")

        req = "SELECT `Groupe` FROM Users WHERE username = %s"
        cur.execute(req, (session['username'],))
        user_data = cur.fetchone()
        cur.close()
        con.close()

        if not user_data:
            flash("Erreur lors de la récupération des informations utilisateur.", "error")
            return redirect(url_for('index'))

        user_group = user_data[0]  # Supposons que le groupe est dans la 1ère colonne

        # Vérification des droits d'accès
        if user_group not in ["admin", "superuser", "root"]:
            flash("Accès réservé à l'administrateur.", "error")
            return redirect(url_for('index'))

        # Récupérer les utilisateurs depuis la base de données
        users_data = get_table_data('Users', "Users")
        if not users_data:
            flash("Erreur lors de la récupération des utilisateurs.", "error")
            return redirect(url_for('index'))

        users = [{"user_id": user[0], "username": user[1], "group": user[3]} for user in users_data]

        # Gestion de l'ajout d'un nouvel utilisateur
        if request.method == 'POST':
            new_username = request.form.get('username')
            new_password = request.form.get('password')
            new_group = request.form.get('group')

            # Vérifier si l'utilisateur existe déjà
            if any(user['username'] == new_username for user in users):
                flash("Cet utilisateur existe déjà.", "error")
            else:
                insert_query = "INSERT INTO Users (username, password, `group`, creation_date) VALUES (%s, %s, %s, NOW())"
                db_query(insert_query, (new_username, new_password, new_group))
                flash("Utilisateur ajouté avec succès.", "success")

        return render_template('gestion_acces.html', users=users)