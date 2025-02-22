from flask import render_template, request, session, flash, redirect, url_for
from app.db_helper import db_connection, db_query, db_data
from app.db_helper import get_table_data, get_specific_data
from app.helper.user_session import get_user_role

def init_admin_tools(app):
    @app.route('/admin_tools', methods=['GET', 'POST'])
    def gestion_acces():
        # Vérifier si l'utilisateur est connecté
        if "username" not in session:
            flash("Vous devez être connecté pour accéder à cette page.", "error")
            return redirect(url_for('authentification'))
        
        if get_user_role() not in ["admin"]:
            flash("Accès réservé à l'administrateur.", "error")
            return redirect(url_for('dashboard'))

        # Récupérer les utilisateurs depuis la base de données
        users_data = get_table_data('NFL_IT', "Users")
        if not users_data:
            flash("Erreur lors de la récupération des utilisateurs.", "error")
            return redirect(url_for('dashboard'))

        users = [{"user_id": user[0], "username": user[1], "role": user[3]} for user in users_data]

        return render_template('admin_tools.html', users=users)