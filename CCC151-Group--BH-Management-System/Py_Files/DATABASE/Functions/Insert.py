from DATABASE.DB import DatabaseConnector
import mysql.connector
from .Function import Function

class Insert(Function):
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (Insert, cls).__new__(cls)
            
        return cls._instance

    def __init__(self):
        super().__init__()

    def InsertQuery(self, table, attr):
        
        self.params = []
        self.place = []
        for i in attr: 
            self.params.append(i)
            print(i)
        excluded = self.checkExcludables(table)
        columns = [col for col in self.get_columns(table) if col not in excluded]
        self.placeholders = ", ".join(["%s"] * len(columns))
        
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({self.placeholders})"


        print(query)
        
        # Example: 
        """

        INSERT INTO Tenant (
        TenantID, ..., RoomNumber
        ) VALUES (
        TenantID, ..., RoomNumber
        )

        """

        self.cursor.execute(query, self.params)
        return self.cursor.fetchall()
    
    # check nullable columns and thus excluded in the insertion
    def checkExcludables(self, table):
        excludables = []
        match table:
            case "Tenant":
                excludables.append("RoomNumber")
            case "Rent":
                excludables.append("RentID")
            case "Pay":
                excludables.append("PayID")
            case "Room":
                pass
            case "EmergencyContact":
                pass
            case _:
                pass

        return excludables
                 





        


