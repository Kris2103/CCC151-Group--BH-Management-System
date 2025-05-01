import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector


class update:
    
    def __init__(self):
        self.connection = DatabaseConnector.get_connection()
        self.resultSetPointer = self.connection.cursor()
        
    def updateTableData(self, table, setParams: dict, whereColumn: str, whereValue):
        setClause = ", ".join([f"{key} = %s" for key in setParams.keys()])
        QUERY = f"UPDATE {table} SET {setClause} WHERE {whereColumn} = %s"
        values = list(setParams.values()) + [whereValue]
        
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
#     setParams = {"MiddleName" : "Lee"} #originally Lee
#     whereColumn = "TenantID"
#     whereValue = "2025-4321"
    
#     updater.updateTableData(table, setParams, whereColumn, whereValue)