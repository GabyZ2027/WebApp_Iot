from flask import Flask,Blueprint,render_template, request

from config import Config

auth_blueprint = Blueprint('auth_blueprint',__name__)

@auth_blueprint.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

"""
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticación aquí
        return redirect(url_for('api_blueprint.dashboard'))  # Redirigir a una página protegida después de iniciar sesión
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    # Lógica de cierre de sesión aquí
    return redirect(url_for('auth_blueprint.login'))
"""