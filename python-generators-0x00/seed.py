import mysql.connector
import uuid
import csv
import os

DB_NAME = "ALX_prodev"

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # Change if needed
            password="123456789"  # Replace with your actual password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Change if needed
            password="123456789",  # Replace with your actual password
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DB_NAME}: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row.get("user_id") or str(uuid.uuid4())
            name = row["name"]
            email = row["email"]
            age = row["age"]

            cursor.execute("""
            SELECT COUNT(*) FROM user_data WHERE user_id = %s
            """, (user_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))
    connection.commit()
    cursor.close()

# ✅ New: Generator function
def stream_user_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
