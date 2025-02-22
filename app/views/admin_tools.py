from flask import render_template, request, session, flash, redirect, url_for
from app.db_helper import db_connection, db_query, db_data
from app.db_helper import get_table_data, get_specific_data

def init_admin_tools(app):
    @app.route('/admin_tools', methods=['GET', 'POST'])
    def gestion_acces():
        # Vérifier si l'utilisateur est connecté
        if "username" not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "error")
            return redirect(url_for('authentification'))
        




        # Récupérer le groupe de l'utilisateur depuis la base de données
        con = db_connection.db_connect()

        # Vérifier si la connexion à la base de donnée à réussie
        if not con:
            flash("Erreur de connexion à la base de données.", "error")
            return redirect(url_for('index'))
        
        cur = con.cursor()
        cur.execute("USE NFL_IT")

        req = "SELECT Groupe FROM Users WHERE username = %s"
        cur.execute(req, (session['username'],))
        user_data = cur.fetchone()


        if not user_data:
            flash("Erreur lors de la récupération des informations utilisateur.", "error")
            return redirect(url_for('dashboard'))

        user_group = user_data[0]  # Supposons que le groupe est dans la 1ère colonne

        # Vérification des droits d'accès
        if user_group not in ["admin", "superuser", "root"]:
            flash("Accès réservé à l'administrateur.", "error")
            return redirect('dashboard')

        # Récupérer les utilisateurs depuis la base de données
        users_data = get_table_data('NFL_IT', "Users")
        if not users_data:
            flash("Erreur lors de la récupération des utilisateurs.", "error")
            return redirect(url_for('dashboard'))

        users = [{"user_id": user[0], "username": user[1], "group": user[3]} for user in users_data]

        # Gestion de l'ajout d'un nouvel utilisateur
        if request.method == 'POST':
            new_username = request.form.get('username')
            new_password = request.form.get('password')
            new_group = request.form.get('groupe')

            # Vérifier si l'utilisateur existe déjà
            if any(user['username'] == new_username for user in users):
                flash("Cet utilisateur existe déjà.", "error")
            else:
                insert_query = "INSERT INTO Users (username, PASSWORD(password), group, creation_date) VALUES (%s, %s, %s, NOW())"
                db_query.do_request(insert_query, (new_username, new_password, new_group))
                flash("Utilisateur ajouté avec succès.", "success")
        return render_template('admin_tools.html', users=users)