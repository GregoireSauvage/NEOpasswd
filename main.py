import sys
from createUser import create_user
from encryptPassword import add_password
from retrievePassword import retrieve_password

def main():
    choice = None
    print("Select an operation:")
    print("1. Create a new user")
    print("2. Add a new password")
    print("3. Retrieve a password")
    choice = input("Enter the number of the operation: ")
    
    if choice == '1':
        create_user()
    elif choice == '2':
        add_password()
    elif choice == '3':
        retrieve_password()
    else:
        print("Invalid choice. Exiting...")
        sys.exit(0)


try:
    main()

except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit(0)