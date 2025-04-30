from DATABASE.DB import DatabaseConnector
from .Function import Function

class Select(Function):
    
    def __init__(self):
        super().__init__()

    def SelectQuery(self, table, select_type, tag = None, key = None):
        
        self.basequery          = f"SELECT {table}.*" 
        self.table              = f" FROM {table} "
        self.search_query       = ""
        self.conditions         = ""

        self.columns = self.get_columns(table)

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
        WHERE   TenantID    = %2000-0001%
        OR      Email       = %2000-0001%
        ...

        """
        self.Conditions(select_type)

        self.query = self.basequery + self.table + self.search_query + self.conditions

        print(self.query)

        self.cursor.execute(self.query, self.params)
        self.rows = self.cursor.fetchall()
        
        return self.rows, self.columns
    
    def Conditions(self, select_type):
        match select_type:
            case 0:
                print("case 0")
                self.basequery          += ", EmergencyContact.PhoneNumber AS EmergencyContact"
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


        


