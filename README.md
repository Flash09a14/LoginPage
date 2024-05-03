# LoginPage

## How it works:

The `main.py` file contains Python code responsible for handling the login and sign-up functionalities.

```python
import json
import secrets
import hashlib

try:
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
except FileNotFoundError:
    passwords = {}

def save_passwords():
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)
```

The first block of code reads the JSON file "passwords.json" and defines the `passwords` dictionary with its content. The second block defines a function `save_passwords()` to save the passwords into the database.

```python
typer = input("Login or sign up? ")
if typer.lower() == "sign up":
    username = input("Enter username: ")
    if username in passwords:
        print("Username already exists.")
```

The code takes input as `typer` to determine if the user wants to sign up or login. `.lower()` ensures that the input is registered in lowercase for case-insensitive comparison. If the user chooses to sign up, the code asks for a username. It then checks if the username already exists in the database and notifies the user accordingly to avoid duplication.

```python
    else:
        password = input("Enter password: ")
        confirm = input("Confirm password: ")
        if password == confirm:
            if len(password) < 4 or len(password) > 8:
                print("Password must be between 4 and 8 characters")
```

If the username does not exist, the code prompts the user to enter a password and confirm it. If the password matches the confirmation, it checks the length of the password to ensure it meets the required length.

```python
            else:
                salt = secrets.token_hex(16)
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
                passwords[username] = {"password_hash": password_hash, "salt": salt}
                save_passwords()
                print("Account created successfully!")
```

If the password meets the length requirement, a random 16-bit salt is generated using `secrets.token_hex(16)`. The password and salt are combined and hashed using the SHA256 algorithm. The resulting hash and salt are stored in the `passwords` dictionary associated with the username. The `save_passwords()` function is called to update the database, and a success message is printed.

```python
        else:
            print("Passwords do not match.")
```

If the password and confirmation do not match, an error message is displayed.

```python
elif typer.lower() == "login":
    username = input("Enter username: ")
    if username in passwords:
        password = input("Enter password: ")
        salt = passwords[username]["salt"]
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        if password_hash == passwords[username]["password_hash"]:
            print("Login successful!")
```

For the login option, the code prompts the user to enter their username. If the username exists in the database, it asks for the password. It retrieves the salt stored with the username and hashes the entered password with the retrieved salt. If the resulting hash matches the stored password hash, a success message is displayed.

```python
        else:
            print("Incorrect password.")
    else:
        print("Username does not exist.")
```

If the entered password does not match the stored hash, an error message is displayed. Final `else` statement checks if the username exists in the database, if not, an error message is printed

## Notes:

Make sure that the JSON file already has a dictionary in it to prevent errors. When clearing out the database, make sure to add 2 curly braces `{}` to prevent any incorrect formatting.

```json
{}
```
