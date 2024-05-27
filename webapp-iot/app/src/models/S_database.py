import sqlite3
import sys

#Utilització:
#Crear la BD
#max = 5000
#nom1 = "sensors.db"
#sensors = SBD.Sensors_BD(nom1,max)
#Utilitzar les id:
#Els metodes et demanane un id, cada id correspon a un sensor/actuador pactem:
#Actudador(LED) = 0
#Sensor(Temperatura) = 1
#Sensor(Humitat) = 2


from multiprocessing import Process, Queue
import sqlite3
from time import sleep

class DatabaseServer(Process):
    def __init__(self, db_name, max_size, request_queue, response_queue):
        super().__init__()
        self.db_name = db_name
        self.max_size = max_size
        self.request_queue = request_queue
        self.response_queue = response_queue
        self.db_connection = None
        self.db_cursor = None

    def run(self):
        try:
            self.db_connection = sqlite3.connect(self.db_name)
            self.db_cursor = self.db_connection.cursor()
            self.db_cursor.executescript("""
            CREATE TABLE IF NOT EXISTS SENSORS(
                ID INTEGER NOT NULL,
                DATA TEXT NOT NULL,
                LECTURA TEXT NOT NULL
            );
            """)
            self.db_connection.commit()

            while True:
                request = self.request_queue.get()
                if request is None:
                    break
                response = self.handle_request(request)
                print("Resposta:",response)
                self.response_queue.put(response)

        except sqlite3.Error as e:
            if self.db_connection:
                self.db_connection.rollback()
                self.db_connection.close()
                print("Error %s:" % e.args[0])

    def handle_request(self, request):
        if request['type'] == 'getLectura':
            return self.get_lectura(request['id'])
        elif request['type'] == 'getLectures':
            return self.get_lectures(request['id'], request['quantitat'])
        elif request['type'] == 'setLectura':
            return self.set_lectura(request['id'], request['lectura'])

    def get_lectura(self, id):
        try:
            self.db_cursor.execute(
                "SELECT LECTURA, DATA FROM SENSORS WHERE ID = ? ORDER BY ROWID DESC LIMIT 1",
                (id,)
            )
            lectura = self.db_cursor.fetchone()
            return (lectura[0], lectura[1]) if lectura else None
        except sqlite3.Error as e:
            print("Error %s:" % e.args[0])
            return None

    def get_lectures(self, id, quantitat):
        try:
            self.db_cursor.execute(
                "SELECT LECTURA, DATA FROM SENSORS WHERE ID = ? LIMIT ?",
                (id, quantitat)
            )
            lecturas = self.db_cursor.fetchall()
            print(lecturas)
            return(lecturas)
            #return [(lectura[0], lectura[1]) for lectura in lecturas]
        except sqlite3.Error as e:
            print("Error %s:" % e.args[0])
            return []

    def set_lectura(self, id, lectura):
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

    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()

def main():
    request_queue = Queue()
    response_queue = Queue()
     
    db_server = DatabaseServer('sensors.db', 1000, request_queue, response_queue)
    db_server.start()

    # Esperar a que el servidor de base de datos se inicie
    sleep(1)
    """
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
    """
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