from dbConfig import create_conn

# Create a function for adding records
def add_student(last_name, first_name, email):
    conn = create_conn()
    cursor = conn.cursor()

    insert_query = "insert into students (lastName, firstName, email) values (%s, %s, %s)"
    record = (last_name, first_name, email)

    cursor.execute(insert_query, record)
    conn.commit()

    print("Student record added successfully!")
    cursor.close()
    conn.close()

    # Add the record
if __name__ == "__main__":
    last_name = "Jingleheimer"
    first_name = "JJ"
    email = "jj@email.com"

    add_student(last_name, first_name, email)