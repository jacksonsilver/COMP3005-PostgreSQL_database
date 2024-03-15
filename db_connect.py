import psycopg2
from psycopg2 import connect

connection = None

def main():
    # Ask user for their username and password for PostgreSQL
    username = input("PostgreSQL username: ")
    password = input("PostgreSQL password: ")

    # Connect to students database
    try:
        connectToStudents(username, password)
    except Exception as e:
        print("Error connecting to Students database: ", e)
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

# Creates and Connects to a new database titled Students
def connectToStudents(username, password):
    global connection
    connection = psycopg2.connect(database="students", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True
 
if __name__ == "__main__":
    main()