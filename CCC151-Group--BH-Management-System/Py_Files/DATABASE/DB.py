import mysql.connector
from mysql.connector import Error, OperationalError, InterfaceError
import configparser
import os

class DatabaseConnector:
    _connection = None

    @staticmethod
    def _loadConfig():
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        properties_path = os.path.join(script_dir, "privateCredentials", "credentials.properties")

        if not os.path.exists(properties_path):
            raise FileNotFoundError(f"Properties file not found at: {properties_path}")

        config.read(properties_path)
        return config

    @staticmethod
    def _connect():
        config = DatabaseConnector._loadConfig()

        try:
            # Primary connection
            host = config.get("DEFAULT", "db.host")
            port = config.getint("DEFAULT", "db.port")
            user = config.get("DEFAULT", "db.user")
            password = config.get("DEFAULT", "db.password")
            database = config.get("DEFAULT", "db.database")

            print(f"Connecting to primary DB: {host}:{port} with user {user}")
            DatabaseConnector._connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )

            if DatabaseConnector._connection.is_connected():
                print("Connected to primary MySQL.")
                return

        except Error as e:
            print(f"Primary SQL Error: {e}")

        # Try fallback connection
        try:
            fallback_host = config.get("FALLBACK", "db.host")
            fallback_port = config.getint("FALLBACK", "db.port")
            fallback_user = config.get("FALLBACK", "db.user")
            fallback_password = config.get("FALLBACK", "db.password")
            fallback_database = config.get("FALLBACK", "db.database")

            print(f"Connecting to fallback DB: {fallback_host}:{fallback_port} with user {fallback_user}")
            DatabaseConnector._connection = mysql.connector.connect(
                host=fallback_host,
                port=fallback_port,
                user=fallback_user,
                password=fallback_password,
                database=fallback_database
            )

            if DatabaseConnector._connection.is_connected():
                print("Connected to fallback MySQL.")
            else:
                print("Fallback connection returned, but not connected.")

        except Error as fallback_error:
            print(f"Fallback SQL Error: {fallback_error}")
            DatabaseConnector._connection = None

    @staticmethod
    def getConnection():
        if (DatabaseConnector._connection is None or
                not DatabaseConnector._connection.is_connected()):
            print("Establishing or re-establishing DB connection...")
            DatabaseConnector._connect()
        return DatabaseConnector._connection

    @staticmethod
    def getCursor():
        conn = DatabaseConnector.getConnection()
        if conn and conn.is_connected():
            return conn.cursor()
        else:
            raise ConnectionError("Unable to get a MySQL cursor. No connection established.")

# Run when executed directly
if __name__ == "__main__":
    try:
        cursor = DatabaseConnector.getCursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print("Connected to database:", result[0] if result else "Unknown")
    except Exception as ex:
        print(f"Startup connection failed: {ex}")
