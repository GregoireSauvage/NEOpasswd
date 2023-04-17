from fileManaging import load_users
from fileManaging import load_data
from utilities import check_master_key
import getpass
from utilities import enter_password
from fileManaging import save_data

# Function to modify a password
def modify_password(filename):
    
    users = load_users(filename)
    username, hashed_key, salt, id_service, services = load_data(filename)
    
    # Find the user data with the given username
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Username does not exist. Please enter a different username.")
        return modify_password(filename)
    
    # Check the user master passphrase 
    check_master_key(hashed_key, salt)
    
    # Load user's password credentials
    passwords = user_data.get("passwords", [])
    if not passwords:
        print("No stored passwords found for the user.")
        exit(1)

    else:
        print("----- Services -----")
        for s in services:
            print(s)
        service = ""
        while service == "":
            service = input("Enter service to modify: ")
            password_data = next((password for password in passwords if password["service"] == service), None)
            if password_data is None:
                print("Service does not exist. Please enter a different service.")
                service = ""
        
        previous_email = password_data["email"]

    # Once the master key is correct, get the email and password to encrypt
    print(f"< SERVICE TO MODIFY: {service} >")
    print(f"previous email: {previous_email} >")
    email = ""
    while email == "":
        email = input("Enter new email address: ")
    new_password = enter_password()

    # Update the password data for the specified service
    for p in passwords:
        if p["service"] == service:
            p["email"] = email
            p["encrypted_password"] = new_password  # Use the correct variable name here

    # Update the user's password credentials
    user_data["passwords"] = passwords

    # Save the updated data to the JSON file
    save_data(filename, users)

    print(f"{username}'s password credentials for {service} have been updated.")
    
    users = load_users(filename)
    username, hashed_key, salt, id_service, services = load_data(filename)
    
    # Find the user data with the given username
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Username does not exist. Please enter a different username.")
        return modify_password(filename)
    
    # Check the user master passphrase 
    check_master_key(hashed_key, salt)
    
    # Load user's password credentials
    passwords = user_data.get("passwords", [])
    if not passwords:
        print("No stored passwords found for the user.")
        exit(1)

    else:
        print("----- Services -----")
        for s in services:
            print(s)
        service = ""
        while service == "":
            service = input("Enter service to modify: ")
            password_data = next((password for password in passwords if password["service"] == service), None)
            if password_data is None:
                print("Service does not exist. Please enter a different service.")
                service = ""
        
        previous_email = password_data["email"]

    # Once the master key is correct, get the email and password to encrypt
    print(f"< SERVICE TO MODIFY: {service} >")
    print(f"previous email: {previous_email} >")
    email = ""
    while email == "":
        email = input("Enter new email address: ")
    password = enter_password()
    print(password)
    # Update the password data for the specified service
    for p in passwords:
        if p["service"] == service:
            password["email"] = email
            password["encrypted_password"] = password  

    # Update the user's password credentials
    user_data["encrypted_password"] = passwords

    # Save the updated data to the JSON file
    save_data(filename, users)

    print(f"{username}'s password credentials for {service} have been updated.")

    