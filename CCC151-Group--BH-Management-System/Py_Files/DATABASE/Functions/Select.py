import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector
from .Function import Function


class Select(Function):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (Select, cls).__new__(cls)
            
            return cls._instance

    def __init__(self):
        super().__init__()

    def SelectQuery(self, table, select_type, spec_col = [], tag = None, key = None):
        
        self.basequery          = f"SELECT {table}."
        self.columnquery        = f"*" if not spec_col else (f", {table}.".join(spec_col))
        self.table              = f" FROM {table} "
        self.search_query       = ""
        self.conditions         = ""

        self.columns            = self.get_columns(table)
        self.row_id             = self.columns[0]

        # Selecting with a tag(column) and key(search key)
        if tag and key:
            self.search_query = f"WHERE {tag} = %s"
            self.params.append(f"%{key}%")

        # Selecting all columns with key(search key)
        elif key:            
            searchAll = [(f"`{col}` LIKE %s") for col in self.columns]
            self.params.extend([f"%{key}%"] * len(self.columns))

            self.search_query = "WHERE " + " OR ".join(searchAll)

        # Example: 
        """

        SELECT * FROM Tenant 
        WHERE   TenantID    LIKE %2000-0001%
        OR      Email       LIKE %2000-0001%
        ...

        """
        self.Conditions(select_type)

        self.query = self.basequery + self.columnquery + self.table + self.search_query + self.conditions 

        print(self.query)

        self.cursor.execute(self.query, self.params)
        self.rows = self.cursor.fetchall()
        
        return self
    
    def retData(self):
        return self.rows
    
    def retCols(self):
        return self.columns
    
    def retAll(self):
        return self.rows, self.columns
    
    def retDict(self):
        return [dict(zip(self.columns, row)) for row in self.rows]
    
    def Conditions(self, select_type):
        match select_type:
            case 0:
                self.columnquery        += ", EmergencyContact.PhoneNumber AS EmergencyContact"
                self.conditions         += "LEFT JOIN EmergencyContact ON Tenant.TenantID = EmergencyContact.EMTenantID"
                self.columns.append("EmergencyContact")
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case _:
                pass
