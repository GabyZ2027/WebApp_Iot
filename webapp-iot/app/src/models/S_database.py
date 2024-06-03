import sqlite3
import sys
from time import sleep
from multiprocessing import Process, Queue
from queue import Empty
import sqlite3
import bcrypt

"""
classe DatabaseServer
"""
class DatabaseServer(Process):
    def __init__(self, db_name, max_size, request_queues, response_queues):
        """
        Initializes the DatabaseServer class.

        Args:
            db_name (str): The name of the .db file that stores all the modifications. It should be 'sensors.db'.
            max_size (int): Sets the maximum number of records for the 'sensors' table.
            request_queues (dict): Specifies the dictionary of queues where request orders to the database are received.
            response_queues (dict): Specifies the dictionary of queues where return values from requests are saved.
        """
        super().__init__()
        self.db_name = db_name
        self.max_size = max_size
        self.request_queues = request_queues
        self.response_queues = response_queues
        self.db_connection = None
        self.db_cursor = None

    def run(self):
        """
        Establishes a connection to the database, creates required tables if they don't exist,
        and continuously handles requests received from request queues.
        """
        try:
            self.db_connection = sqlite3.connect(self.db_name)
            self.db_cursor = self.db_connection.cursor()
            self.db_cursor.executescript("""
            CREATE TABLE IF NOT EXISTS SENSORS(
                ID INTEGER NOT NULL,
                DATA TEXT NOT NULL,
                LECTURA TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS USERS(
                NOM TEXT PRIMARY KEY,
                PASSW TEXT                          
            );
            """)
            self.db_connection.commit()

            while True:
                for queue_name, request_queue in self.request_queues.items():
                    try:
                        request = request_queue.get(timeout=0.1) 
                        response = self.handle_request(request)
                        self.response_queues[queue_name].put(response)
                        sleep(1)
                    except Empty:
                        pass

        except sqlite3.Error as e:
            if self.db_connection:
                self.db_connection.rollback()
                self.db_connection.close()
            print("Error %s:" % e.args[0])

    def handle_request(self, request):
        """
        Handles different types of requests received from the request queues.
        Args:
            request (dict): A dictionary representing a request.
        Returns:
            Various: Returns values based on the type of request.
        """
        if request['type'] == 'getLectura':
            return self.get_lectura(request['id'])
        elif request['type'] == 'getLectures':
            return self.get_lectures(request['id'], request['quantitat'])
        elif request['type'] == 'setLectura':
            return self.set_lectura(request['id'], request['lectura'])
        elif request['type'] == 'registerUser':
            return self.register_user(request['username'], request['password'])
        elif request['type'] == 'loginUser':
            return self.login_user(request['username'], request['password'])
        elif request['type'] == 'getUser':
            return self.getUser(request['username'])

    def get_lectura(self, id):
        """
        Retrieves the most recent value and date from the database for the specified ID.
        Args:
            id (int): Represents the ID associated with a sensor or actuator.
                - ID = 0: LED
                - ID = 1: Temperature sensor
                - ID = 2: Humidity sensor
        Returns:
            tuple: A tuple containing the ID, value, and date if found, otherwise None.
        Raises:
            sqlite3.Error: If an error occurs during the database query.
        """
        try:
            self.db_cursor.execute(
                "SELECT LECTURA, DATA FROM SENSORS WHERE ID = ? ORDER BY DATA DESC LIMIT 1",
                (id,)
            )
            lectura = self.db_cursor.fetchone()
            return (id, lectura[0], lectura[1]) if lectura else None
        except sqlite3.Error as e:
            print("Error %s:" % e.args[0])
            return None

    def get_lectures(self, id, quantitat):
        """
        Retrieves the specified number of most recent values from the database for the given ID.
        Args:
            id (int): Represents the ID associated with a sensor or actuator.
                - ID = 0: LED
                - ID = 1: Temperature sensor
                - ID = 2: Humidity sensor
            quantitat (int): The number of most recent values to retrieve.

        Returns:
            tuple: A tuple containing a string identifier and a list of readings.
        Raises:
            sqlite3.Error: If an error occurs during the database query.
        """
        try:
            self.db_cursor.execute(
                "SELECT LECTURA, DATA FROM SENSORS WHERE ID = ? ORDER BY DATA DESC LIMIT ?",
                (id, quantitat)
            )
            lecturas = self.db_cursor.fetchall()
            return ("get" + str(id), lecturas)
        except sqlite3.Error as e:
            print("Error %s:" % e.args[0])
            return []

    def set_lectura(self, id, lectura):
        """
        Inserts a value into the database in the SENSORS table associated with the specified ID and the current time. If the maximum number of records is surpassed, the oldest one is deleted.
        Args:
            id (int): Represents the ID associated with a sensor or actuator.
                - ID = 0: LED
                - ID = 1: Temperature sensor
                - ID = 2: Humidity sensor
            lectura (str): The value read from a sensor or actuator.
        Returns:
            bool: True if the insertion is successful, False otherwise.
        Raises:
            sqlite3.Error: If an error occurs during the database operation.
        """
        try:
            self.db_cursor.execute("SELECT COUNT(*) FROM SENSORS")
            quant = self.db_cursor.fetchone()[0]
            if quant >= self.max_size:
                self.db_cursor.execute(
                    "DELETE FROM SENSORS WHERE ROWID IN (SELECT ROWID FROM SENSORS ORDER BY ROWID ASC LIMIT 1)"
                )
            self.db_cursor.execute(
                "INSERT INTO SENSORS (ID, DATA, LECTURA) VALUES (?, datetime('now'), ?)",
                (id, lectura)
            )
            self.db_connection.commit()
            return True
        except sqlite3.Error as e:
            self.db_connection.rollback()
            print("Error %s:" % e.args[0])
            return False
        
    def getUser(self, name):
        """
        Checks if the username already exists in the database.
        Args:
            name (str): The username to check.
        Returns:
            bool: True if the username exists, False otherwise.
        Raises:
            sqlite3.Error: If an error occurs during the database query.
        """
        try:
            self.db_cursor.execute("SELECT NOM FROM USERS WHERE NOM = ?", (name,))
            lectura = self.db_cursor.fetchone()
            return True if lectura else False    
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def register_user(self, username, password):
        """
        Registers a new user in the database with the specified username and password hash (bcrypt).
        Args:
            username (str): The username to register.
            password (str): The password to hash and store.
        Returns:
            bool: True if the user is registered successfully, False if the username already exists.
        Raises:
            sqlite3.Error: If an error occurs during the database operation.
        """
        try:
            if self.getUser(username) is False:
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                self.db_cursor.execute("INSERT INTO USERS (NOM, PASSW) VALUES (?, ?)", (username, hashed_password))
                self.db_connection.commit()
                return True
            else:
                return False
        except sqlite3.Error as e:
            self.db_connection.rollback()
            print("Error %s:" % e.args[0])
            return False

    def login_user(self, name, passw):
        """
        Authenticates a user by verifying the provided password against the stored hash.
        Args:
            name (str): The username to authenticate.
            passw (str): The password to verify.
        Returns:
            bool or None: True if the authentication is successful, False if the password is incorrect, None if the username does not exist.
        Raises:
            sqlite3.Error: If an error occurs during the database query.
        """
        try:
            if self.getUser(name) == True:
                self.db_cursor.execute("SELECT PASSW FROM USERS WHERE NOM = ?", (name,))
                lectura = self.db_cursor.fetchone()
                hash = lectura[0]
                epassw = passw.encode()
                if bcrypt.checkpw(epassw,hash):
                    return True     
                else:
                    return False    
            else:  
                return None         
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def close_connection(self):
        """
        Closes the connection to the database.
        Returns:
            None
        """
        if self.db_connection:
            self.db_connection.close()


