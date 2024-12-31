from dbConfig import create_conn

# Create a function to delete records
def delete_student(student_id):
    conn = create_conn()
    cursor = conn.cursor()

    delete_query = "delete from students where studentID = %s"
    cursor.execute(delete_query, (student_id,)) # The extra comma tricks Python into accepting the INT as a String.

    conn.commit()

    # Add some logic to verify that records exist
    if cursor.rowcount >0:
        print("Student record deleted successfully!")
    else:
        print("No record found with the given student ID.")
    
    cursor.close()
    conn.close()

# Record to delete
student_id = 1
delete_student(student_id)