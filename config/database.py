# mysql handling
import mysql.connector
from mysql.connector import Error
from mysql.connector.errors import IntegrityError

# this is to load de user data stored in the file ".env"
import os
from dotenv import load_dotenv
load_dotenv()

class Database:
    # contructor, to open the connection to the DB
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.connection.cursor()

    # private method to excude queries            
    def _execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except IntegrityError as e:
            raise Exception(f"Error de integridad: {e.msg}")
        except Error as e:
            raise Exception(f"Error al ejecutar la consulta: {e.msg}")

    # public method to excute the queries
    def execute_query(self, query, params=None):
        self._execute(query, params)
        self.connection.commit()

    # public method to select row    
    def execute_select(self, query, params=None):
        self._execute(query, params)
        return self.cursor.fetchall()

    # public method to selece 1
    def fetchone(self, query, params=None):
        self._execute(query, params)
        return self.cursor.fetchone()

    # public method to close the cursor, and the connection
    def close(self):
        self.cursor.close()
        self.connection.close()
