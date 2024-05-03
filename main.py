import hashlib
import json
import secrets

try:
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
except FileNotFoundError:
    passwords = {}

def save_passwords():
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)

typer = input("Login or sign up? ")
if typer.lower() == "sign up":
  username = input("Enter username: ")
  if username in passwords:
    print("Username already exists.")
  else:
    password = input("Enter password: ")
    confirm = input("Confirm password: ")
    if password == confirm:
        if len(password) < 4 or len(password) > 8:
            print("Password must be between 4 and 8 characters")
        else:
            salt = secrets.token_hex(16)
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            passwords[username] = {"password_hash": password_hash, "salt": salt}
            save_passwords()
            print("Account created successfully!")
    else:
        print("Passwords do not match.")
        
elif typer.lower() == "login":
  username = input("Enter username: ")
  if username in passwords:
    password = input("Enter password: ")
    salt = passwords[username]["salt"]
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    if password_hash == passwords[username]["password_hash"]:
        print("Login successful!")
    else:
        print("Incorrect password.")
  else:
    print("Username does not exist.")
