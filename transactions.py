import bcrypt
from datetime import datetime
import db

def _to_cents(amount: float) -> int:
    return round(amount * 100)

def _to_dollars(cents: int) -> float:
    return cents / 100

def get_name(id: int):
    return db.fetch_name(id)

def validate_user(id_input: int, password_input: str):
    password_hash = db.fetch_password_hash(id_input)
    if password_hash is None:
        return False
    return bcrypt.checkpw(password_input.encode(), password_hash.encode())

def sign_up_user(name_input: str, password_input: str, confirm_input):
    if name_input == "":
        print("Please enter a name")
        return

    if password_input != confirm_input:
        print("Please confirm password match")
        return

    password_hash = bcrypt.hashpw(password_input.encode(), bcrypt.gensalt()).decode()
    now = str(datetime.now())

    db.insert_user(name_input, password_hash, 0 , now)
    print("Signed up successfully, log in to continue")

def change_name(id: int, new_name: str):
    if db.fetch_name(id) == new_name:
        print("New name same to current name")
        return
    
    db.update_name(id, new_name)
    print(f"Name updated to {new_name} successfully")

def change_password(id: int, new_password: str):
    # To change implementation
    password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    db.update_password(id, password_hash)
    print("Password changed successfully")

def get_bal(id: int) -> float:
    balance_cents = db.fetch_balance(id)
    if balance_cents is None:
        print("Error occurred, account not found") # To change implementation
        return 0.0

    return _to_dollars(balance_cents)


def send_to_acc(sender: int, receiver: int, send_amount: float):
    if not db.id_exists(receiver):
        print("Something went wrong, please try again")
        return
    if sender == receiver:
        print("Error can't send to your own account")
        return 
    send_amount_cents = _to_cents(send_amount)
    sender_balance_cents = db.fetch_balance(sender)
    if sender_balance_cents is None:
        print("Error occurred, account not found")
        return
    if send_amount_cents > sender_balance_cents:
        print("Amount cannot be greater than balance")
        return
    receiver_balance_cents = db.fetch_balance(receiver)
    if receiver_balance_cents is None:
        print("Error occurred, account not found")
        return  
    sender_balance_cents -= send_amount_cents
    receiver_balance_cents += send_amount_cents
    db.update_balance(sender, sender_balance_cents)
    db.update_balance(receiver, receiver_balance_cents)
    print(f"Successfully sent ${send_amount:.2f} to account:{receiver}, balance is ${_to_dollars(sender_balance_cents):.2f}")
    now = str(datetime.now())
    db.insert_transaction(
        sender, 
        f"Sent ${send_amount:.2f} to account:{receiver}, new balance: ${_to_dollars(sender_balance_cents):.2f}",
        now)
    
    db.insert_transaction(
        receiver, 
        f"Received ${send_amount:.2f} from account:{sender}, new balance: ${_to_dollars(receiver_balance_cents):.2f}",
        now)


def deposit_to_acc(id: int, amount: float):
    if not db.id_exists(id):
        print("Error occurred, account not found")
        return
    if amount <= 0:
        print("Amount must be greater than 0")
        return
    amount_cents= _to_cents(amount)
    balance_cents = db.fetch_balance(id) 
    if balance_cents is None:
        print("Error occurred, account not found")
        return 
    balance_cents += amount_cents
    db.update_balance(id, balance_cents)
    print(f"Successfully deposited ${amount:.2f}, new balance is ${_to_dollars(balance_cents):.2f}")
    now = str(datetime.now())
    db.insert_transaction(
        id,
        f"Deposited ${amount:.2f}, new balance: ${_to_dollars(balance_cents):.2f}",
        now
    )

def withdraw_from_acc(id: int, amount: float):
    if not db.id_exists(id):
        print("Error occurred, account not found")
        return
    if amount <= 0:
        print("Amount must be greater than 0")
        return
    amount_cents= _to_cents(amount)
    balance_cents = db.fetch_balance(id)
    if balance_cents is None:
        print("Error occurred, account not found")
        return
    if amount_cents > balance_cents:
        print("Amount greater than balance")
        return
    balance_cents -= amount_cents
    db.update_balance(id, balance_cents)
    print(f"Successfully withdrew ${amount:.2f}, your new balance is ${_to_dollars(balance_cents):.2f}")
    now = str(datetime.now())
    db.insert_transaction(
        id,
        f"Withdrew ${amount:.2f}, new balance: ${_to_dollars(balance_cents):.2f}",
        now
    )

def get_transactions(id: int):
    return db.fetch_transactions(id)

