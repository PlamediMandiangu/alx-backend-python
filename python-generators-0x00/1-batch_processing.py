import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to yield batches of users from the database"""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="ALX_prodev"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:  # yield remaining records
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Process and yield users over 25 from each batch"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:
                print(user)  # or use: yield user
