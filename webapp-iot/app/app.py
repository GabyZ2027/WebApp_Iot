from flask import Flask, render_template,redirect,url_for
from src import init_app

app=init_app()

@app.route('/')
def index():
    return redirect(url_for('auth_blueprint.login')) 

if __name__ == '__main__':
    try:
        app.run(debug=True,port=5600)
    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")
    finally:
        # Detener los consumidores al finalizar la aplicación
        app.data_acquisition_process.join()
        #app.mqtt_kafka_bridge.stop()
