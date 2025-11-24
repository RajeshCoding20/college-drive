import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS admin(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(50))")
c.execute("CREATE TABLE IF NOT EXISTS customers(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), phone VARCHAR(20), email VARCHAR(50))")
c.execute("CREATE TABLE IF NOT EXISTS rooms(id INT AUTO_INCREMENT PRIMARY KEY, room_no VARCHAR(10), type VARCHAR(20), price FLOAT)")
c.execute("CREATE TABLE IF NOT EXISTS bookings(id INT AUTO_INCREMENT PRIMARY KEY, cust_id INT, room_id INT, check_in DATE, check_out DATE)")

db.commit()

def admin_login():
    print("\n=== Admin Login ===")
    u = input("Username: ")
    p = input("Password: ")
    c.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (u, p))
    if c.fetchone():
        print("Login Successfully \n")
        return True
    print("Invalid Login \n")
    return False

def add_customer():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    c.execute("INSERT INTO customers(name, phone, email) VALUES(%s, %s, %s)", (name, phone, email))
    db.commit()
    print("Customer Added \n")

def add_room():
    no = input("Room No: ")
    t = input("Type: ")
    p = input("Price: ")
    c.execute("INSERT INTO rooms(room_no, type, price) VALUES(%s, %s, %s)", (no, t, p))
    db.commit()
    print("Room Added \n")

def book_room():
    cid = input("Customer ID: ")
    rid = input("Room ID: ")
    cin = input("Check-in (YYYY-MM-DD): ")
    cout = input("Check-out (YYYY-MM-DD): ")
    c.execute("INSERT INTO bookings(cust_id, room_id, check_in, check_out) VALUES(%s, %s, %s, %s)", (cid, rid, cin, cout))
    db.commit()
    print("Room Booked \n")

def view_customers():
    print("\n----- CUSTOMER LIST -----")
    c.execute("SELECT id, name, phone, email FROM customers")
    print("ID  NAME        PHONE       EMAIL")
    for i in c.fetchall():
        print(f"{i[0]:<4}{i[1]:<12}{i[2]:<12}{i[3]}")
    print("--------------------------\n")

def view_rooms():
    print("\n----- ROOMS -----")
    c.execute("SELECT id, room_no, type, price FROM rooms")
    print("ID  ROOM NO   TYPE       PRICE")
    for i in c.fetchall():
        print(f"{i[0]:<4}{i[1]:<10}{i[2]:<10}{i[3]}")
    print("-----------------------------\n")

def view_bookings():
    print("\n----- BOOKINGS -----")
    c.execute("SELECT id, cust_id, room_id, check_in, check_out FROM bookings")
    print("ID  CUST  ROOM  CHECK-IN      CHECK-OUT")
    for i in c.fetchall():
        print(f"{i[0]:<4}{i[1]:<6}{i[2]:<6}{i[3]:<13}{i[4]}")
    print("----------------------------------------\n")

def main():
    while True:
        print("\n=== HOTEL MANAGEMENT ===")
        print("1. Add Customer")
        print("2. Add Room")
        print("3. Book Room")
        print("4. View Customers")
        print("5. View Rooms")
        print("6. View Bookings")
        print("0. Exit")

        ch = input("Enter choice: ")

        if ch == "1": add_customer()
        elif ch == "2": add_room()
        elif ch == "3": book_room()
        elif ch == "4": view_customers()
        elif ch == "5": view_rooms()
        elif ch == "6": view_bookings()
        elif ch == "0": break
        else: print("Invalid Option \n")

if admin_login():
    main()
else:
    print("Access Closed.")
