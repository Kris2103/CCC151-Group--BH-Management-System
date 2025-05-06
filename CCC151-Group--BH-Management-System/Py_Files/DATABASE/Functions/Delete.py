import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from .Function import Function

class Delete(Function):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (Delete, cls).__new__(cls)
            
        return cls._instance

    def __init__(self):
        super().__init__()

    def DeleteQuery(self, table, column, key):
        
        query = f"DELETE FROM {table} WHERE {column} = %s"
        self.params.append(key)
        
        # Example: 
        """
        f"DELETE FROM students WHERE `ID Number` = %s"

        """

        try:
            self.cursor.execute(query, self.params)
            return self.cursor.fetchall()
        
        except Exception as exception:
            print(f"Error deleting selection '{key}' from '{table}' : {exception}")
            self.conn.rollback()
