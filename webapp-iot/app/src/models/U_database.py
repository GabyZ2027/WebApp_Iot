import sqlite3
import sys
import bcrypt
class Usuaris_BD():

    def __init__(self, nom):

        try:
            self.__con = sqlite3.connect(nom)
            self.__cur = self.__con.cursor()  
            self.__cur.executescript("""
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

    def getUser(self, name):
        try:
            self.__cur.execute("SELECT NOM FROM USERS WHERE NOM = ?", (name,))
            lectura = self.__cur.fetchone()
            return True if lectura else False    
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def register(self, name, passw):
        try:
            if self.getUser(name) == False:
                epassw = passw.encode()
                hash=bcrypt.hashpw(epassw, bcrypt.gensalt())
                self.__cur.execute("INSERT INTO USERS VALUES (?, ?)", (name, hash))
                self.__con.commit()
                return True   #L'usuari ha sigut registrat
            else:
                return False  #L'usuari ja existeix
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def login(self, name, passw):
        try:
            if self.getUser(name) == True:
                self.__cur.execute("SELECT PASSW FROM USERS WHERE NOM = ?", (name,))
                lectura = self.__cur.fetchone()
                hash = lectura[0]
                epassw = passw.encode()
                if bcrypt.checkpw(epassw,hash):
                    return True     #S'ha verificat
                else:
                    return False    #Passwd incorrecte
            else:  
                return None         #No existeix l'usuari
        except sqlite3.Error as e:
            self.__con.rollback()
            print("Error %s:" % e.args[0])

    def sortir(self):
        self.__con.close()

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
