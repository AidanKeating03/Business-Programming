from dbConfig import create_conn

import tkinter as tk
import customtkinter as ctk

# Open db connection

conn = create_conn()
cursor = conn.cursor()

# Build out the basics of our application window
# These are currently blue, dark blue, and green
# Modes are system, light, and dark

ctk.set_default_color_theme("blue")

ctk.set_appearance_mode("dark")

# CTK is inherited from customtkinter

window = ctk.CTk()
window.geometry("850x350")
window.title("My first UI")
# window.iconitmap("Jupyter/uccs.ico")
# window.wm_iconitmap("Jupyter/uccs.ico")

# Create button to display all the students table records

def display_records():
    cursor.execute("select * from students;")
    records = cursor.fetchall()
    msg = ""
    for record in records:
        msg += f"ID: {record[0]}, Name: {record[2]} {record[1]}, Email: {record[3]}\n"

    # Clears any data that is in the text box

    text_widget.delete('1.0', tk.END)

    # Insert new text box

    text_widget.insert(tk.END,msg)

# Dispaly the button that will use the function above

display_button = ctk.CTkButton(master = window, text = "Display Records", command = display_records)
display_button.grid(
    row = 0,
    rowspan = 1,
    column = 7,
    padx = 5,
    pady = 5,
    sticky = "e"
)

# Create a widget to display the records in

text_widget = ctk.CTkTextbox(master = window, width = 450)
text_widget.grid(
    row = 1,
    rowspan = 5,
    column = 5,
    columnspan = 3,
    padx = 5,
    ipady = 5,
    pady = 5,
    stick = "e"
)

# Create an empty widget to move stuff around

placeholder_label = ctk.CTkLabel(master = window, text = "")
placeholder_label.grid( row = 0, column = 2, columnspan = 3, ipadx =40, ipady = 5, sticky = "e")

# Create form elements to enter records in our db

# Create a label for StudentID

studentID_label = ctk.CTkLabel(master = window, text = "Student ID:")
studentID_label.grid(row = 0, column = 0, ipadx = 1, padx = 25, ipady = 2, pady = 2, sticky = "w")
studentID_input = ctk.CTkEntry(master = window)
studentID_input.grid(row = 0, column = 1, ipadx = 5, padx = 2, sticky = "w")

# Create a label for First Name

firstName_label = ctk.CTkLabel(master = window, text = "First Name:")
firstName_label.grid(row = 1, column = 0, ipadx = 1, padx = 25, ipady = 2, pady = 2, sticky = "w")
firstName_input = ctk.CTkEntry(master = window)
firstName_input.grid(row = 1, column = 1, ipadx = 5, padx = 2, sticky = "w")

# Create a label for Last Name

lastName_label = ctk.CTkLabel(master = window, text = "Last Name:")
lastName_label.grid(row = 2, column = 0, ipadx = 1, padx = 25, ipady = 2, pady = 2, sticky = "w")
lastName_input = ctk.CTkEntry(master = window)
lastName_input.grid(row = 2, column = 1, ipadx = 5, padx = 2, sticky = "w")

# Create a label for Email

email_label = ctk.CTkLabel(master = window, text = "Email:")
email_label.grid(row = 3, column = 0, ipadx = 1, padx = 25, ipady = 2, pady = 2, sticky = "w")
email_input = ctk.CTkEntry(master = window)
email_input.grid(row = 3, column = 1, ipadx = 5, padx = 2, sticky = "w")

# Add a function and button to insert records into the db

def insert_records():
    fistName = firstName_input.get()
    lastName = lastName_input.get()
    email = email_input.get()
    sql = "instert into students (firstName, lastName, email) values (%s, %s, %s)"
    val = (fistName, lastName, email)
    cursor.execute(sql, (val))
    conn.commit()
    clear_inputs()

# Function to clear the input fields

def clear_inputs():
    firstName_input.delete(0,tk.END)
    lastName_input.delete(0,tk.END)
    email_input.delete(0,tk.END)
    studentID_input.delete(0,tk.END)

# Add a button for inserting records

insert_button = ctk.CTkButton(master = window, text = "Insert", command = insert_records)
insert_button.grid(row = 5, column = 0, padx = 10, pady = 10)

#-------------------------------------SEARCH FOR RECORDS---------------------------------------

#create a function to search for records

def search_records():
    studentID_var = studentID_input.get()
    sql = "select * from students where studentID = %s"
    val = (studentID_var,)
    cursor.execute(sql,val)
    record = cursor.fetchone()
    if record:
        lastName_input.delete(0, tk.END)
        firstName_input.delete(0, tk.END)
        email_input.delete(0, tk.END)
        lastName_input.insert(0,record[1])
        firstName_input.insert(0,record[2])
        email_input.insert(0,record[3])

# Create a button that will search for records

search_button = ctk.CTkButton(master = window, text = "Search", command = search_records)
search_button.grid(row = 4, column = 0, padx= 10, pady = 10)

#-------------------------------------UPDATE RECORDS---------------------------------------

def update_records():
    studentID_var = studentID_input.get()
    firstName_var = firstName_input.get()
    lastName_var = lastName_input.get()
    email_var = email_input.get()
    sql = "update students set firstName = %s, lastName = %s, email = %s where studentID = %s"
    val = (firstName_var, lastName_var, email_var, studentID_var)
    cursor.execute(sql, val)
    conn.commit()
    clear_inputs()

# Add button to the UI to update records

update_button = ctk.CTkButton(master = window, text = "Update", command = update_records)
update_button.grid(row = 4, column = 1, padx = 10, pady = 10)

#------------------------------------------DELETE RECORDS-------------------------------------

def delete_records():
    studentID_var = studentID_input.get()
    sql = "delete from students where studentID = %s"
    val = (studentID_var,)
    cursor.execute(sql, val)
    conn.commit()
    clear_inputs()

# Creates button to delete records

delete_button = ctk.CTkButton(master = window, fg_color = 'red', text = "Delete", command = delete_records)
delete_button.grid(row = 5, column = 1, padx = 10, pady = 10)


window.mainloop()