"""
def main():
    request_queue = Queue()
    response_queue = Queue()
     
    db_server = DatabaseServer('sensors.db', 1000, request_queue, response_queue)
    db_server.start()

    # Esperar a que el servidor de base de datos se inicie
    sleep(1)
    # Test setLectura
    request_queue.put({'type': 'setLectura', 'id': 1, 'lectura': '25.0'})
    sleep(3)  # Esperar a que la base de datos procese la solicitud
    response = response_queue.get()
    print(f'setLectura response: {response}')

    # Test getLectura
    request_queue.put({'type': 'getLectura', 'id': 1})
    sleep(3)  # Esperar a que la base de datos procese la solicitud
    response = response_queue.get()
    print(f'getLectura response: {response}')

    # Test setLectura multiple times to test max size
    for i in range(10):
        request_queue.put({'type': 'setLectura', 'id': 2, 'lectura': f'{i}.0'})
        sleep(3)  # Esperar a que la base de datos procese la solicitud
        response = response_queue.get()
        print(f'setLectura response: {response}')
    # Test getLectures
    request_queue.put({'type': 'getLectures', 'id': 0, 'quantitat': 10})
    sleep(3)  # Esperar a que la base de datos procese la solicitud
    response = response_queue.get()
    print(f'getLectures response: {response}')

    # Finalizar el servidor de base de datos
    request_queue.put(None)
    db_server.join()

if __name__ == "__main__":
    main()
"""

