import psycopg2
from psycopg2 import sql
from psycopg2 import connect

connection = None

def main():
    # Ask user for their username and password for PostgreSQL
    username = input("PostgreSQL username: ")
    password = input("PostgreSQL password: ")

    # Make connection to postgres and create databae
    try:
        connect(username, password)
        create_and_connect_to_Students(username, password)
    except Exception as e:
        print("Errors setting up Database: ", e)
        return
    
    # Create and populate students table
    try:
        create_students_table()
    except Exception as e:
        print("Error creating students table: ", e)
        return
    
    # Loop prompt to provide user menu
    while True:
        print("\n1. Get all students")
        print("2. Add a student")
        print("3. Update student email")
        print("4. Delete a student")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                students = getAllStudents()
                print("\nAll Students:")
                for student in students:
                    print(str(student[0]) + " : " + student[1] + ", " + student[2] + ", " + student[3] + ", " + student[4].strftime("%Y-%m-%d"))
            except Exception as e:
                print("Error getting all students", e)
        elif choice == "2":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            try:
                addStudent(first_name, last_name, email, enrollment_date)
                print("Student added successfully.")
            except Exception as e:
                print("Error adding student.", e)
        elif choice == "3":
            student_id = input("Enter student ID: ")
            new_email = input("Enter new email: ")
            try:
                updateStudentEmail(student_id, new_email)
                print("Email updated successfully.")
            except Exception as e:
                print("Error updating student.", e)
        elif choice == "4":
            student_id = input("Enter student ID: ")
            try:
                deleteStudent(student_id)
                print("Student deleted successfully.")
            except Exception as e:
                print("Error deleting student.", e) 
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

# Gets all students from students table in database
def getAllStudents():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    output = cursor.fetchall()
    cursor.close()
    return output

# Adds new student with given information to database
def addStudent(first_name, last_name, email, enrollment_date):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
    cursor.close()

# Updates student with student_id and changes email to new_email
def updateStudentEmail(student_id, new_email):
    cursor = connection.cursor()
    cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
    cursor.close()

# Deletes student with student_id=student_id
def deleteStudent(student_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s",(student_id,))
    cursor.close()

# Creates connection to Postgres
def connect(username, password):
    global connection
    connection = psycopg2.connect(database="postgres", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True

# Creates and Connects to a new database titled Students
def create_and_connect_to_Students(username, password):
    global connection
    cursor = connection.cursor()

    # Creates Students Database in Postgres
    cursor.execute('DROP DATABASE IF EXISTS Students')
    cursor.execute('CREATE DATABASE Students')

    # Closes connection to Postgres
    cursor.close()
    connection.close()

    # Connects to Students Database
    connection = psycopg2.connect(database="students", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True

# Creates students table in the Students database
def create_students_table():
    cursor = connection.cursor()

    # Creates students table with fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            enrollment_date DATE
        )
    ''')

    # Populates students table with initial values
    cursor.execute('''
        INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
            ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
            ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
            ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
    ''')

    cursor.close()
 
if __name__ == "__main__":
    main()