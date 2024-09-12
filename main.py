import hashlib
import json
import secrets
import getpass

try:
    with open("passwords.json", "r") as f:
        passwords = json.load(f)
except FileNotFoundError:
    passwords = {}


def save_passwords():
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)


def sign_up():
    username = input("Enter username: ")
    if username in passwords:
        print("Username already exists.")
        return

    if not 4 <= len(username) <= 16:
        print("Username must be between 4-16 characters")
        return

    password = getpass.getpass("Enter password: ")
    confirm = getpass.getpass("Confirm password: ")
    
    if password != confirm:
        print("Passwords do not match.")
        return

    if len(password) < 8 or len(password) > 16:
        print("Password must be between 8 and 16 characters.")
        return

    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    passwords[username] = {"password_hash": password_hash, "salt": salt}
    save_passwords()
    print("Account created successfully!")


def login():
    username = input("Enter username: ")
    if username not in passwords:
        print("Username does not exist.")
        return

    password = getpass.getpass("Enter password: ")
    salt = passwords[username]["salt"]
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()

    if password_hash == passwords[username]["password_hash"]:
        print("Login successful!")
    else:
        print("Incorrect password.")


def main():
    while True:
        typer = input("Login or sign up? ").lower()
        if typer == "sign up":
            sign_up()
        elif typer == "login":
            login()
        else:
            print("Invalid input, please type 'login' or 'sign up'.")


if __name__ == "__main__":
    main()
