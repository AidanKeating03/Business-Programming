from dbConfig import create_conn

# Create a function for fetching all student records
def get_all_students():
    conn = create_conn()
    cursor = conn.cursor()

    select_query = "select * from students;"
    cursor.execute(select_query)

    results = cursor.fetchall()
    print("All records from students: ")
    for row in results:
        print(row)

    cursor.close()
    conn.close()

# Fetch all records
if __name__ == "__main__":
    get_all_students()