import os
import bcrypt
from dotenv import load_dotenv
from colorama import init, Fore, Style
import getpass  # Import getpass for masking password input

# Initialize Colorama
init(autoreset=True)

load_dotenv()  # Load environment variables from .env file

USER_FILE = "./db/users_db.txt"
ADMIN_USER = os.getenv("ADMIN_USER")  # Load from environment variable
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")  # Load from environment variable

# Hash the admin password if it's not already hashed
if not ADMIN_PASSWORD or ADMIN_PASSWORD.startswith('$2b$'):  # Check if already hashed
    raise ValueError("Admin password must be set in the environment variable and should be hashed.")

# Load the users from a file
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for line in f:
                username, password_hash, user_type = line.strip().split(',')
                users[username] = {'password_hash': password_hash, 'user_type': user_type}
    return users

# Hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verify a password
def verify_password(stored_password_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash.encode('utf-8'))

# Register a new user
def register_user(users):
    username = input("Enter a username: ").strip()
    if username in users:
        print(f"{Fore.RED}Username already exists. Please choose another.")
        return None
    password = getpass.getpass("Enter a password: ").strip()  # Masked password input
    password_hash = hash_password(password)  # Hash the password

    # User type selection
    print("Select user type:")
    print("1. Supply Officer")
    print("2. Supply Manager")
    user_type_choice = input("Choose an option (1 or 2): ").strip()

    if user_type_choice == '1':
        user_type = 'supply officer'
    elif user_type_choice == '2':
        user_type = 'supply manager'
    else:
        print(f"{Fore.RED}Invalid choice. Defaulting to 'supply officer'.")
        user_type = 'supply officer'

    users[username] = {'password_hash': password_hash, 'user_type': user_type}
    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{password_hash},{user_type}\n")
    print(f"User '{username}' registered successfully as '{user_type}'.")
    return username

# Login an existing user
def login_user(users):
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ").strip()  # Masked password input
    if username in users and verify_password(users[username]['password_hash'], password):
        print(f"Welcome back, {username}! Your role is: {users[username]['user_type']}.")
        # Return username, password_hash, and user_type
        return username, users[username]['password_hash'], users[username]['user_type']
    else:
        print("Invalid username or password.")
        return None

# Admin login
def admin_login():
    username = input("Enter admin username: ").strip()
    password = getpass.getpass("Enter admin password: ").strip()  # Masked password input
    if username == ADMIN_USER and verify_password(ADMIN_PASSWORD, password):
        print("Admin logged in successfully.")
        return True
    else:
        print(f"{Fore.RED}Invalid admin credentials.")
        return False

# Add a new user (admin only)
def admin_add_user(users):
    username = input("Enter new username: ").strip()
    if username in users:
        print("Username already exists. Please choose another.")
        return
    password = getpass.getpass("Enter password for new user: ").strip()  # Masked password input
    password_hash = hash_password(password)  # Hash the password

    # User type selection
    print("Select user type:")
    print("1. Supply Officer")
    print("2. Supply Manager")
    user_type_choice = input("Choose an option (1 or 2): ").strip()

    if user_type_choice == '1':
        user_type = 'supply_officer'
    elif user_type_choice == '2':
        user_type = 'supply_manager'
    else:
        print(f"{Fore.RED}Invalid choice. Defaulting to 'supply officer'.")
        user_type = 'supply_officer'

    users[username] = {'password_hash': password_hash, 'user_type': user_type}
    with open(USER_FILE, 'a') as f:
        f.write(f"{username},{password_hash},{user_type}\n")
    print(f"User '{username}' added successfully as '{user_type}'.")

# Delete a user (admin only)
def admin_delete_user(users):
    username = input("Enter username to delete: ").strip()
    if username in users:
        del users[username]
        print(f"User '{username}' deleted successfully.")
        with open(USER_FILE, 'w') as f:
            for user, data in users.items():
                f.write(f"{user},{data['password_hash']},{data['user_type']}\n")
    else:
        print(f"User '{username}' not found.")

# View all users
def view_users(users):
    if not users:
        print(f"{Fore.YELLOW}No users found.")
    else:
        print(f"\n{'Username':<20} {'User Type':<15} {'Password Hash'}")
        print("=" * 70)
        for username, data in users.items():
            print(f"{username:<20} {data['user_type']:<15} {data['password_hash']}")  # Display username, user type, and hashed password

