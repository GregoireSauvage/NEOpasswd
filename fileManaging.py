import json

# Functions: load_users, load_data, load_password_data, save_master_key_and_salt_to_file, save_password_data_to_file

# Function to load the users from a JSON file
def load_users(filename):
    """
    Load the data from a JSON file.
    """
    try:
        with open(filename, "r") as f:
            users = json.load(f)["users"]
        
        # Check if all data is present in the file
        for user in users:
            if(user["username"] and user["master_key"] and user["salt"]):
                pass
            else:
                print("Invalid JSON data in file")
                exit(1)

    except FileNotFoundError:
        raise ValueError(f"File not found at path {filename}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {filename}")

    return users


# Function to load data from the JSON file
def load_data(file_path):
    """
    Load password data from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)["users"]
    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")

    # Print users
    print("----- Users -----")
    for user in data:
        print(user["username"])

    # Find the user data with the given username
    username = input("Enter username: ")
    user_data = next((user for user in data if user["username"] == username), None)
    if user_data is None:
        print("Incorrect username")
        exit(0)

    hashed_key = user_data["master_key"]

    # Convert hexadecimal strings to bytes
    salt = bytes.fromhex(user_data["salt"])

    if "passwords" in user_data and len(user_data["passwords"]) > 0:
        id_service = max([p["id"] for p in user_data["passwords"]]) + 1
    else:
        id_service = 1

    if "passwords" in user_data:
        services = [p["service"] for p in user_data["passwords"]]
    else:
        services = []

    # Return the decrypted password data
    return username, hashed_key, salt, id_service, services

# Function to load password data from a JSON file for a specific service and user
def load_password_data(file_path):
    """
    Load password data from a JSON file for a specific service and user.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)["users"]

    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")

    # Print users
    print("Users: " + ", ".join([user["username"] for user in data]))
    
    # Find the user data with the given username
    username = input("Enter username: ")
    user_data = next((user for user in data if user["username"] == username), None)
    if user_data is None:
        raise ValueError("Incorrect username")

    # Convert hexadecimal strings to bytes
    salt = bytes.fromhex(user_data["salt"])

    # Print all the services for the user
    if "passwords" in user_data:
        print("Services: " + ", ".join([password["service"] for password in user_data["passwords"]]))

        # Get the password data for the specified service from the user data
        service = input("Enter service (gmail for example): ")
        password_data = next((password for password in user_data["passwords"] if password["service"] == service), None)
        if password_data is None:
            raise ValueError("Service not found in password data.")
        
        encrypted_password = bytes.fromhex(password_data["encrypted_password"])
        email = password_data["email"]

    else:
        print(f"No password data found for user {username}")
        exit(0)
        
    # Return the decrypted password data
    return salt, encrypted_password, service, username, email

# Function to save the master key and salt to a JSON file
def save_master_key_and_salt_to_file(filename, hashed_key, username, salt):
    """
    Save the username, master key, and salt to a JSON file.
    """
    data = {
        "username": username,
        "master_key": hashed_key,
        "salt": salt.hex()
    }
    
    try:
        with open(filename, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {"users": []}
        
    # Append the new user to the list of users
    existing_data["users"].append(data)
    
    try:
        with open(filename, "w") as f:
            json.dump(existing_data, f)
    except FileNotFoundError:
        raise ValueError(f"File not found at path {filename}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {filename}")


# Function to save the password data to a JSON file
def save_password_data_to_file(username, filename, password_id, service, email_address, encrypted_password):
    """
    Save password data to a JSON file.
    """
    with open(filename, "r") as f:
        data = json.load(f)

    # Create a new password entry
    password_entry = {
        "id": password_id,
        "service": service,
        "email": email_address,
        "encrypted_password": encrypted_password.hex()
    }

    # Find the user data with the given username
    user_data = next((user for user in data["users"] if user["username"] == username), None)

    # Add the password entry to the user's data
    if "passwords" in user_data:
        user_data["passwords"].append(password_entry)
    else:
        user_data["passwords"] = [password_entry]

    # Write the updated data dictionary to the file
    with open(filename, "w") as f:
        json.dump(data, f)
