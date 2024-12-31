from dbConfig import create_conn

# Create a function to update records
def update_student(student_id, last_name, first_name, email):
    conn = create_conn()
    cursor = conn.cursor()

    update_query = "update students set lastName = %s, firstName = %s, email = %s where studentID = %s;"

    cursor.execute(update_query, (last_name, first_name, email, student_id))
    conn.commit()

    print("Student record updated successfully!")
    cursor.close()
    conn.close()

# Update the record with the information below
student_id = 3
updated_last_name = 'Smith'
updated_first_name = 'John'
upated_email = 'js@email.com'
update_student(student_id, updated_last_name, updated_first_name, upated_email)