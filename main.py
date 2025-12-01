import sys
from auth.user_manager import get_current_user
from ui.prompts import prompt_login, prompt_register, prompt_logout
from ui.menus import transactions_menu, reports_menu, help_menu,advanced_features_menu, pause



# ========== Main Menu ==========

def main_menu():
    while True:
        user = get_current_user()
        if not user:
            print("\n=== Welcome to the Finance Manager ===")
            print("1. Log in")
            print("2. Create New User")
            print("3. Exit")
            choice = input("Choose: ").strip()

            if choice == "1":
                prompt_login()
            elif choice == "2":
                prompt_register()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
            
        else:
            print(f"\n=== Main Menu (Logged in as {user['name']}) ===")
            print("1. Transactions")
            print("2. Reports")
            print("3. Advanced Features")
            print("4. Help")
            print("5. Logout")
            print("6. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                transactions_menu()
            elif choice == "2":
                reports_menu()
            elif choice == "3":
                advanced_features_menu()
            elif choice == "4":
                help_menu()
            elif choice == "5":
                prompt_logout()
            elif choice == "6":
                print("Goodbye! Your finances are now under control.")
                sys.exit(0)
            else:
                print("Invalid option. Please try again.")
            pause()


if __name__ == "__main__":
    main_menu()
