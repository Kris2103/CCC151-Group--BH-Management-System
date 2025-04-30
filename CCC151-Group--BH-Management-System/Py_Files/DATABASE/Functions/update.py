import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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
            print(f"Table '{table}' updated successfully.")
            
        except Exception as exception:
            print(f"Error updating table '{table}' : {exception}")

if __name__ == "__main__":
    updater = update()
    table = "Tenant"
    setParams = {"MiddleName" : "UPDATED MIDDLE NAME"}
    whereColumn = "TenantID"
    whereValue = "2025-4321"
    
    updater.updateTableData(table, setParams, whereColumn, whereValue)