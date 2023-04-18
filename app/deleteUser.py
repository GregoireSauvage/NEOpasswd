from fileManaging import load_users
from fileManaging import load_data
from fileManaging import remove_user_from_file
from utilities import check_master_key

# Function to delete a user
def delete_user(filename):
    """
    Delete a user from the data.
    """
    users = load_users(filename)

    username, hashed_key, salt, id_service, services = load_data(filename)
    
    # Find the user data with the given username
    user_data = next((user for user in users if user["username"] == username), None)
    if user_data is None:
        print("Username does not exist. Please enter a different username.")
        return delete_user(filename)
    
    # Get username and passphrase from user
    check_master_key(hashed_key, salt)
        
    # security check
    print("Are you sure you want to delete " + username + "?")
    print("This action cannot be undone.")
    while check != f"delete {username}":
        check = input(f"Enter 'delete {username}' to confirm or 'cancel' to cancel: ")
        print(check)
        if check == "cancel":
            print("Delete user cancelled.")
            exit(1)
            
    # Remove the user from the data
    users.remove(user_data)
    remove_user_from_file(filename, users)
    print("User " + username + " deleted")

    