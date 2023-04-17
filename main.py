import sys
from createUser import create_user
from encryptPassword import add_password
from retrievePassword import retrieve_password
from deleteUser import delete_user
from deletePassword import delete_password
from modifyPassword import modify_password
from modifyUser import modify_user

def main(filename):
    choice = None
    print("Select an operation:")
    print("1. Create a new user")
    print('2. Modify a user')
    print('3. Delete a user')
    print("4. Add a new password")
    print("5. Retrieve a password")
    print('6. Modify a password')
    print('7. Delete a password')
    print('8. Exit')
    choice = input("Enter the number of the operation: ")
    
    if choice == '1':
        print("< CREATE A NEW USER >")
        create_user(filename)
    elif choice == '2':
        print("< MODIFY A USER >")
        modify_user(filename)
    elif choice == '3':
        print("< DELETE A USER >")
        delete_user(filename)
    elif choice == '4':
        print("< ADD A NEW PASSWORD TO ENCRYPT >")
        add_password(filename)
    elif choice == '5':
        print("< RETRIEVE A PASSWORD >")
        retrieve_password(filename)
    elif choice == '6':
        print("< MODIFY A PASSWORD >")
        modify_password(filename)
        exit(0)
    elif choice == '7':
        print("< DELETE A PASSWORD >")
        delete_password(filename)
    elif choice == '8':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice.")
        return main(filename)


try:
    filename = "passwordManager.json"
    main(filename)

except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit(0)