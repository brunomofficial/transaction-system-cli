import cred
user_id = None
allowed_attempts: int = 5

def lines():
    print("------------------")

def to_num(user_input):
    try:
        return int(user_input)
    except ValueError:
        print("Error occurred")
        return None

# REGISTER
def register():
    lines()
    name_input = input("_Enter name>").strip()
    if name_input.strip() == "":
        return

    password_input = input("_Enter a password>").strip()
    confirm_input = input("_Confirm password>").strip()
    if password_input.strip()  == "" or confirm_input.strip() == "":
        return

    cred.sign_up_user(name_input, password_input, confirm_input)
    return

# SIGN IN
def sign_in():
    global allowed_attempts
    global user_id

    while allowed_attempts > 0:
        lines()
        print("Enter your credentials or 0 to go back")
        id_input = input("_Enter id> ").strip()

        if id_input == '0':
            return

        allowed_attempts -= 1

        id_input = to_num(id_input)

        if not id_input:
            print("Please enter a valid id")
            continue

        password_input = input("_Enter password> ").strip()

        if cred.validate_user(id_input, password_input):
            user_id = id_input
            print("Logged in successfully")
            name = cred.get_name(id_input)
            print(f"WELCOME {name}")
            home_menu()
            allowed_attempts = 5
            lines()
            return
        else:
            print("Log in unsuccessful please try again")
            print(f"You have {allowed_attempts} attempts left")

            if allowed_attempts == 0:
                exit(0)

            continue

# HOME MENU
def home_menu():
    global user_id
    while True:
        lines()
        print("1. My Account\n2. Send\n3. Deposit\n4. Withdraw\n0. Log Out")
        choice = input("Enter choice> ").strip()

        match choice:
            case '1': account_info()
            case '2': send()
            case '3': deposit()
            case '4': withdraw()
            case '0':
                user_id = None
                return
            case _:
                print("Invalid choice please try again")
                continue

# ACCOUNT INFORMATION
def account_info():
    while True:
        lines()
        print("1. Check Balance\n2. Change password\n3. Change credentials\n0. Back")
        choice: str= input("Enter choice> ").strip()

        match choice:
            case '1':
                balance = cred.get_bal(user_id)
                lines()
                print(f"Your balance is ${balance}")
                lines()
                return
            case '2':
                change_password()
            case '3':
                change_creds()
            case '0':
                return
            case _:
                print("Invalid input, please try again")
                continue

# change credentials
def change_creds():
    while True:
        lines()
        choice = input("_Enter credential to change: 1. Name or 0. to go back> ")
        if choice == "" or choice not in('1', '0',):
            print("Please enter a valid choice")
            continue
        if choice == '0':
            return

        if choice == '1':
            new_name = input("Enter new name> ")
            confirmation = input("Enter 1 to confirm or 0 to go back > ")
            if confirmation == '1':
                cred.change_name(user_id, new_name)
                return
        continue

# change password
def change_password():
    while True:
        lines()
        current_password = input("_Enter your current password or 0 to go back>")

        if current_password == "":
            print("Please enter a valid password")
            continue

        if current_password == '0':
            return

        if not cred.validate_user(user_id, current_password):
            print("Invalid password, please try again")
            return
        else:
            new_password=input("_Enter new password>")
            new_password2=input("_Confirm new password>")

            if new_password != new_password2:
                print("Password didn't match, please try again")
                continue
            else:
                cred.add_new_password(user_id, new_password)
                return
# SEND
def send():
    while True:
        lines()
        receiver_acc = input("_Enter receiver account or 0 to go back>")
        if receiver_acc == "0":
            return

        if to_num(receiver_acc):
            receiver_acc = to_num(receiver_acc)
        else:
            print("Please enter valid id")
            continue

        amount: str = input("Enter amount to send>")
        if to_num(amount) <= 0:
            print("Amount must be greater than 0")
        if to_num(amount):
            amount:int = to_num(amount)
        else:
            print("Please enter valid amount")
            continue

        print(f"Send {amount} to {receiver_acc}?, enter 1 to confirm or 0 to cancel")
        confirm_send = input("_Confirm? > ")

        if confirm_send == '1':
            cred.send_to_acc(user_id, receiver_acc, amount)
            return
        else:
            return

# DEPOSIT
def deposit():
    while True:
        lines()
        amount = input("Enter amount to deposit or 0 to go back> ").strip()
        if amount == "":
            print("Please enter an amount")
            continue
        if amount == '0':
            return
        if not to_num(amount):
            print("Please enter a valid amount")
            continue
        if to_num(amount) <= 0:
            print("Amount must be greater than 0")

        amount = to_num(amount)
        cred.deposit_to_acc(user_id, amount)
        return

# WITHDRAW
def withdraw():
    while True:
        lines()
        amount = input("Enter amount to withdraw or 0 to go back> ").strip()
        if amount == "":
            print("Please enter an amount")
            continue
        if amount == '0':
            return
        if not to_num(amount):
            print("Please enter a valid amount")
            continue
        if to_num(amount) <= 0:
            print("Amount must be greater than 0")

        amount = to_num(amount)
        cred.withdraw_from_acc(user_id, amount)
        return

def main():
    lines()
    print("\tWELCOME")
    lines()

    while True:
        lines()
        print("1. Sign in\n2. Register\n0. exit")

        choice: str = input("Enter an option> ").strip()
        match choice:
            case '1':
                sign_in()
            case '2':
                register()
            case '0':
                print("Bye")
                exit(0)
            case _:
                print("Invalid option")


if __name__ == "__main__":
    main()