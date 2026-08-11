import transactions as ts

user_id = None
allowed_attempts: int = 5 # to add rate limiting later

hr = "--------------------\n"

def to_id(user_input):
    try:
        user_input = int(user_input)

        if user_input < 0:
            print("Amount cannot be less than 0")
            return None
        
        return user_input
    
    except ValueError:
        return None
    
def to_amount(user_input):
    try:
        user_input = float(user_input)
        if user_input < 0:
            print("Amount cannot be lesser than 0")
            return None
        return user_input
    except ValueError:
        return None
    
# Start Menu
def start_menu():
    print(f"{hr}\n1. Sign in\n2. Register\n0. exit")

    choice = input("Enter an option> ").strip()

    match choice :
        case '1': 
            return "sign_in"
        case '2':
            return "register"
        case '0':
            print("Bye")
            return "quit"
        case _:
            print("Invalid input, please try again")
            return "start"
    

# SIGN IN
def sign_in():
    print(f"{hr}\nEnter your tsentials or 0 to go back")
    id_input = input("_Enter id> ").strip()
    if id_input == '0':
        return None, 'start'
 
    id_input = to_id(id_input)
    if id_input is None:
        print("Please enter a valid id")
        return None, "sign_in"
    
    password_input = input("_Enter password> ").strip()

    if not ts.validate_user(id_input, password_input):
        print("Log in unsuccessful please try again")
        return None, "sign_in"
    
    print("Logged in successfully")
    name = ts.get_name(id_input)
    print(f"WELCOME {name}\n{hr}")
    return id_input, "home"


# REGISTER
def register():
    name_input = input(f"{hr}\n_Enter name>").strip()

    if name_input.strip() == "":
        print("Please enter a name")
        return None, "start"

    password_input = input("_Enter a password>").strip()
    confirm_input = input("_Confirm password>").strip()

    ts.sign_up_user(name_input, password_input, confirm_input)
    return None, "start"


# HOME MENU
def home_menu(user_id):
    print(f"{hr}\n1. My Account\n2. Send\n3. Deposit\n4. Withdraw\n0. Log Out")
    choice = input("Enter choice> ").strip()

    match choice:
        case '1': 
            return "account_info"
        case '2': 
            return "send"
        case '3': 
            return "deposit"
        case '4': 
            return "withdraw"
        case '0':
            return "logout"
        case _:
            print("Invalid input please try again")
            return "home"
        

# ACCOUNT INFORMATION
def account_info(user_id):
    print(f"{hr}\n1. Check Balance\n2. Change password\n3. Change credentials\n4. Transaction History\n0. Back")

    choice = input("Enter choice> ").strip()

    match choice:
        case '1':
            balance = ts.get_bal(user_id)
            print(f"{hr}\nYour balance is ${balance:.2f}")
            return "account_info"
        case '2':
            return "change_password"
        case '3':
            return "change_creds"
        case '4':
            return "view_history"
        case '0':
            return "home"
        case _:
            print("Invalid input, please try again")
            return "account_info"        

# change credentials
def change_creds(user_id):
    choice = input(f"{hr}\nEnter credential to change:\n 1. Name\n2. Clear transaction history\n0. Back> ")

    if choice == "" or choice not in('1', '2', '0'):
        print("Please enter a valid choice")
        return "account_info"
    
    if choice == '0':
        return "account_info"
    
    if choice == "1":
        new_name = input("Enter new name> ")
        confirmation = input("Enter 1 to confirm or 0 to go back > ")
        if confirmation == '1':
            ts.change_name(user_id, new_name)
        return "account_info"

    elif choice == '2':
        print("Clearing transaction history is coming soon")
        return "account_info"


# change password
def change_password(user_id):
    current_password = input(f"{hr}\nEnter your current password or 0 to go back>")
    if current_password == "":
        print("Please enter a valid password")
        return "account_info"
    if current_password == '0':
        return "account_info"
    if not ts.validate_user(user_id, current_password):
        print("Invalid password, please try again")
        return "account_info"        
    new_password=input("_Enter new password>")
    new_password2=input("_Confirm new password>")
    if new_password != new_password2:
        print("Password didn't match, please try again")
        return "account_info"    
    ts.change_password(user_id, new_password)
    return "home"   

def view_history(user_id):
    print(f"{hr}\nYour transactions: ")
    transactions = ts.get_transactions(user_id)
    if transactions:
        for note, created_at in transactions:
            print(f"{created_at} : {note}")
    else:
        print("No transactions yet")
    return "account_info"

# SEND
def send(user_id):
    receiver_acc = input(f"{hr}\nEnter receiver account or 0 to go back>").strip()

    if receiver_acc == "0":
        return "home"
    
    receiver_acc = to_id(receiver_acc)

    if receiver_acc is None:
        print("Please enter valid id")
        return "send"
    
    amount = input("Enter amount to send>").strip()
    amount = to_amount(amount)

    if amount is None:
        print("Please enter valid amount")
        return "send"
    
    print(f"Send {amount} to {receiver_acc}?, enter 1 to confirm or 0 to cancel")
    confirm_send = input("_Confirm? > ")

    if confirm_send == '1':
        ts.send_to_acc(user_id, receiver_acc, amount)

    return "home"
        

# DEPOSIT
def deposit(user_id):
    amount = input(f"{hr}\nEnter amount to deposit or 0 to go back> ").strip()

    if amount == "":
        print("Please enter an amount")
        return "deposit"

    if amount == '0':
        return "home"
    
    amount = to_amount(amount)
    if amount is None:
        print("Please enter a valid amount")
        return "deposit"

    ts.deposit_to_acc(user_id, amount)
    return "home"

# WITHDRAW
def withdraw(user_id):
    amount = input(f"{hr}\nEnter amount to withdraw or 0 to go back> ").strip()

    if amount == "":
        print("Please enter an amount")
        return "withdraw"
    
    if amount == '0':
        return "home"
    
    amount = to_amount(amount)
    if amount is None:
        print("Please enter a valid amount")
        return "withdraw"

    ts.withdraw_from_acc(user_id, amount)
    return "home"

def main():
    print(f"{hr}\nWELCOME")
    state = "start"
    user_id = None

    while True:
        match state:
            case "start":
                state = start_menu()
            case "sign_in":
                user_id, state = sign_in()
            case "register":
                user_id, state = register()
            case "home":
                state = home_menu(user_id)
            case "logout":
                user_id = None
                state = "start"
            case "account_info":
                state = account_info(user_id)
            case "change_password":
                state = change_password(user_id)
            case "change_creds":
                state = change_creds(user_id)
            case "view_history":
                state = view_history(user_id)
            case "send":
                state = send(user_id)
            case "deposit":
                state = deposit(user_id)
            case "withdraw":
                state = withdraw(user_id)
            case "quit":
                break

if __name__ == "__main__":
    main()
