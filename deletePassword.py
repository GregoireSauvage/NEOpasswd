from fileManaging import load_users
from fileManaging import remove_password_from_file
from utilities import check_master_key
from fileManaging import load_data

# Function to delete a password
def delete_password(filename):
    """
    Delete a password from the data.
    """
    users = load_users(filename)

    username, hashed_key, salt, id_service, services = load_data(filename)
    
    # Find the user data with the given username
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Username does not exist. Please enter a different username.")
        return delete_password(filename)
    
    # Get username and passphrase from user
    check_master_key(hashed_key, salt)
    
    
    # Load user's password credentials
    passwords = user_data.get("passwords", [])
    if not passwords:
        print("No stored passwords found for the user.")
        exit(1)

    else:
        service = ""
        while service == "":
            service = input("Enter service to remove: ")
        
        password_data = next((password for password in passwords if password["service"] == service), None)
        if password_data is None:
            print("Service does not exist. Please enter a different service.")
            return delete_password(filename)
        
    # security check
    print("Are you sure you want to delete " + service + "?")
    print("This action cannot be undone.")
    check = ""
    while check != f"delete {service}":
        check = input(f"Enter 'delete {service}' to confirm or 'cancel' to cancel: ")
        print(check)
        if check == "cancel":
            print("Delete service cancelled.")
            exit(1)

    # Remove the password credential of the service from the data
    remove_password_from_file(filename, users, username, service)
    print(username + "'s password credentials for " + service + " are deleted.")