"""
# Ahora puedes usar esta clase `DatabaseServer` como servidor de base de datos


class Sensors_BD():

    def __init__(self, nom, max):

        try:
            self.__max = max
            self.__con = sqlite3.connect(nom)
            self.__cur = self.__con.cursor()  
            self.__cur.executescript("""
"""     
            CREATE TABLE IF NOT EXISTS SENSORS( 
            ID INTEGER NOT NULL,
            DATA DATE NOT NULL,
            LECTURA TEXT NOT NULL,
            PRIMARY KEY (ID, DATA)
            );
            )"""
"""
            self.__con.commit()
            
            
        except sqlite3.Error as e:
            if self.__con:
                self.__con.rollback()
                self.__con.close()
                print("Error %s:" % e.args[0])

    def getLectura(self,id):
        try:
            self.__cur.execute("SELECT LECTURA,DATA FROM SENSORS WHERE ID = ? AND DATA = (SELECT MAX(DATA) FROM SENSORS WHERE ID = ?)", (id, id))
            lectura = self.__cur.fetchone()
            resultat = (lectura[0],lectura[1])
            return resultat
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def getLectures(self, id, quantitat):
        try:
            self.__cur.execute("SELECT LECTURA,DATA FROM SENSORS WHERE ID = ? ORDER BY DATA DESC LIMIT ?", (id, quantitat))
            lectura = self.__cur.fetchall()
            lectura_rect = []
            for tupla in lectura:
                lectura_rect.append((tupla[0],tupla[1]))
            return lectura_rect
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def setLectura(self, id, lectura):
        try:
            self.__cur.execute("SELECT COUNT(*) FROM SENSORS")
            quant = self.__cur.fetchone()
            if (quant[0] >= self.__max):
                self.__cur.execute("DELETE FROM SENSORS WHERE ROWID = (SELECT ROWID FROM SENSORS WHERE ID = ? ORDER BY DATA ASC LIMIT 1)", (id,))
                self.__con.commit() 
            self.__cur.execute("INSERT INTO SENSORS VALUES (?, CURRENT_TIMESTAMP, ?)", (id,lectura))
            self.__con.commit()        
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def sortir(self):
        self.__con.close()

    def exportSen(self):
        f=open("ExportDataS.txt","w")
        try:
            listt=self.__cur.execute('SELECT * FROM SENSORS')
            for row in listt:
                f.write(str(row)+"\n")
            f.close()
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])
"""
