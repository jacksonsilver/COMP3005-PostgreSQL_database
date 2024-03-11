import psycopg2
from psycopg2 import sql
from psycopg2 import connect

def main():
    # Ask user for their username and password for PostgreSQL
    username = input("PostgreSQL username: ")
    password = input("PostgreSQL password: ")

    try:
        connection = connect(username, password)
        connection = create_and_connect_to_Students(connection, username, password)
    except Exception as e:
        print("Errors setting up Database: ", e)
        return
    
    create_students_table(connection)

# Creates connection to Postgres
def connect(username, password):
    connection = psycopg2.connect(database="postgres", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True
    return connection

# Creates and Connects to a new database titled Students
def create_and_connect_to_Students(connection, username, password):
    cursor = connection.cursor()

    # Creates Students Database in Postgres
    cursor.execute('''CREATE DATABASE IF NOT EXISTS''')
    cursor.close()

    # Closes connection to Postgres
    connection.close()

    # Connects to Students Database
    connection = psycopg2.connect(database="Students", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True

    return connection

# Creates students table in the Students database
def create_students_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            enrollment_date DATE
        )
    """)
    cursor.close()



    
    
if __name__ == "__main__":
    main()