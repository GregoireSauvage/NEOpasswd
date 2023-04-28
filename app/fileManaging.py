import json
import os

# Functions: load_users, load_data, load_password_data, save_master_key_and_salt_to_file, save_password_data_to_file

# Function to load the users from a JSON file
def load_users(filename):
    """
    Load the data from a JSON file.
    """
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
            if file_content == "":
                return []
                
            else:
                users = json.loads(file_content)["users"]
            
        # Check if all data is present in the file
        for user in users:
            if(user["username"] and user["master_key"] and user["salt"]):
                pass
            else:
                print("Invalid JSON data in file")
                exit(1)

    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")

    return users


# Function to load data from the JSON file
def load_data(filename):
    """
    Load password data from a JSON file.
    """
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "r") as f:
            data = f.read()
            if data == "":
                users = []
                print("No users found in file. Create a new user first.")
                exit(1)
                
            else:
                users = json.loads(data)["users"]
    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")

    # Print users
    print("----- Users -----")
    for user in users:
        print(user["username"])

    # Find the user data with the given username
    username = ""
    while username == "":
        username = input("Enter username: ")
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Incorrect username")
        return load_data(filename)

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
def load_password_data(filename):
    """
    Load password data from a JSON file for a specific service and user.
    """
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "r") as f:
            data = f.read()
            if data == "":
                users = []
                print("No users found in file. Create a new user first.")
                exit(1)
                
            else:
                users = json.loads(data)["users"]
                if not users:
                    print("No users found in file. Create a new user first.")
                    exit(1)

    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")

    # Print users
    print("----- Users -----")
    for user in users:
        print(user["username"])
    
    # Find the user data with the given username
    username = ""
    while username == "":
        username = input("Enter username: ")
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Incorrect username. Please try again.")
        return load_password_data(filename)

    # Convert hexadecimal strings to bytes
    salt = bytes.fromhex(user_data["salt"])

    # Print all the services for the user
    if "passwords" in user_data and len(user_data["passwords"]) > 0:
        print("----- Services -----")
        for password in user_data["passwords"]:
            print(password["service"])

        # Get the password data for the specified service from the user data
        service = ""
        while service == "":
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
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {"users": []}

        
    # Append the new user to the list of users
    existing_data["users"].append(data)
    
    try:
        with open(file_path, "w") as f:
            json.dump(existing_data, f)
    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")


# Function to remove a user from the JSON file
def remove_user_from_file(filename, users):
    """
    Save the updated list of users to a JSON file.
    """
    data = {"users": users}
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")
    
# Function to remove a user from the JSON file
def remove_password_from_file(filename, users, username, service):
    """
    Remove a password credential for a specific service from the JSON file.
    """
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError or json.JSONDecodeError:
        existing_data = {"users": []}

    # Find the user with the given username
    for user in existing_data["users"]:
        if user["username"] == username:
            # Remove the password credential of the specific service
            user["passwords"] = [credential for credential in user["passwords"] if credential["service"] != service]
            break

    # Save the updated data to the JSON file
    try:
        with open(file_path, "w") as f:
            json.dump(existing_data, f)
    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")



# Function to save the password data to a JSON file
def save_password_data_to_file(username, filename, password_id, service, email_address, encrypted_password):
    """
    Save password data to a JSON file.
    """
    file_path = os.path.join("../data", filename)
    with open(file_path, "r") as f:
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
    with open(file_path, "w") as f:
        json.dump(data, f)


# Functipon to save the modified user data to the JSON file
def save_data(filename, users):
    """
    Save the updated users data to the JSON file.
    """
    data = {
        "users": users
    }
    file_path = os.path.join("../data", filename)
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
    except FileNotFoundError:
        raise ValueError(f"File not found at path {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON data in file {file_path}")
