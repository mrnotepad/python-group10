import time
import sys
from colorama import init, Fore, Style
from auth import load_users, login_user, admin_login, admin_add_user, admin_delete_user, view_users
from inventory import load_inventory, save_inventory, display_inventory, add_item, update_item, remove_item, search_item, display_graph, display_graph_by_date
from log import log_login, view_logs

# Initialize Colorama
init(autoreset=True)

def print_header(title, user_type=None):
    print("\n" + "=" * 40)
    
    # Modify the title based on the user type
    if user_type == "supply_manager":
        title = f"Supply Manager Menu: {title}"
    elif user_type == "supply_officer":
        title = f"Supply Officer Menu: {title}"
    
    print(f"{Fore.CYAN}{title:^40}{Style.RESET_ALL}")
    print("=" * 40)

def loading_animation(message):
    print(f"{Fore.YELLOW}{message} ", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(Style.RESET_ALL)  # Reset style

def inventory_management(user, password_hash, user_type):
    inventory = load_inventory()
    
    while True:
        print_header("Supply Inventory Management", user_type=user_type)
        print(f"{Fore.GREEN}1. View Inventory")
        if user_type == "supply_manager":  # Supply Manager
            print(f"{Fore.GREEN}2. Add Item")
            print(f"{Fore.GREEN}3. Remove Item")
            print(f"{Fore.GREEN}4. Update Item (limited)")
        elif user_type == "supply_officer":  # Supply Officer
            
            print(f"{Fore.GREEN}4. Update Item ")  # Optionally limited functionality
        print(f"{Fore.GREEN}5. Search Item")
        print(f"{Fore.GREEN}6. View Logs")
        print(f"{Fore.GREEN}7. Display Graph")
        print(f"{Fore.GREEN}8. Display Graph by date")
        print(f"{Fore.GREEN}9. Save & Exit")
        choice = input("Choose an option (1-9): ").strip()
        
        if choice == '1':
            display_inventory(inventory)
        elif choice == '2' and user_type in ["supply_manager"]: 
            add_item(inventory, user)
        elif choice == '3' and user_type in ["supply_manager"]:  
            remove_item(inventory, user)
        elif choice == '4' and user_type == "supply_officer":  # Only supply manager can update items
            update_item(inventory, user)
        elif choice == '5':
            search_item(inventory)
        elif choice == '6':
            view_logs()
        elif choice == '7':
            display_graph(inventory)
        elif choice == '8':
            display_graph_by_date(inventory)
        elif choice == '9':
            loading_animation("Saving Inventory")
            save_inventory(inventory)
            print("Inventory saved. Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid choice or permission denied. Please try again.{Style.RESET_ALL}")

def main():
    users = load_users()
    
    while True:
        print_header("Welcome to the Supply Inventory System")
        print(f"{Fore.GREEN}1. Login")
        print(f"{Fore.GREEN}2. Admin Login")
        print(f"{Fore.GREEN}3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == '1':
            result = login_user(users)
            if result:  # Ensure login_user returns a valid result
                user, password_hash, user_type = result
                log_login(user)
                inventory_management(user, password_hash, user_type)  # Pass user type to inventory management
            else:
                print(f"{Fore.RED}Login failed. Please try again.{Style.RESET_ALL}")
        elif choice == '2':
            if admin_login():
                while True:
                    print_header("Admin Menu")
                    print(f"{Fore.GREEN}1. Add User")
                    print(f"{Fore.GREEN}2. Delete User")
                    print(f"{Fore.GREEN}3. View Logs")
                    print(f"{Fore.GREEN}4. View all users")
                    print(f"{Fore.GREEN}5. Logout")
                    admin_choice = input("Choose an option (1-5): ").strip()
                    
                    if admin_choice == '1':
                        admin_add_user(users)
                    elif admin_choice == '2':
                        admin_delete_user(users)
                    elif admin_choice == '3':
                        view_logs()
                    elif admin_choice == '4':
                        view_users(users)
                    elif admin_choice == '5':
                        print("Admin logged out.")
                        break
                    else:
                        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
