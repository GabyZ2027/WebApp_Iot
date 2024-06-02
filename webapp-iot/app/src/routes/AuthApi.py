from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from multiprocessing import Queue

# Create the Blueprint
auth_blueprint = Blueprint('auth_blueprint', __name__)

# Initialize LoginManager
login_manager = LoginManager()

def set_queues(s_request_queues, s_response_queues):
    """
    Sets the request and response queues for inter-process communication.

    Args:
        s_request_queues (dict): A dictionary of request queues.
        s_response_queues (dict): A dictionary of response queues.
    """
    global request_queues, response_queues
    request_queues = s_request_queues
    response_queues = s_response_queues

def send_request(queue_name, request):
    """
    Sends a request to a specified queue and waits for a response.

    Args:
        queue_name (str): The name of the queue to send the request to.
        request (dict): The request message to send.

    Returns:
        dict: The response message received.
    """
    request_queues[queue_name].put(request)
    return response_queues[queue_name].get()

class User(UserMixin):
    def __init__(self, username):
        """
        Initializes a User object.

        Args:
            username (str): The username of the user.
        """
        self.id = username  # Flask-Login requires an `id` attribute
        self.username = username

@login_manager.user_loader
def load_user(username):
    """
    Loads a user from the user database.

    Args:
        username (str): The username of the user to load.

    Returns:
        User: A User object if the user exists, None otherwise.
    """
    response = send_request('auth', {'type': 'getUser', 'username': username})
    if response:
        return User(username)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """
    Redirects unauthorized users to the login page.

    Returns:
        Response: A redirect response object to the login page.
    """
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    Returns:
        Response: A rendered template for the registration page or a redirect response on successful registration.
    """
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
    """
    Handles user login.

    Returns:
        Response: A rendered template for the login page or a redirect response on successful login.
    """
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
    """
    Logs out the current user.

    Returns:
        Response: A redirect response object to the login page.
    """
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/home')
@login_required
def home():
    """
    Renders the home page for logged-in users.

    Returns:
        Response: A rendered template for the home page.
    """
    return render_template('home.html')

@auth_blueprint.route('/home-guest')
def home_guest():
    """
    Renders the home page for guest users.

    Returns:
        Response: A rendered template for the guest home page.
    """
    return render_template('home_guest.html')

