import sqlite3
import string
import re
from datetime import datetime

# --------------------------------------------------------functions
def is_valid_password(password):
    if len(password) < 8:
        return False, "Too short (min 8 chars)"
    if not any(char.isupper() for char in password):
        return False, "Missing uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Missing lowercase letter"
    if not any(char.isdigit() for char in password):
        return False, "Missing digit"
    if not any(char in string.punctuation for char in password):
        return False, "Missing special character"
    
    return True, "Strong password"

def is_valid_syntax(email):
    # A standard pattern for common email formats
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(pattern, email):
        return True
    return False

# ------------------------------------------------------------
def initialize_database():
    """Creates the tables if they do not exist."""
    conn = sqlite3.connect('digital_wallet.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create wallets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            wallet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT NOT NULL,
            balance DECIMAL(12,2) DEFAULT 0.00,
            currency VARCHAR(10) DEFAULT 'USD',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    return conn, cursor

def insert_balance(cursor, conn):
    # Check if user exists by email
    email = input("Enter your email: ")
    
    
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    user_result = cursor.fetchone()

    if not user_result:
        print("Your email is not registered. Go register first.")
        return

    user_id = user_result[0] # Extract the ID from the tuple (e.g., (1,))

    
    cursor.execute("SELECT wallet_id FROM wallets WHERE user_id = ?", (user_id,))
    wallet_result = cursor.fetchone()

    if wallet_result:
        print("This user already has a wallet.")
        return

    
    try:
        balance = float(input("Put money you wanna add: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    # Get currency
    currencys = ["USD", "EUR", "TND"]
    currency = input("Give the type of currency USD/EUR/TND: ").upper()
    while currency not in currencys:
        currency = input("Invalid currency. Give the type again (USD/EUR/TND): ").upper()

    # Insert the wallet
    try:
        cursor.execute(
            "INSERT INTO wallets (user_id, balance, currency) VALUES (?, ?, ?)",
            (user_id, balance, currency)
        )
        conn.commit()
        print(f"Wallet created successfully with balance {balance} {currency}.")
    except Exception as e:
        print(f"Error creating wallet: {e}")

def insert_user(cursor, conn):
    # Get inputs
    username = input("Give your username >> ")
    
    email = input("Give your email >> ")
    while not is_valid_syntax(email):
        print("Invalid email syntax.")
        email = input("Give your email >> ")
    
    password = input("Give password >> ")
    # Fix: is_valid_password returns a tuple (bool, message)
    is_valid, message = is_valid_password(password)
    while not is_valid:
        print(message)
        password = input("Give password >> ")
        is_valid, message = is_valid_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
            (username, email, password)
        )
        conn.commit()
        print(f"User '{username}' added successfully!")
        
    except sqlite3.IntegrityError:
        print("Error: Username or Email already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def aff_b(cursor):
    email=input("give email")
    cursor.execute("SELECT balance ,currency FROM wallets LEFT JOIN users ON wallets.user_id = users.user_id and email=?",(email,))
    storage=cursor.fetchall()
    for j in storage:
        print(f"you have {j[0]} {j[1]} in your email related wallet")
    
    
def aff_u(cursor):
    email=input("give email")
    cursor.execute("select * from users where email=?",(email,))
    data=cursor.fetchall()
    for i in data:
        print(f"user name : {i[1]} || email : {i[2]} || user_first_login : {i[4]}")
def main():
    conn, cursor = initialize_database()
    
    while True:
        action = input("\nChoose action: register / add money / exit: / show ").lower().strip()
        
        if action == "register":
            insert_user(cursor, conn)
            
        elif action == "add money":
            insert_balance(cursor, conn)
            
        elif action == "exit":
            print("Goodbye!")
            break
        elif action == "show":
            type=input ("type of info you wanna see balance / user_login_info")
            if type=="balance":
                aff_b(cursor)
            elif type=="user_login_info":
                aff_u(cursor)
        else:
            print("Unknown command. Try 'register', 'add money', or 'exit'.")
        
    conn.close()

if __name__ == "__main__":
    main()