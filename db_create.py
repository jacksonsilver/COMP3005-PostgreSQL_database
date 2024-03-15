import psycopg2
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
    
    connection.close()

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