import seed

def stream_user_ages():
    """Generator that yields one user age at a time."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row["age"]
    connection.close()

def compute_average_age():
    """Compute the average age using the generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No user data found.")

# Run the computation when this script is executed
if __name__ == "__main__":
    compute_average_age()
