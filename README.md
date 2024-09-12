# LoginPage

## Overview

This is a simple command-line-based user authentication system with sign-up and login functionality. Passwords are securely stored with unique salts and hashed using the SHA-256 algorithm.

## Features

- **Sign-up:** Create a new account with a username and password.
- **Login:** Access an existing account by verifying the password.
- **Secure password storage:** Passwords are salted and hashed before storage for security.
- **Password constraints:** Passwords must be 8-16 characters long, and usernames must be 4-16 characters long.

## How it Works

### Data Storage

The program reads from and writes to a JSON file (`passwords.json`) to store user credentials.

```python
try:
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
except FileNotFoundError:
    passwords = {}
```

If `passwords.json` doesn't exist, an empty dictionary is initialized to store the usernames and hashed passwords.

### Saving Passwords

A helper function `save_passwords()` is used to write the updated user credentials to the JSON file.

```python
def save_passwords():
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)
```

### Sign-up Process

- The user is prompted to create a username and password.
- Username requirements: 4-16 characters, must not already exist.
- Password requirements: 8-16 characters, must be confirmed by entering it twice.

```python
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
```

1. If the username already exists, sign-up is denied.
2. A unique 16-character salt is generated and combined with the password before being hashed using SHA-256. This ensures that even if two users have the same password, their stored credentials are different.

### Login Process

- The user is prompted to enter their username and password.
- The stored salt for that username is retrieved and combined with the entered password before hashing.
- The hashed value is compared to the stored password hash to verify the login.

```python
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
```

1. If the username does not exist, login fails.
2. The input password is hashed with the associated salt, and the hash is compared to the one stored in `passwords.json`.

### User Interface

The program runs in a continuous loop, asking the user to either sign up or log in.

```python
def main():
    while True:
        typer = input("Login or sign up? ").lower()
        if typer == "sign up":
            sign_up()
        elif typer == "login":
            login()
        else:
            print("Invalid input, please type 'login' or 'sign up'.")
```

## Notes

- Passwords are stored securely using both salt and hashing mechanisms.
- The `passwords.json` file format:
  ```json
  {
    "username": {
      "password_hash": "<hashed_password>",
      "salt": "<salt_value>"
    }
  }
  ```
- Ensure that when you reset or clear the `passwords.json` file, it contains an empty JSON object (`{}`) to avoid errors.
