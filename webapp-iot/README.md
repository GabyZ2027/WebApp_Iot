## Project Structure

```
webapp_iot/app/
├── app.py
├── config.py
├── models/
│   ├── database.py
│   ├── __init__.py
│   ├── kafka.py
│   └── mqtt_kafka_bridge.py
├── routes/
│   ├── api.py
│   ├── AuthApi.py
│   └── __init__.py
├── services/
│   ├── DataAcquisitionService.py
│   └── __init__.py
└── templates/
    ├── index.html
    └── __init__.py
```

## Setup

### Prerequisites

Ensure you have Python installed on your system. It is recommended to use a virtual environment to manage your project dependencies.

### Virtual Environment

1. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

### Install Dependencies

Install the necessary dependencies using `pip`:

```bash
pip install Flask paho-mqtt pykafka
```

### Generate `requirements.txt`

To generate the `requirements.txt` file, which captures the exact versions of the libraries used in your environment:

```bash
pip freeze > requirements.txt
```

### Using the `requirements.txt` File

When setting up the project on a different machine or for the first time, use the `requirements.txt` file to install the necessary dependencies:

```bash
pip install -r requirements.txt
```lask_app

## Running the Application

1. **Start the Flask application**:
    ```bash
    python app.py
    ```

2. **Navigate to** `http://127.0.0.1:5000/` in your web browser to view the application.

## Application Components

### app.py

This is the main entry point of the Flask application. It initializes the Kafka consumer and the MQTT-Kafka bridge, and sets up the necessary routes.

### models/

This directory contains modules related to data models and message handling.

- **database.py**: Manages interactions with the SQLite database.
- **kafka.py**: Contains the `KafkaManager` class which manages Kafka producers and consumers.
- **mqtt_kafka_bridge.py**: Contains the `MQTTKafkaBridge` class that bridges messages between MQTT and Kafka.

### routes/

This directory contains modules related to defining routes and API endpoints.

- **api.py**: Defines general API routes.
- **AuthApi.py**: Defines authentication-related API routes.

### services/

This directory contains modules related to business logic and service layers.

- **DataAcquisitionService.py**: Contains the `DataAcquisitionService` class for handling data acquisition tasks.

### templates/

This directory contains HTML templates for the Flask application.

- **index.html**: The main HTML template for the application.
