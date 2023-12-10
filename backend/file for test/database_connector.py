import mysql.connector

def connect_to_database():
    try:
        # Replace with your actual database credentials
        conn = mysql.connector.connect(
            user='ghostbin3',
            password='Ahmed197524',
            host='ghostbin3.mysql.pythonanywhere-services.com',
            port=5001,
            database='ghostbin3$bakersbox'
        )

        if conn.is_connected():
            print("Connected to MySQL server")

        return conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Attempt to connect to the database
connection = connect_to_database()

# Close the connection if it was successfully established
if connection:
    connection.close()
    print("Connection closed")
