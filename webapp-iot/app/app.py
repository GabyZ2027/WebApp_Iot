from flask import Flask, render_template,redirect,url_for
from src import init_app

app=init_app()

@app.route('/')
def index():
    return redirect(url_for('auth_blueprint.login')) 
    
def status_401(error):
    return redirect(url_for('auth_blueprint.login'))


def status_404(error):
    return "<h1>Page not found</h1>", 404

if __name__ == '__main__':
    try:
    	context = ('certs/cert.pem', 'certs/key.pem')
    	app.register_error_handler(401, status_401)
        app.register_error_handler(404, status_404)
    	app.run(debug=True,port=443, ssl_context=context) 
    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")
    finally:
        # Detener los consumidores al finalizar la aplicación
        app.data_acquisition_process.join()
        #app.mqtt_kafka_bridge.stop()
