import os
from datetime import datetime
import matplotlib.pyplot as plt
from log import log_item_change, log_item_removal

INVENTORY_FILE = "./db/inventory_db.txt"

# Save the inventory to a file
def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        for item_id, data in inventory.items():
            f.write(f"{item_id},{data['item']},{data['quantity']},{data['date_added']},{data['user_added']}\n")

# Load the inventory from the file
def load_inventory():
    inventory = {}
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            for line in f:
                item_id, item, qty, date_added, user_added = line.strip().split(',')
                inventory[item_id] = {
                    'item': item,
                    'quantity': int(qty),
                    'date_added': date_added,
                    'user_added': user_added
                }
    return inventory

# Display the inventory in a table format
def display_inventory(inventory):
    if not inventory:
        print("\nInventory is empty.")
    else:
        print("\nCurrent Inventory:")
        print(f"{'ID':<10} {'Item':<20} {'Quantity':<10} {'Date Added':<15} {'User Added':<15}")  # Header
        print("=" * 75)  # Separator
        for item_id, data in inventory.items():
            print(f"{item_id:<10} {data['item']:<20} {data['quantity']:<10} {data['date_added']:<15} {data['user_added']:<15}")  # Align columns
    print()

# Print a report of the inventory
def print_report(inventory):
    if not inventory:
        print("\nNo items in inventory to report.")
    else:
        print("\nInventory Report:")
        print(f"{'ID':<10} {'Item':<20} {'Quantity':<10} {'Date Added':<15} {'User Added':<15}")  # Header
        print("=" * 75)  # Separator
        for item_id, data in inventory.items():
            print(f"{item_id:<10} {data['item']:<20} {data['quantity']:<10} {data['date_added']:<15} {data['user_added']:<15}")  # Align columns
        print()

# Generate a new ID for an item
def generate_item_id(inventory):
    return str(len(inventory) + 1)  # Simple incremental ID based on current inventory length

# Add a new item to the inventory (with logging)
def add_item(inventory, user):
    item_name = input("Enter item name: ").strip()
    
    while True:
        try:
            qty = int(input(f"Enter quantity for '{item_name}': ").strip())
            break  # Exit loop if input is a valid integer
        except ValueError:
            print("Invalid input. Please enter a valid integer for quantity.")
    
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_id = generate_item_id(inventory)
    
    print(f"Adding new item '{item_name}' with quantity: {qty}")
    log_item_change(user, "Added item", item_name, qty)
    inventory[item_id] = {
        'item': item_name,
        'quantity': qty,
        'date_added': date_added,
        'user_added': user
    }  # Add new item with details
    
    save_inventory(inventory)

# Update an existing item in the inventory (with logging)
def update_item(inventory, user):
    item_name = input("Enter item name to update: ").strip()
    
    while True:
        try:
            qty = int(input(f"Enter new quantity for '{item_name}': ").strip())
            break  # Exit loop if input is a valid integer
        except ValueError:
            print("Invalid input. Please enter a valid integer for quantity.")

    for id, data in inventory.items():
        if data['item'] == item_name:
            print(f"Updating '{item_name}' with new quantity: {qty}")
            log_item_change(user, "Updated item", item_name, qty)
            data['quantity'] = qty  # Update quantity
            save_inventory(inventory)
            return

    print(f"Item '{item_name}' not found in the inventory.")

# Remove an item from the inventory (with logging)
def remove_item(inventory, user):
    item_name = input("Enter item name to remove: ").strip()
    item_id_to_remove = None
    
    for item_id, data in inventory.items():
        if data['item'] == item_name:
            item_id_to_remove = item_id
            break
    
    if item_id_to_remove:
        del inventory[item_id_to_remove]
        print(f"Removed '{item_name}' from the inventory.")
        log_item_removal(user, item_name)
        save_inventory(inventory)
    else:
        print(f"Item '{item_name}' not found in the inventory.")

# Search for an item in the inventory
def search_item(inventory):
    item_name = input("Enter item name to search: ").strip()
    for item_id, data in inventory.items():
        if data['item'] == item_name:
            print(f"ID: {item_id}, Item: {data['item']}, Quantity: {data['quantity']}, Date Added: {data['date_added']}, User Added: {data['user_added']}")
            return
    print(f"Item '{item_name}' not found in the inventory.")

# Display a bar graph of items and their quantities
def display_graph(inventory):
    if not inventory:
        print("\nNo items to display in graph.")
        return
    
    items = [data['item'] for data in inventory.values()]
    quantities = [data['quantity'] for data in inventory.values()]

    plt.figure(figsize=(10, 5))
    plt.bar(items, quantities, color='skyblue')
    plt.xlabel('Items')
    plt.ylabel('Quantity')
    plt.title('Inventory Items and Their Quantities')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def display_graph_by_date(inventory):
    if not inventory:
        print("\nNo items to display in graph.")
        return
    
    # Prepare data for the first graph (items and their quantities)
    items = [data['item'] for data in inventory.values()]
    quantities = [data['quantity'] for data in inventory.values()]

    # Plot the items and their quantities
    plt.figure(figsize=(12, 6))

    # Bar graph for items and their quantities
    plt.subplot(1, 2, 1)  # Create subplot for items
    plt.bar(items, quantities, color='skyblue')
    plt.xlabel('Items')
    plt.ylabel('Quantity')
    plt.title('Inventory Items and Their Quantities')
    plt.xticks(rotation=45, ha='right')

    # Prepare data for the second graph (total added per date)
    date_counts = {}
    for data in inventory.values():
        date = data['date_added'].split(' ')[0]  # Get the date part
        quantity = data['quantity']
        if date in date_counts:
            date_counts[date] += quantity
        else:
            date_counts[date] = quantity

    dates = list(date_counts.keys())
    total_added = list(date_counts.values())

    # Bar graph for total added per date
    plt.subplot(1, 2, 2)  # Create subplot for date totals
    plt.bar(dates, total_added, color='salmon')
    plt.xlabel('Date')
    plt.ylabel('Total Added')
    plt.title('Total Items Added Per Date')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()
