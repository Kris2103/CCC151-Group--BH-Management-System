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


Return functions:

A. retData = rows
B. retCol = columns
C. retAll = rows, columns
D. retDict = {columns : rows}


"""

class Select(Function):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super (Select, cls).__new__(cls)
            
        return cls._instance

    def __init__(self):
        super().__init__()

    def SelectQuery(self,   table,          select_type = None, spec_col    = [],   tag = [], key = [], filters = {}, 
                            group = None,   limit       = None, sort_column = None, sort_order = None):
        
        self.params.clear()
        # , CTEs = []
        # self.CTE                = ("WITH " + ", ".join(CTEs)) if CTEs else ""
        self.basequery          = f"SELECT DISTINCT "
        self.table              = f" FROM {table} "
        self.conditions         = ""
        self.limitquery         = (f" LIMIT {limit}") if limit else ""
        self.groupquery         = (f" GROUP BY {group}") if group else ""
        self.sortquery          = (f" ORDER BY {sort_column} {sort_order}") if sort_column and sort_order else ("")

        self.columns            = self.get_columns(table)
        self.aliascolumn        = {} 

        if not spec_col: 
            self.columnquery    = ", ".join([f"{table}.{col}" for col in self.columns])
        
        self.Conditions(select_type) # Special joins, CTEs, Aliases

        if spec_col:
            self.columnquery    = ", ".join([f"{col}" for col in spec_col])
            self.columns = [col.split(" AS ")[-1].split(".")[-1] for col in spec_col]
               
        self.search_query = self.SearchQuery(table, tag, key, filters) # In case of search call, execute search

        self.query = self.basequery + self.columnquery + self.table + self.conditions + self.search_query + self.groupquery + self.sortquery + self.limitquery

        print(self.query)
        self.execute(self.query, self.params)

        return self
    
    def SearchQuery(self, table, tag, key, filters):
        search_query = ""
        filters_conditions = []

        # Selecting with a tag(column) and key(search key)
        if tag and key:
            search_tag = self.aliascolumn.get(tag, f"{table}.{tag}")
            filters_conditions.append(f"{search_tag} LIKE %s")
            self.params.append(f"%{key}%" if key != "Male" else key)

        # Selecting all columns with key(search key)
        elif key:
            searchAll = [(f"`{col}` LIKE %s") for col in self.columns]
            self.params.extend([f"%{key}%"] * len(self.columns))
            search_query = "WHERE " + " OR ".join(searchAll)

        # Selecting via dictionary, multiple tag-key pairs
        if filters:
            for ind_tag, ind_key in filters.items():
                filter_tag = self.aliascolumn.get(ind_tag, f"{table}.{ind_tag}")
                filters_conditions.append(f"{filter_tag} LIKE %s")
                self.params.append(ind_key)

        if filters_conditions:
            if search_query:
                search_query += " AND " + " AND ".join(filters_conditions)
            else:
                search_query = "WHERE " + " AND ".join(filters_conditions)

        return search_query
        # Example: 
        """

        SELECT * FROM Tenant 
        WHERE   TenantID    LIKE %2000-0001%
        OR      Email       LIKE %2000-0001%
        ...

        """

    def execute(self, query, params = None):
        try:
            self.cursor.execute(query, params)
            self.rows = self.cursor.fetchall()
            return self
        except Exception as exception:
            print(f"Error selecting : {exception}")
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
                # CTEs = [CTE_RentDuration, CTE_PaidAmount, CTE_RemainingDue]
                # self.basequery = "WITH " + ", ".join(CTEs) + self.basequery
                # self.columnquery        +=  """, RentDuration.Duration AS `Rent Duration in Months`, RentDuration.MoveStatus AS `Move Status`"""
                # self.aliascolumn[           "`Rent Duration in Months`"]    = "RentDuration.Duration"
                # self.columns.append(        "Rent Duration in Months")
                # self.aliascolumn[           "`Move Status`"]    = "MoveStatus.MoveStatus"
                # self.columns.append(        "Move Status")

                # self.conditions +=          """ 
                #                                 LEFT JOIN RentDuration 
                #                                     ON RentDuration.TenantID = Tenant.TenantID
                #                                 LEFT JOIN PaidAmount 
                #                                     ON RentDuration.TenantID = Tenant.TenantID
                #                             """
                pass
            case "Rents":
                CTEs = [CTE_RentDuration]
                self.basequery = "WITH " + ", ".join(CTEs) + self.basequery
                self.columnquery        +=  """, RentDuration.Duration AS `Rent Duration in Months`, RentDuration.MoveStatus AS `Move Status`"""
                self.aliascolumn[           "`Rent Duration in Months`"]    = "RentDuration.Duration"
                self.columns.append(        "Rent Duration in Months")
                self.aliascolumn[           "`Move Status`"]    = "MoveStatus.MoveStatus"
                self.columns.append(        "Move Status")

                self.conditions +=          """ LEFT JOIN Tenant
                                                    ON Tenant.TenantID = Rents.RentingTenant
                                                LEFT JOIN RentDuration 
                                                    ON RentDuration.TenantID = Tenant.TenantID
                                            """
            case "Pays":
                CTEs = [CTE_RentDuration, CTE_PaidAmount, CTE_RemainingDue]
                self.basequery = "WITH " + ", ".join(CTEs) + self.basequery
                self.columnquery +=         """, RemainingDue.RemainingDue AS RemainingDue """                
                self.aliascolumn[           "RemainingDue"]                 = "RemainingDue.RemainingDue"
                self.columns.append(        "RemainingDue")

                self.conditions +=          """ LEFT JOIN RemainingDue 
                                                    ON RemainingDue.TenantID = Pays.PayingTenant
                                                LEFT JOIN RentDuration 
                                                    ON RentDuration.TenantID = Pays.PayingTenant, Tenant.TenantID
                                                LEFT JOIN PaidAmount
                                                    ON PaidAmount.TenantID = Pays.PayingTenant, Tenant.TenantID
                                            """ 
            case "Room":
                pass


