## Project Structure

```
app/src/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── kafka.py
│   └── S_database.py
├── routes/
│   ├── api.py
│   ├── AuthApi.py
│   └── __init__.py
├── services/
│   ├── DataAcquisitionService.py
│   └── __init__.py
├── static/
│   ├── css/
│   │   ├── login.css
│   │   └── style.css
│   ├── img/
│   │   └── Logo_UPC.png
│   └── js/
│       ├── script.js
│       └── script_regist.js
└── templates/
    ├── __init__.py
    ├── home_guest.html
    ├── home.html
    ├── layout.html
    ├── login.html
    ├── register.html
    └── template.html
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
```

## Running the Application

1. **Start the Flask application**:
    ```bash
    python app.py
    ```

2. **Navigate to** `http://127.0.0.1:5000/` in your web browser to view the application.

## Application Components

### app/src/\_\_init\_\_.py

This is the main entry point of the Flask application. It initializes all the services and sets up the necessary routes.

### models/

This directory contains modules related to data models and message handling.

- **kafka.py**: Contains the `KafkaManager` class which manages Kafka producers and consumers.
- **S_database.py**: Manages interactions with the SQLite database.

### routes/

This directory contains modules related to defining routes and API endpoints.

- **api.py**: Defines general API routes.
- **AuthApi.py**: Defines authentication-related API routes.

### services/

This directory contains modules related to business logic and service layers.

- **DataAcquisitionService.py**: Contains the `DataAcquisitionService` class for handling data acquisition tasks.

### static/

This directory contains static files such as CSS, JavaScript, and images.

- **css/**: Contains CSS files for styling the application.
  - **login.css**
  - **style.css**
- **img/**: Contains image files used in the application.
  - **Logo_UPC.png**
- **js/**: Contains JavaScript files for client-side logic.
  - **script.js**
  - **script_regist.js**

### templates/

This directory contains HTML templates for the Flask application.

- **home_guest.html**: Template for guest home page.
- **home.html**: Template for user home page.
- **layout.html**: Base layout template.
- **login.html**: Template for login page.
- **register.html**: Template for registration page.
- **template.html**: General template for other pages.

By following this structure and setup guide, you should be able to get your Flask application up and running, leveraging both MQTT and Kafka for messaging.
