import sqlite3
from pprint import pprint

DB_NAME = "db.sqlite"

class SQLiteDB:

    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS climat (
            id INTEGER PRIMARY KEY,
            time DATETIME,
            green FLOAT,
            temperature FLOAT,
            light FLOAT,
            CO2 FLOAT
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def get_last_record(self):
        query = """
            SELECT time, light, CO2, temperature
            FROM climat
            ORDER BY id DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def add_new_dataframe(self, temperature, light, CO2, green):
        query = "INSERT INTO climat (time, green, temperature, light, CO2) VALUES (datetime('now', 'localtime'), ?, ?, ?, ?);"
        self.cursor.execute(query, (green, temperature, light, CO2))
        self.connection.commit()

    def get_last_hour(self):
        query = "SELECT * FROM climat WHERE time > datetime('now', '+2 hour');"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all(self):
        query = "SELECT * FROM climat;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

