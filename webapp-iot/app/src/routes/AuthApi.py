from flask import Flask,Blueprint,render_template, request, redirect, url_for, flash, session
from config import Config
from multiprocessing import Queue


auth_blueprint = Blueprint('auth_blueprint',__name__)


def set_queues(s_request_queues, s_response_queues):
    global request_queues, response_queues
    request_queues = s_request_queues
    response_queues = s_response_queues

def send_request(queue_name, request):
    request_queues[queue_name].put(request)
    return response_queues[queue_name].get()

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            response = send_request('register', {'type': 'registerUser', 'username': username, 'password': password})
            if response:
                flash('Registration successful.', 'success')
                return redirect(url_for('auth_blueprint.login'))
            else:
                flash('Username already exists.', 'error')
        else:
            flash('Passwords do not match.', 'error')
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = send_request('login', {'type': 'loginUser', 'username': username, 'password': password})
        if response:
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('auth_blueprint.home'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout successful.', 'success')
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/home')
def home():
    return render_template('home.html')

@auth_blueprint.route('/home-guest')
def home_guest():
    return render_template('home_guest.html')

def status_401(error):
    return redirect(url_for('auth_blueprint.login'))

def status_404(error):
    return "<h1>Page not found</h1>", 404