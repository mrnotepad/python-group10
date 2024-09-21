import datetime

LOG_FILE = "./db/activity_log.txt"

# Log any general activity
def log_activity(user, action, details=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] User: {user}, Action: {action}, Details: {details}\n")

# Log user login
def log_login(user):
    log_activity(user, "Logged in")

# Log item added or updated
def log_item_change(user, action, item, quantity):
    log_activity(user, action, f"Item: {item}, Quantity: {quantity}")

# Log item removal
def log_item_removal(user, item):
    log_activity(user, "Removed item", f"Item: {item}")

# View logs
def view_logs():
    print("\n=== Activity Logs ===")
    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
            if logs:
                for log in logs:
                    print(log.strip())
            else:
                print("No logs available.")
    except FileNotFoundError:
        print("No logs available.")
    print()
