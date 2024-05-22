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

class Sensors_BD():

    def __init__(self, nom, max):

        try:
            self.__max = max
            self.__con = sqlite3.connect(nom)
            self.__cur = self.__con.cursor()  
            self.__cur.executescript("""     
            CREATE TABLE IF NOT EXISTS SENSORS( 
            ID INTEGER NOT NULL,
            DATA DATE NOT NULL,
            LECTURA TEXT NOT NULL,
            PRIMARY KEY (ID, DATA)
            );
            """)
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


                    
        
    
                

                    
        

        

