import sqlite3
import hashlib

# Use a context manager to handle the connection
with sqlite3.connect('database.db', check_same_thread=False) as connect:
    # Execute the schema script
    with open('schema.sql') as f:
        connect.executescript(f.read())

    # Get a cursor object
    cur = connect.cursor()

    # Define a function to insert a doctor
    def insert_doc(user, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cur.execute("INSERT INTO doctor (username, password) VALUES (?, ?)", (user, hashed_password))
            # Commit the changes
            connect.commit()
        except sqlite3.Error as e:
            # Handle any errors
            print(f"An error occurred: {e}")

    # Define a function to insert a patient
    def insert_pat(user, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cur.execute("INSERT INTO patient (username, password) VALUES (?, ?)", (user, hashed_password))
            connect.commit()
        except sqlite3.Error as e:
            # Handle any errors
            print(f"An error occurred: {e}")


    def doc_login(user, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cur.execute("SELECT * FROM doctor WHERE username = ? AND password = ?", (user, hashed_password))
            return cur.fetchone()
        except sqlite3.Error as e:
            # Handle any errors
            print(f"An error occurred: {e}")
            return None


    def pat_login(user, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cur.execute("SELECT * FROM patient WHERE username = ? AND password = ?", (user, hashed_password))
            return cur.fetchone()
        except sqlite3.Error as e:

            print(f"An error occurred: {e}")
            return None

    def get_patient_data(user):
        try:
            cur.execute("SELECT * FROM patient_profile WHERE username = ?", (user,))
            return cur.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None


    def store_patient_data(name, gender, dob, bloodgroup, phone, address):
        try:
            cur.execute("INSERT INTO patient_profile VALUES (?, ?, ?, ?, ?, ?)",
                        (name, gender, dob, bloodgroup, phone, address))
            connect.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


    def update_patient_data(name, gender, dob, bloodgroup, phone, address):
        try:
            cur.execute("UPDATE patient_profile SET gender = ?, dob = ?, bloodgroup = ?, phone = ?, address = ? WHERE name = ?",
                (gender, dob, bloodgroup, phone, address, name))
            connect.commit()
        except sqlite3.Error as e:
             print(f"An error occurred: {e}")

# The connection will be closed automatically when the block ends
