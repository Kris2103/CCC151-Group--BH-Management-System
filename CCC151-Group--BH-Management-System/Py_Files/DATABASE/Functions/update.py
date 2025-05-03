import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector


class update:
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (update, cls).__new__(cls)
            
            return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = DatabaseConnector.get_connection()
            self.resultSetPointer = self.connection.cursor()
            self.initialized = True
        
    def updateTableData(self, table, setParameters: dict, whereColumn: str, whereValue):
        setClause = ", ".join([f"{key} = %s" for key in setParameters.keys()])
        QUERY = f"UPDATE {table} SET {setClause} WHERE {whereColumn} = %s"
        values = list(setParameters.values()) + [whereValue]
        
        print("SQL Query:", QUERY)
        print("Values:", values)
        
        try:
            self.resultSetPointer.execute(QUERY, values)
            self.connection.commit()
            affected_rows = self.resultSetPointer.rowcount
            
            if affected_rows > 0:
                print(f"Table '{table}' updated successfully.")
            else:
                print(f"No rows were updated for table '{table}'.")
                self.connection.rollback()
            
        except Exception as exception:
            print(f"Error updating table '{table}' : {exception}")
            self.connection.rollback()


# 2. comment everything below (only uncomment if testing, also uncomment 1.)

# if __name__ == "__main__":
#     updater = update()
    
#     table = "Tenant"
#     setParameters = {"MiddleName" : "NEW MIDDLE NAME"} #originally Lee
#     whereColumn = "TenantID"
#     whereValue = "2025-4321"

    # table = "Rents"
    # setParameters = {
    #     "MoveInDate": "2025-01-15",
    #     "MoveOutDate": "2026-01-15",
    #     "RentedRoom": "301",
    #     "MoveStatus": "Moved Out"
    # }
    # whereColumn = "RentingTenant"
    # whereValue = "2025-4322"
    
    # updater.updateTableData(table, setParameters, whereColumn, whereValue)