from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

def admin_login():
    print("=== Admin Login ===")
    username = input("Username: ")
    password = input("Password: ")
    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    if cursor.fetchone():
        print("Login Successful!\n")
        return True
    print("Invalid Credentials!\n")
    return False

def add_student():
    print("=== Add Student ===")
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender (Male/Female/Other): ")
    email = input("Email: ")
    course = input("Course: ")
    cursor.execute(
        "INSERT INTO students (name, age, gender, email, course) VALUES (%s,%s,%s,%s,%s)",
        (name, age, gender, email, course)
    )
    db.commit()
    print("Student Added Successfully!\n")

def view_students():
    print("=== All Students ===")
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    if students:
        for student in students:
            print(f"ID: {student[0]} | Name: {student[1]} | Age: {student[2]} | Gender: {student[3]} | Email: {student[4]} | Course: {student[5]}")
    else:
        print("No students found!")

def update_student():
    student_id = int(input("Enter Student ID to update: "))
    cursor.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    if not student:
        print("Student not found!")
        return
    print("Leave blank to keep current value.")
    name = input(f"Name [{student[1]}]: ") or student[1]
    age = input(f"Age [{student[2]}]: ") or student[2]
    gender = input(f"Gender [{student[3]}]: ") or student[3]
    email = input(f"Email [{student[4]}]: ") or student[4]
    course = input(f"Course [{student[5]}]: ") or student[5]
    cursor.execute(
        "UPDATE students SET name=%s, age=%s, gender=%s, email=%s, course=%s WHERE student_id=%s",
        (name, age, gender, email, course, student_id)
    )
    db.commit()
    print("Student Updated Successfully!\n")

def delete_student():
    student_id = int(input("Enter Student ID to delete: "))
    cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    db.commit()
    print("Student Deleted Successfully!\n")

def main_menu():
    while True:
        print("\n=== Smart Campus Management ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice!")

if admin_login():
    main_menu()
