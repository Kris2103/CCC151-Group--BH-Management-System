import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector
from .Function import Function

class Delete(Function):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (Delete, cls).__new__(cls)
            
        return cls._instance

    def __init__(self):
        super().__init__()

    def DeleteQuery(self, table):

        

        try:
            self.cursor.execute(self.query, self.params)
            self.rows = self.cursor.fetchall()
            
            return self
        except Exception as exception:
            print(f"Error selecting table '{table}' : {exception}")
            self.conn.rollback()
