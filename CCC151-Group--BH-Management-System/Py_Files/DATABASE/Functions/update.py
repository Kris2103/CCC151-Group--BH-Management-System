import sys
import os
import threading

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector


class update:
    
    _instance = None
    _lock = threading.Lock()
    _threadLocal = threading.local()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super (update, cls).__new__(cls)
                
        return cls._instance
    
    def __init__(self):
        if not hasattr(self._threadLocal, 'initialized'):
            self._threadLocal.connection = DatabaseConnector.getConnection()
            self._threadLocal.initialized = True
        
    def updateTableData(self, table, setParameters: dict, whereColumn: str, whereValue):
        setClause = ", ".join([f"{key} = %s" for key in setParameters.keys()])
        
        values = list(setParameters.values())
        
        if isinstance(whereValue, (list, tuple, set)):  # multiple values
            placeholders = ", ".join(["%s"] * len(whereValue))
            QUERY = f"UPDATE {table} SET {setClause} WHERE {whereColumn} IN ({placeholders})"
            values += list(whereValue)
        else:  # single value
            QUERY = f"UPDATE {table} SET {setClause} WHERE {whereColumn} = %s"
            values.append(whereValue)

        print("SQL Query:", QUERY)
        print("Values:", values)

        try:
            resultSetPointer = self._threadLocal.connection.cursor()
            resultSetPointer.execute(QUERY, values)
            self._threadLocal.connection.commit()
            affectedRows = resultSetPointer.rowcount

            if affectedRows > 0:
                print(f"{affectedRows} row(s) updated successfully in table '{table}'.")
            else:
                print(f"No rows were updated for table '{table}'.")
                self._threadLocal.connection.rollback()

        except Exception as exception:
            print(f"Error updating table '{table}' : {exception}")
            self._threadLocal.connection.rollback()

        finally:
            resultSetPointer.close()

                        
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
    
#     updater.updateTableData(
#     table="Tenant",
#     setParameters={"MiddleName": "UPDATED NAME"},
#     whereColumn="TenantID",
#     whereValue=["2025-4321", "2025-1234", "2025-5678"]
# )
