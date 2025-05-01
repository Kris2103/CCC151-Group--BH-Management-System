import mysql.connector
<<<<<<< HEAD

=======
from mysql.connector import Error
import configparser
import os

class DatabaseConnector:
    _connection = None

#CREATE privateCredentials FOLDER under DATABASE
    #CREATE credentials.properties FILE under privateCredentials

    @staticmethod
    def get_connection():

        if (DatabaseConnector._connection is None
            or not DatabaseConnector._connection.is_connected() #reconnect check
            ):

            config = configparser.ConfigParser()

            # Ensure the path is relative to the script file, not the working directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            properties_path = os.path.join(script_dir, "privateCredentials", "credentials.properties")

            if os.path.exists(properties_path):
                config.read(properties_path)

                try:
                    # Read individual properties
                    host = config.get("DEFAULT", "db.host")
                    port = config.getint("DEFAULT", "db.port")
                    user = config.get("DEFAULT", "db.user")
                    password = config.get("DEFAULT", "db.password")
                    database = config.get("DEFAULT", "db.database")

                    print(f"Connecting to primary DB: {host}:{port} with user {user} and database {database}")

                    # Connect
                    DatabaseConnector._connection = mysql.connector.connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        database=database
                    )

                    if DatabaseConnector._connection.is_connected():
                        print("Connected to primary MySQL.")
                    else:
                        print("Primary connection returned, but not connected.")

                except Error as e:
                    print(f"Primary SQL Error: {e}")
                    
                    try:
                        # Secondary (fallback - individual localhost version) DB credentials
                        fallback_host = config.get("FALLBACK", "db.host")
                        fallback_port = config.getint("FALLBACK", "db.port")
                        fallback_user = config.get("FALLBACK", "db.user")
                        fallback_password = config.get("FALLBACK", "db.password")
                        fallback_database = config.get("FALLBACK", "db.database")

                        print(f"Connecting to fallback DB: {fallback_host}:{fallback_port} with user {fallback_user} and database {fallback_database}")

                        # Try connecting to the fallback database
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
                        print("Could not connect to any database.")

            else:
                print(f"Properties file not found at: {properties_path}")

        return DatabaseConnector._connection

# ✅ Call the connection when running directly
if __name__ == "__main__":
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()
>>>>>>> dd22bb28b60a82b20a30c79905d568268d294b52
