from DATABASE.DB import DatabaseConnector
from .Function import Function

class Select(Function):
    
    def __init__(self):
        super().__init__()

    def SelectQuery(self, table, tag = None, key = None):
        
        self.basequery = f"SELECT * FROM {table} "
        self.search_query = ""

        # Selecting with a tag(column) and key(search key)
        if tag and key:
            self.search_query = f"WHERE {tag} = %s"
            self.params.append(f"%{key}%")

        # Selecting all columns with key(search key)
        elif key:
            columns = self.get_columns(table)
            
            searchAll = [(f"`{col}` LIKE %s") for col in columns]
            self.params.extend([f"%{key}%"] * len(columns))

            self.search_query = "WHERE " + " OR ".join(searchAll)

        query = self.basequery + self.search_query 

        self.cursor.execute(query, self.params)
        return self.cursor.fetchall()



        


