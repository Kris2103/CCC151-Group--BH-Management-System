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
        super.__init__(self)

    def InsertQuery(self, table, attr):
        
        for i in attr: self.params.append(i)
        columns = self.get_columns(table)
        
        query = (
            
            f"INSERT INTO {table} ("    + 
            ", ".join(columns)          + 
            ") VALUES ("                +
            ", ".join(self.params)      +
            ")"
        )
        
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



        


