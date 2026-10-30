
import sqlite3


con = sqlite3.connect("student.db")
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

con.commit()


cur.execute("SELECT * FROM users WHERE username='admin'")

if cur.fetchone() is None:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "admin123", "admin")
    )
    con.commit()


def register():
    print("\n--- Registration ---")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Fields cannot be empty!")
        return

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, "staff")
        )
        con.commit()
        print("Registration successful!")

    except sqlite3.IntegrityError:
        print("Username already exists!")



def login():
    print("\n--- Login ---")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cur.fetchone()

    if user:
        print("\nLogin successful!")
        print("Welcome", username)
        return user

    else:
        print("Invalid username or password!")
        return None



def add_student(user_id):
    name = input("Enter student name: ").strip()
    age = input("Enter age: ").strip()
    course = input("Enter course: ").strip()

    if not name or not age or not course:
        print("All fields are required!")
        return

    try:
        age = int(age)

        if age <= 0:
            print("Enter a valid age!")
            return

        cur.execute(
            "INSERT INTO students (name, age, course, user_id) VALUES (?, ?, ?, ?)",
            (name, age, course, user_id)
        )

        con.commit()
        print("Student added successfully!")

    except ValueError:
        print("Age must be a number!")



def view_students():
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    print("\n--- Student Details ---")

    if not students:
        print("No student records found!")
        return

    for s in students:
        print("ID:", s[0], "| Name:", s[1],
              "| Age:", s[2], "| Course:", s[3])



def update_student():
    try:
        student_id = int(input("Enter student ID to update: "))

        cur.execute("SELECT * FROM students WHERE id=?", (student_id,))

        if cur.fetchone() is None:
            print("Student not found!")
            return

        name = input("Enter new name: ").strip()
        age = int(input("Enter new age: "))
        course = input("Enter new course: ").strip()

        if not name or not course or age <= 0:
            print("Invalid details!")
            return

        cur.execute(
            "UPDATE students SET name=?, age=?, course=? WHERE id=?",
            (name, age, course, student_id)
        )

        con.commit()
        print("Student updated successfully!")

    except ValueError:
        print("Please enter valid numbers!")



def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))

        cur.execute("DELETE FROM students WHERE id=?", (student_id,))
        con.commit()

        if cur.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student not found!")

    except ValueError:
        print("Invalid student ID!")



while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        register()

    elif choice == "2":
        user = login()

        if user:
            user_id = user[0]
            role = user[3]

            while True:
                print("\n===== STUDENT MENU =====")
                print("1. Add Student")
                print("2. View Students")

                if role == "admin":
                    print("3. Update Student")
                    print("4. Delete Student")

                print("0. Logout")

                option = input("Enter choice: ").strip()

                if option == "1":
                    add_student(user_id)

                elif option == "2":
                    view_students()

                elif option == "3" and role == "admin":
                    update_student()

                elif option == "4" and role == "admin":
                    delete_student()

                elif option == "0":
                    print("Logged out successfully!")
                    break

                else:
                    print("Invalid choice or permission denied!")

    elif choice == "3":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")

con.close()