CTE_RentDuration    = """ RentDuration AS (
                            SELECT 
                                t.TenantID AS TenantID, 
                                r.MoveInDate AS MoveInDate,
                                r.MoveOutDate AS MoveOutDate,
                                r.RentedRoom AS RoomNumber,
                                TIMESTAMPDIFF(MONTH, r.MoveInDate, r.MoveOutDate) AS Duration,
                                CASE
                                    WHEN (CURRENT_DATE() BETWEEN r.MoveInDate AND r.MoveOutDate) AND t.RoomNumber = r.RentedRoom THEN "Active"
                                    ELSE "Moved Out"
                                END AS MoveStatus
                            FROM Rents r
                            LEFT JOIN Tenant t ON t.TenantID = r.RentingTenant
                            ) """

CTE_PaidAmount      = """ PaidAmount AS (
                            SELECT 
                                p.PayingTenant AS TenantID, 
                                SUM(p.PaymentAmount) AS PaidAmount
                            FROM Pays p
                            LEFT JOIN Rents r ON r.RentingTenant = p.PayingTenant
                                            AND p.PaymentDate BETWEEN r.MoveInDate AND r.MoveOutDate
                            GROUP BY p.PayingTenant
                            ) """

CTE_RemainingDue    = """ RemainingDue AS (
                            SELECT 
                                rd.TenantID AS TenantID,
                                ((COALESCE(r.Price, 0) * COALESCE(rd.Duration, 0)) - COALESCE(pa.PaidAmount, 0)) AS RemainingDue
                            FROM RentDuration rd
                            LEFT JOIN PaidAmount pa ON rd.TenantID = pa.TenantID
                            LEFT JOIN Room r ON r.RoomNumber = rd.RoomNumber
                            ) """

CTE_PaymentStatus   = """ PaymentStatus AS (
                            SELECT 
                                t.TenantID AS TenantID,
                                CASE
                                    WHEN pa.PaidAmount IS NULL THEN "Pending"
                                    WHEN COALESCE(pa.PaidAmount, 0) < COALESCE(red.RemainingDue, 0) AND CURRENT_DATE() > rd.MoveOutDate THEN "Overdue"
                                    WHEN COALESCE(pa.PaidAmount, 0) >= COALESCE(red.RemainingDue, 0) THEN "Paid"
                                    ELSE "Pending"
                                END AS PaymentStatus,
                                COALESCE(red.RemainingDue, 0) / COALESCE(rd.Duration, 0) AS UnpaidMonths
                            FROM Tenant t
                            LEFT JOIN RentDuration rd ON t.TenantID = rd.TenantID
                            LEFT JOIN RemainingDue red ON t.TenantID = red.TenantID
                            LEFT JOIN PaidAmount pa ON t.TenantID = pa.TenantID
                            ) """

# if __name__ == "__main__":
#     selector = Select()
        
#     selector.SelectQuery(table="Rents")
#     resultBuilder = selector.retDict()
#     print(f"Query Result: {resultBuilder}")

