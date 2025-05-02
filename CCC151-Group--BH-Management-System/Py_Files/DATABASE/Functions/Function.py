from DATABASE.DB import DatabaseConnector
import mysql.connector

class Function:
    
    def __init__(self):
        self.conn = DatabaseConnector.get_connection()
        self.cursor = self.conn.cursor()
        self.params = []

    def get_columns(self, table):
        query = """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        """
        db_name = self.conn.database
        self.cursor.execute(query, (db_name, table))
        return [row[0] for row in self.cursor.fetchall()]
    
