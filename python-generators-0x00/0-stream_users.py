import mysql.connector

def stream_users():
    """Generator function to yield users one by one from the database"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your MySQL password if needed
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
