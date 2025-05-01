from DATABASE.DB import DatabaseConnector
import mysql.connector
from .Function import Function

class Insert(Function):
    
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



        


