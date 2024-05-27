from flask import Flask,Blueprint,render_template, request, redirect, url_for, flash, session

from config import Config

from src.models.U_database import Usuaris_BD

auth_blueprint = Blueprint('auth_blueprint',__name__)

usuaris_BD= Usuaris_BD("usuaris.db")

#@login_manager_app.user_loader
"""
@auth_blueprint.route('/')
def index():
    return redirect(url_for('auth_blueprint.login'))
"""

@auth_blueprint.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            if usuaris_BD.register(username,password):
                flash('Registration successful.', 'success')
                return redirect(url_for('auth_blueprint.login'))
            else:
                flash('Username already exists.', 'error')
                return render_template('register.html')
        else:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
    else:
        return render_template('register.html')

@auth_blueprint.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if usuaris_BD.login(username,password):
            session['username'] = username
            flash('Registration successful.', 'success')
            return redirect(url_for('auth_blueprint.home'))
        else:
            flash('Username already exists.', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout successful.', 'success')
    return redirect(url_for('auth_blueprint.login'))
    
@auth_blueprint.route('/home')
def home():
    return render_template('home.html')

def status_401(error):
    return redirect(url_for('auth_blueprint.login'))


def status_404(error):
    return "<h1>Page not found</h1>", 404

    
    
