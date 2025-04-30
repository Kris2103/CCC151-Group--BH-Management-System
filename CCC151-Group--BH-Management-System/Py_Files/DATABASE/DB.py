import mysql.connector
from mysql.connector import Error
import configparser
import os

class DatabaseConnector:
    _connection = None

#CREATE privateCredentials FOLDER under DATABASE
    #CREATE credentials.properties FILE under privateCredentials

    @staticmethod
    def get_connection():

        if DatabaseConnector._connection is None:
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

                    print(f"Connecting to {host}:{port} with user {user} and database {database}")

                    # Connect
                    DatabaseConnector._connection = mysql.connector.connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        database=database
                    )

                    print("Connected to MySQL.")

                    if DatabaseConnector._connection.is_connected():
                        print("Connected to MySQL.")
                    else:
                        print("Connection object returned, but not connected.")

                except Error as e:
                    print(f"SQL Error: {e}")

            else:
                print(f"Properties file not found at: {properties_path}")

        return DatabaseConnector._connection

# ✅ Call the connection when running directly
if __name__ == "__main__":
    conn = DatabaseConnector.get_connection()
    cursor = conn.cursor()