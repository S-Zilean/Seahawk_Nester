from flask import render_template, request, session, flash, redirect, url_for
from app.helper import db_query
from app.helper.user_session import get_user_role

def init_admin_tools(app):
    @app.route('/admin_tools', methods=['GET', 'POST'])
    def gestion_acces():
        # Vérification de l'authentification et des permissions
        if "username" not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "error")
            return redirect(url_for('authentification'))

        if get_user_role() != "admin":
            flash("Accès réservé à l'administrateur.", "error")
            return redirect(url_for('dashboard'))

        # Gestion de l'ajout d'un utilisateur
        if request.method == 'POST':
            username = request.form.get('username')
            role = request.form.get('role')
            password = request.form.get('password')

            if not username or not password or not role:
                flash("Tous les champs sont obligatoires.", "error")
            else:
                query = "INSERT INTO Users (username, password, role) VALUES (?, PASSWORD(?), ?)"
                result = db_query.do_request(query, (username, password, role))

                if result is not None:
                    flash(f"Utilisateur '{username}' ajouté avec succès.", "success")
                else:
                    flash("Erreur lors de l'ajout de l'utilisateur.", "error")

            return redirect(url_for('gestion_acces'))

        # Récupération des utilisateurs avec des noms de colonnes corrects
        users_data = db_query.db_get_table("Users")

        users = []
        for user in users_data:
            users.append({
                "user_id": user[0], 
                "username": user[1], 
                "role": user[3]  # Ici, on prend bien la colonne 'role'
            })

        return render_template('admin_tools.html', users=users)

    @app.route('/delete_user/<int:user_id>', methods=['POST'])
    def delete_user(user_id):
        """Supprime un utilisateur de la base de données."""
        if "username" not in session or get_user_role() != "admin":
            flash("Accès non autorisé.", "error")
            return redirect(url_for('authentification'))
        
        query = "DELETE FROM Users WHERE user_id = ?"
        result = db_query.do_request(query, (user_id,))
        
        if result is not None:
            flash(f"Utilisateur ID {user_id} supprimé avec succès.", "success")
        else:
            flash("Erreur lors de la suppression de l'utilisateur.", "error")

        return redirect(url_for('gestion_acces'))
