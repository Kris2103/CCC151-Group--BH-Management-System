import sys
import os

# Add the root directory (where DATABASE is located) to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # 1. comment this line if it errors, only uncomment if you run it directly (testing, like running 2.)

from DATABASE.DB import DatabaseConnector
from .Function import Function 
# from Function import Function # uncomment for debugging

"""

READ ME FOR THE FUNCTION
SelectQuery has 5 Arguments

A. table
- String
- Accepts valid table name from schema
  - Tenant, Room, Rents, Pays, EmergencyContact
- DONT FORGET TO ENCLOSE IN "table"

B. select_type
- String
- corresponds to additional conditions according to type 
- "Tenant" = additional left join for emergency contact phone number
- None = loads data normallly with no additional changes to sleect query
- "Rents/Pays" = additional left join for tenant phone number

C. spec_col
- List
- accepts valid specific columns from a table
- could be multiple, could just be one
- used for filling combobox and other functionalities
- "EmergencyContact.PhoneNumber"

D. tag
- String
- accepts a valid column name of the passed table
- used for searching along specified column
- if none are passed, key will be used on ALL columns of the passed table

E. key
- String
- used as "%key%"
- used for searching, this is the search key

"""

class Select(Function):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (Select, cls).__new__(cls)
            
        return cls._instance

    def __init__(self):
        super().__init__()

    def SelectQuery(self, table, select_type=None, spec_col = [], tag = None, key = None, group = None, limit = None):
        
        self.params.clear()

        self.basequery          = f"SELECT "
        self.table              = f" FROM {table} "
        self.search_query       = ""
        self.conditions         = ""
        self.limitquery         = (f" LIMIT {limit}") if limit else ("")
        self.groupquery         = (f" GROUP BY {group}") if group else ("")

        self.columns            = self.get_columns(table)
        self.aliascolumn        = {}
        
        if not spec_col:
            self.columnquery    = ", ".join([f"{table}.{col}" for col in self.columns])
        
        else:
            self.columnquery    = ", ".join([f"{col}" for col in spec_col])
            self.columns = [col.split(" AS ")[-1].split(".")[-1] for col in spec_col]

        self.Conditions(select_type)

        # Selecting with a tag(column) and key(search key)
        if tag and key:
            search_tag = self.aliascolumn.get(tag, f"{table}.{tag}")
            self.search_query = f"WHERE {search_tag} LIKE %s "
            if key == "Male":
                self.params.append(f"{key}")
            else:
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

        self.query = self.basequery + self.columnquery + self.table + self.conditions + self.search_query + self.groupquery + self.limitquery

        print(self.query)
   

        try:
            self.cursor.execute(self.query, self.params)
            self.rows = self.cursor.fetchall()
            
            return self
        except Exception as exception:
            print(f"Error selecting table '{table}' : {exception}")
            self.conn.rollback()

    
    def retData(self):
        return self.rows
    
    def retCols(self):
        return self.columns
    
    def retAll(self):
        # for row in self.rows: print(row)
        # for col in self.columns: print(col)
        return self.rows, self.columns
    
    def retDict(self):
        print(list(zip(self.columns, self.rows[0])))

        return [dict(zip(self.columns, row)) for row in self.rows]
    
    def Conditions(self, select_type = None):
        match select_type:
            case "Tenant":
                self.columnquery        += ", EmergencyContact.PhoneNumber AS EmergencyContact"
                self.conditions         += "LEFT JOIN EmergencyContact ON Tenant.TenantID = EmergencyContact.EMTenantID "
                self.aliascolumn["EmergencyContact"] = "EmergencyContact.PhoneNumber"
                self.columns.append("EmergencyContact")
            case "Rents":
                self.columnquery        += ", TIMESTAMPDIFF(MONTH, MoveInDate, MoveOutDate) AS `Rent Duration in Months`"
                self.aliascolumn["`Rent Duration in Months`"] = "TIMESTAMPDIFF(MONTH, MoveInDate, MoveOutDate)"
                self.columns.append("Rent Duration in Months")
            case "Pays":
                pass
            case None:
                pass

# if __name__ == "__main__":
#     selector = Select()
        
#     selector.SelectQuery(table="Rents")
#     resultBuilder = selector.retDict()
#     print(f"Query Result: {resultBuilder}")

# uncomment for debugging