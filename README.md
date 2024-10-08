# python-group10

# Inventory Management System

## User Login Information

The following are the default usernames and passwords for accessing the system:

| Username | Password | Role           |
| -------- | -------- | -------------- |
| ken      | ken      | Supply Manager |
| john     | john     | Supply Officer |
| admin    | admin123 | Super Admin    |

## How to Use

1. Clone or download the repository.
2. Run the inventory management system.
3. Use the login credentials provided above to log in and manage the inventory.

## Features

- Supply Manager

  - Add, search, View and remove items from the inventory
  - Display inventory in a table format.
  - Generate reports of items in stock.
  - Visualize inventory data using graphs.
  - View Logs

- Supply Officer

  - Update, search, View items from the inventory.
  - Display inventory in a table format.
  - Generate reports of items in stock.
  - Visualize inventory data using graphs.
  - View Logs

- Super Admin
  - Add new users
  - Assign Roles
  - Delete Users
  - View logs
  - View All users

# dependencies - Need to install

install dependencies in command prompt/terminal:

pip install python-dotenv
pip install matplotlib
pip install bcrypt
pip install colorama

# vscode - Instructions

cd project folder in vscode
run:
python main.py

# pycharm - Instructions

The getpass module is designed for terminal-based password input, and it can sometimes have issues in IDE environments like PyCharm.

in pycharm run in console

open console: alt+f12
run: python main.py
