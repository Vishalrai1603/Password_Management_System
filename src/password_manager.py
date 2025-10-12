from database import setup_database
from user_operations import signup, login
from password_operations import add_password, view_passwords, search_password, delete_password


def main_menu():
    print("\n" + "="*40)
    print("     PASSWORD MANAGER")
    print("="*40)
    print("1. Signup")
    print("2. Login")
    print("3. Exit")
    print("="*40)


def user_menu():
    print("\n" + "="*40)
    print("     PASSWORD MANAGER")
    print("="*40)
    print("1. Add Password")
    print("2. View Password")
    print("3. Search Password")
    print("4. Delete Password")
    print("5. Logout")
    print("="*40)


def main():

    setup_database()

    current_user_id = None

    while True:

        if current_user_id is None:
            main_menu()
            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("\nInvalid input! Please enter a number.")
                continue

            if choice == 1:
                # Signup
                print("\n--- SIGNUP ---")
                username = input("Enter username:")
                password = input("Enter password:")
                signup(username, password)

            elif choice == 2:
                # Login
                print("\n--- LOGIN ---")
                username = input("Enter username:")
                password = input("Enter password:")
                user_id = login(username, password)
                if user_id:
                    current_user_id = user_id
            elif choice == 3:
                # Exit
                print("\nThank you for using Password Manager. Goodbye!")
                break

            else:
                print("\nInvalid choice. Please enter 1, 2, or 3.")

        else:
            user_menu()
            try:
                choice = int(input("\nEnter your choice: "))
            except ValueError:
                print("\nInvalid input! Please enter a number.")
                continue

            if choice == 1:
                print("\n--- ADD PASSWORD ---")
                website = input("Enter website/app name:")
                web_username = input("Enter website username:")
                web_password = input("Enter password:")
                add_password(current_user_id, website,
                             web_username, web_password)

            elif choice == 2:
                view_passwords(current_user_id)

            elif choice == 3:
                print("\n--- SEARCH PASSWORD ---")
                website = input("Enter website/app name to search: ")
                search_password(current_user_id, website)

            elif choice == 4:
                print("\n--- DELETE PASSWORD ---")
                password_id = input("Enter password ID to delete: ")
                try:
                    password_id = int(password_id)
                    delete_password(current_user_id, password_id)
                except ValueError:
                    print("\nInvalid ID. Please enter a number.")

            elif choice == 5:
                # Logout
                print("\nLogged out successfully!")
                current_user_id = None

            else:
                print("\nInvalid choice. Please try again.")


main()
