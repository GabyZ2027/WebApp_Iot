from flask import Flask, render_template, redirect, url_for
from src import init_app

app = init_app()

@app.route('/')
def index():
    """
    Redirects to the login page.

    Returns:
        Response: A redirect response object to the login page.
    """
    return redirect(url_for('auth_blueprint.login'))

def status_401(error):
    """
    Handles 401 Unauthorized errors by redirecting to the login page.

    Args:
        error (Exception): The exception that was raised.

    Returns:
        Response: A redirect response object to the login page.
    """
    return redirect(url_for('auth_blueprint.login'))

def status_404(error):
    """
    Handles 404 Not Found errors by returning a custom error message.

    Args:
        error (Exception): The exception that was raised.

    Returns:
        tuple: A tuple containing an error message and a 404 status code.
    """
    return "<h1>Page not found</h1>", 404

if __name__ == '__main__':
    try:
        app.register_error_handler(401, status_401)
        app.register_error_handler(404, status_404)
        app.run(host='194.164.172.230',port=443,ssl_context=('certs/cert.pem', 'certs/key.pem'))
        # app.run(debug=True)
    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")
    finally:
        # Detener los consumidores al finalizar la aplicación
        app.data_acquisition_process.join()
        # app.mqtt_kafka_bridge.stop()

