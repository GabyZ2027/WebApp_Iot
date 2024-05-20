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
