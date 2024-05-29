from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from multiprocessing import Queue

# Create the Blueprint
auth_blueprint = Blueprint('auth_blueprint', __name__)

# Initialize LoginManager
login_manager = LoginManager()

def set_queues(s_request_queues, s_response_queues):
    global request_queues, response_queues
    request_queues = s_request_queues
    response_queues = s_response_queues

def send_request(queue_name, request):
    request_queues[queue_name].put(request)
    return response_queues[queue_name].get()

class User(UserMixin):
    def __init__(self, username):
        self.id = username  # Flask-Login requires an `id` attribute
        self.username = username

@login_manager.user_loader
def load_user(username):
    response = send_request('auth', {'type': 'getUser', 'username': username})
    if response:
        return User(username)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth_blueprint.login'))

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
            user = User(username)
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('auth_blueprint.home'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/home')
@login_required
def home():
    return render_template('home.html')

@auth_blueprint.route('/home-guest')
def home_guest():
    return render_template('home_guest.html')
