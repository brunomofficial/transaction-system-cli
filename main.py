import cred


def lines():
    print("------------------")

def to_num(user_input):
    try:
        user_input = int(user_input)
        if user_input < 0:
            print("Amount cannot be less than 0")
            return None

        return user_input

    except ValueError:
        return None


def sign_in():
    lines()
    print("Enter your credentials or 0 to go back")
    id_input = input("_Enter id> ").strip()

    if id_input == '0':
        main()

    id_input = to_num(id_input)

    if not id_input:
        print("Please enter a valid id")
        sign_in()

    password_input = input("_Enter password> ").strip()

    if cred.validate_user(id_input, password_input):
        lines()
        print("Logged in successfully")
        name = cred.get_name(id_input)
        print(f"WELCOME {name}")
        lines()
        home_menu(id_input)
    else:
        print("Log in unsuccessful please try again")
        sign_in()


def register():
    lines()
    name_input = input("_Enter name>").strip()

    password_input = input("_Enter a password>").strip()
    confirm_input = input("_Confirm password>").strip()

    cred.sign_up_user(name_input, password_input, confirm_input)

    main()


def forgot_password():
    main()


def home_menu(id_input):
    home_menu_list: str = "1. My Account\n2. Send\n3. Deposit\n4. Withdraw\n5. Log Out"

    id = id_input

    print(home_menu_list)
    choice = input("Enter choice> ").strip()

    match choice:
        case '1': account_info(id)
        case '2': send(id)
        case '3': deposit(id)
        case '4': withdraw(id)
        case '5': main()


def change_password(id):
    user_id = id
    current_password = input("_Enter your current password>")

    if current_password == "":
        print("Please enter a valid password")
        change_password(user_id)

    if not cred.validate_user(id, current_password):
        print("Invalid password, please try again")
    else:
        new_password=input("_Enter new password>")
        new_password2=input("_Confirm new password>")

        if new_password != new_password2:
            print("Password didn't match, please try again")
            change_password(user_id)
        else:
            cred.add_new_password(user_id, new_password)
            main()


def account_info(id):
    lines()

    print("1. Check Balance\n2. Change password\n3. Change credentials\n4. Transaction history\n5. Back")

    choice: str= input("Enter choice> ").strip()

    match choice:
        case '1':
            balance = cred.get_bal(id)
            lines()
            print(f"\tYour balance is ${balance}")
            lines()
            account_info(id)
        case '2':
            change_password(id)
        case '3':
            change_creds(id)
        case '4':
            view_transaction_history(id)
        case '5':
            home_menu(id)
        case _:
            print("Invalid input, please try again")
            account_info(id)

def change_creds(id):
    pass

def view_transaction_history(id):
    pass

def send(id):
    receiver_acc = input("_Enter receiver account or 0 to go back>")
    if receiver_acc == "0":
        home_menu(id)

    if to_num(receiver_acc):
        receiver_acc = to_num(receiver_acc)
    else:
        print("Please enter valid id")
        send(id)


    amount = input("Enter amount to send>")
    if to_num(amount):
        amount = to_num(amount)
    else:
        print("Please enter valid id")
        send(id)



    print(f"Send {amount} to {receiver_acc}?, enter 1 to confirm or 0 to cancel")
    confirm_send = input("_Confirm? > ")

    if confirm_send == '1':
        cred.send_to_acc(id, receiver_acc, amount)
        home_menu(id)
    else:
        home_menu(id)


def deposit(id):
    lines()
    amount = input("Enter amount to deposit or 0 to go back> ").strip()
    if amount == "":
        print("Please enter an amount")
        deposit(id)
    if amount == '0':
        home_menu(id)
    if not to_num(amount):
        print("Please enter a valid amount")
        deposit(id)

    amount = to_num(amount)

    cred.deposit_from_acc(id, amount)

    home_menu(id)


def withdraw(id):
    lines()
    amount = input("Enter amount to withdraw or 0 to go back> ").strip()
    if amount == "":
        print("Please enter an amount")
        deposit(id)
    if amount == '0':
        home_menu(id)
    if not to_num(amount):
        print("Please enter a valid amount")
        deposit(id)

    if not to_num(amount):
        print("Please enter a valid amount")
        withdraw(id)

    amount = to_num(amount)
    cred.withdraw_from_acc(id, amount)

    home_menu(id)

lines()
print("\tWELCOME")
lines()

def main():
    lines()
    print("1. Sign in\n2. Register\n3. Forgot password\n4. exit")
    choice = input("Enter an option> ").strip()

    match choice:
        case '1':
            sign_in()
        case '2':
            register()
        case '3':
            forgot_password()
        case '4':
            print("Bye")
            exit(0)
        case _:
            main()


if __name__ == "__main__":
    main()