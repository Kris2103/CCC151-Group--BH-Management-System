import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector
# import mysql.connector

class Function:
    
    def __init__(self):
        self.conn = DatabaseConnector.getConnection()
        self.cursor = self.conn.cursor()
        self.params = []

    def get_columns(self, table):
        query = """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """
        db_name = self.conn.database
        self.cursor.execute(query, (db_name, table))
        return [row[0] for row in self.cursor.fetchall()]
    
# if __name__ == "__main__":
#     func = Function()
#     for col in func.get_columns("Tenant"):
#         print(col)