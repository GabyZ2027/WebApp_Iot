import sqlite3
import sys

class Sensors_BD():

    def __init__(self, nom, max):

        try:
            self.__max = max
            self.__con = sqlite3.connect(nom)
            self.__cur = self.__con.cursor()  
            self.__cur.executescript("""
            
            CREATE TABLE IF NOT EXISTS SENSORS( 
            SENSOR TEXT NOT NULL,
            DATA DATE NOT NULL,
            LECTURA TEXT NOT NULL,
            PRIMARY KEY (SENSOR, DATA)
            );
            
            CREATE TABLE IF NOT EXISTS USERS(
            NOM TEXT PRIMARY KEY,
            PASSW TEXT                          
            );
            """)
            self.__con.commit()
            
            
        except sqlite3.Error as e:
            if self.__con:
                self.__con.rollback()
                self.__con.close()
                print("Error %s:" % e.args[0])

    def getLecturaAct(self):
        try:
            self.__cur.execute("SELECT LECTURA FROM SENSORS WHERE SENSOR = '0' AND DATA = (SELECT MAX(DATA) FROM SENSORS WHERE SENSOR = '0')")
            lectura = self.__cur.fetchone()
            return lectura[0] if lectura else None
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def getLecturesAct(self, quantitat):
        try:
            self.__cur.execute("SELECT LECTURA FROM SENSORS WHERE SENSOR = '0' ORDER BY DATA DESC LIMIT ?", (quantitat,))
            lectura = self.__cur.fetchall()
            lectura_rect = [tupla[0] for tupla in lectura]
            return lectura_rect
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def getLecturaSen(self):
        try:
            self.__cur.execute("SELECT LECTURA FROM SENSORS WHERE SENSOR = '1' AND DATA = (SELECT MAX(DATA) FROM SENSORS WHERE SENSOR = '1')")
            lectura = self.__cur.fetchone()
            return lectura[0] if lectura else None
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def getLecturesSen(self, quantitat):
        try:
            self.__cur.execute("SELECT LECTURA FROM SENSORS WHERE SENSOR = '1' ORDER BY DATA DESC LIMIT ?", (quantitat,))
            lectura = self.__cur.fetchall()
            lectura_rect = [tupla[0] for tupla in lectura]
            return lectura_rect
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def setLecturaAct(self, lectura):
        try:
            self.__cur.execute("SELECT COUNT(*) FROM SENSORS")
            quant = self.__cur.fetchone()
            if (quant[0] >= self.__max):
                self.__cur.execute("DELETE FROM SENSORS WHERE ROWID = (SELECT ROWID FROM SENSORS WHERE SENSOR = '0' ORDER BY DATA ASC LIMIT 1)")
                self.__con.commit() 
            self.__cur.execute("INSERT INTO SENSORS VALUES ('0', CURRENT_TIMESTAMP, ?)", (lectura,))
            self.__con.commit()        
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def setLecturaSen(self, lectura):
        try:
            self.__cur.execute("SELECT COUNT(*) FROM SENSORS")
            quant = self.__cur.fetchone()
            if (quant[0] >= self.__max):
                self.__cur.execute("DELETE FROM SENSORS WHERE ROWID = (SELECT ROWID FROM SENSORS WHERE SENSOR = '1' ORDER BY DATA ASC LIMIT 1)")
                self.__con.commit()  
            self.__cur.execute("INSERT INTO SENSORS VALUES ('1', CURRENT_TIMESTAMP, ?)", (lectura,))
            self.__con.commit()        
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def setUser(self, name, passw):
        try:
            self.__cur.execute("INSERT INTO USERS VALUES (?, ?)", (name, passw))
            self.__con.commit()        
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def getUser(self, name, passw):
        try:
            self.__cur.execute("SELECT NOM FROM USERS WHERE NOM = ? AND PASSW = ?", (name, passw))
            lectura = self.__cur.fetchone()
            return True if lectura else False    
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

    def exportUsu(self):
        f=open("ExportDataU.txt","w")
        try:
            listt=self.__cur.execute('SELECT * FROM USERS')
            for row in listt:
                f.write(str(row)+"\n")
            f.close()
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])
