import sqlite3
import bcrypt
from datetime import datetime

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def get_all_names():
    names_list = []
    all_names = cursor.execute("SELECT name FROM users").fetchall()

    for name in all_names:
        names_list.append(name[0])

    return names_list

def get_name(user_id):
    try:
        name = cursor.execute("SELECT name FROM users where id = (?)", (user_id,)).fetchone()[0]
        return name
    except sqlite3.Error:
        print("Failed to get name")

def get_all_ids():
    ids_list = []
    all_ids = cursor.execute("SELECT id FROM users").fetchall()
    for id in all_ids:
        ids_list.append(id[0])

    return ids_list

def id_found(user_id):
    if user_id not in get_all_ids():
        return False
    else:
        return True

def validate_user(id_input, password_input):
    if id_input not in get_all_ids():
        return False

    (select_id, password_hash) = cursor.execute("SELECT id, password_hash FROM users WHERE id = (?)", (id_input,)).fetchone()

    if bcrypt.checkpw(password_input.encode(), password_hash.encode()):
        return True
    else:
        return False

def sign_up_user(name_input, password_input, confirm_input):
    if name_input == "":
        print("Please enter a name")
        return
    if password_input != confirm_input:
        print("Passwords must be similar")
        return
    else:
        password_hash = bcrypt.hashpw(password_input.encode(), bcrypt.gensalt()).decode()
        now = str(datetime.now())

        cursor.execute("INSERT INTO users (name, password_hash, balance, date_created, transactions) VALUES (?,?,?,?,?)",
                       (name_input, password_hash, 0, now, ""))
        conn.commit()

        print(f"Added successfully, welcome {name_input}")



def add_new_password(user_id, current_password):
    password_hash = bcrypt.hashpw(current_password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("UPDATE users SET password_hash = (?) WHERE id = (?)", (password_hash, user_id))
        conn.commit()
        print("Password changed successfully")
    except sqlite3.Error:
        print("Something went wrong please try again")

def change_name(user_id, new_name):
    current_name = get_name(user_id)
    if current_name == new_name:
        print("New name same to current name")
        return

    try:
        cursor.execute("UPDATE users SET name = (?) WHERE id = (?)", (new_name, user_id))
        conn.commit()

        print(f"Name updated successfully to {new_name}")
    except sqlite3.Error as e:
        print("Something went wrong, please try again")


def get_bal(user_id):
    cursor.execute("SELECT balance FROM users WHERE id = (?)", (user_id,))
    bal = cursor.fetchone()[0]
    return bal


def send_to_acc(sender, receiver, send_amount):
    if not id_found(receiver):
        print("Something went wrong please try again")
        return
    if sender == receiver:
        print("Error, can't send to your own account")
        return

    sender_balance = get_bal(sender)
    if send_amount > sender_balance:
        print("Amount cannot be greater than your balance")
        return

    receiver_balance = get_bal(receiver)

    try:
        sender_balance = sender_balance - send_amount
        receiver_balance = receiver_balance + send_amount

        cursor.execute("UPDATE users SET balance = (?) WHERE id = (?)", (sender_balance, sender))
        cursor.execute("UPDATE users SET balance = (?) WHERE id = (?)", (receiver_balance, receiver))
        conn.commit()
        print(f"SUCCESSFULLY SENT ${send_amount} to account-{receiver} your new balance is ${sender_balance}")

    except sqlite3.Error:
        print("Something went wrong please try again")

def deposit_to_acc(user_id, amount):
    if not id_found(user_id):
        print("Error occurred, account not found")
        return

    if amount <= 0:
        print("Amount must be greater than 0")
        return

    balance = get_bal(user_id)

    try:
        balance = balance + amount

        cursor.execute("UPDATE users SET balance = (?) WHERE id = (?)", (balance, user_id))
        conn.commit()

        print(f"Successfully deposited {amount}, new balance is ${balance}")

    except sqlite3.Error:
        print("Something went wrong, please try again")

def withdraw_from_acc(user_id, amount):
    if not id_found(user_id):
        print("Error occurred, account not found")
        return
    if amount <= 0:
        print("Amount must be greater than 0")
        return
    if amount > get_bal(user_id):
        print("Amount greater than your balance, please try again")
        return

    balance = get_bal(user_id)

    try:
        balance = balance - amount
        cursor.execute("UPDATE users SET balance = (?) WHERE id = (?)", (balance, user_id))
        conn.commit()

        print(f"Successfully withdrew {amount}, your new balance is ${balance}")

    except sqlite3.Error:
        print("Something went wrong please try again")

