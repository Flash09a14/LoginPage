# LoginPage

## How it works:

## main.py
```py
try:
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
except FileNotFoundError:
    passwords = {}

def save_passwords():
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)
```
#### First block of code reads the json file "passwords.json", and saves the data as "passwords"
#### Second block of code, we make a new function to save the passwords into the database

```py
typer = input("Login or sign up? ")
if typer.lower() == "sign up":
  username = input("Enter username: ")
  if username in passwords:
    print("Username already exists.")
```
#### We take input as "typer" and check if the user wants to sign up or login (.lower() makes sure that the input is registered in all lowercase so it can accept all cases of input)
#### If the user wants to sign up, we ask for the username. We then check if the username is in the database, and, if so, disallow them to make it (we don't want rare cases of duplication, even with salting)

```py
  else:
    password = input("Enter password: ")
    confirm = input("Confirm password: ")
    if password == confirm:
        if len(password) < 4 or len(password) > 8:
            print("Password must be between 4 and 8 characters")
```
#### If it doesn't exist, now we can ask for them to choose a password and confirm it. If the password matches the confirmation, we then check the length of the password to make sure it isn't too small

```py
        else:
            salt = secrets.token_hex(16)
            password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            passwords[username] = {"password_hash": password_hash, "salt": salt}
            save_passwords()
            print("Account created successfully!")
```
#### If it isn't too small, we now generate a random 16-bit salt and a hash using the SHA256 algorithm. We combine both to create a random and unique encryption string that is exclusive to a specific user, even if they choose the same password as someone else (although make sure not to use predictable passwords either way :) )

```py
    else:
        print("Passwords do not match.")
```
#### Just a simple else statement after the confirm check to disallow them to create a new username if they failed to match their chosen passwords

```py
elif typer.lower() == "login":
  username = input("Enter username: ")
  if username in passwords:
    password = input("Enter password: ")
    salt = passwords[username]["salt"]
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    if password_hash == passwords[username]["password_hash"]:
        print("Login successful!")
```
#### Checks back into our "typer" input to make a case for a login
#### We take the username, confirm if it is in the database
#### If it is, we find the salt string that is located within the user's data in the database
#### We combine the salt string with the hash of the password input to check if they match the password hash stored int he database, and if they do, log them in

```py
    else:
        print("Incorrect password.")
  else:
    print("Username does not exist.")
```
#### Final two else statements, one for the password input and the other for the username input


## Make sure that the JSON file already has a dictionary in it to prevent errors.
#### When clearing out the database, make sure to add 2 curly braces to prevent any incorrect formatting
```json
{}
```
