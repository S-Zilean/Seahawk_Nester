from flask import render_template, request, redirect, url_for, session


def init_modalites_pem(app):
  @app.route('/modalites_pem', methods=['GET', 'POST'])
  def modalites_pem():
      if "username" not in session:
          return redirect(url_for('authentification'))

      sondes = {
          "franchise1": {"franchise": "Franchise 1", "ip": "192.168.1.1", "username": "admin1", "password": "pass1"},
          "franchise2": {"franchise": "Franchise 2", "ip": "192.168.2.1", "username": "admin2", "password": "pass2"},
          "franchise3": {"franchise": "Franchise 3", "ip": "192.168.3.1", "username": "admin3", "password": "pass3"},
      }

      selected_sonde = None
      if request.method == 'POST':
          sonde_id = request.form.get('sonde')
          selected_sonde = sondes.get(sonde_id)

      return render_template('modalites_pem.html', selected_sonde=selected_sonde)