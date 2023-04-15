import sys
from createUser import create_user
from encryptPassword import encrypt_password
from retrievePassword import retrieve_password

def main():
    choice = None
    print("Select an operation:")
    print("1. Create a new user")
    print("2. Add a new password")
    print("3. Retrieve a password")
    choice = input("Enter the number of the operation: ")

    if choice == '1':
        print(1)
        #create_user()
    elif choice == '2':
        print(2)
        #encrypt_password()
    elif choice == '3':
        print(3)
        #retrieve_password()
    else:
        print("Invalid choice. Exiting...")
        sys.exit(0)


print("Welcome to the password manager!")
if __name__ == "__main__":
    main()
