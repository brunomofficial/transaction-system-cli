import sqlite3
from sqlite3 import SQLITE_ERROR

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

def get_name(id):
    name = cursor.execute("SELECT name FROM users where id = (?)", (id,)).fetchone()[0]
    return name

def get_all_ids():
    ids_list = []
    all_ids = cursor.execute("SELECT id FROM users").fetchall()
    for id in all_ids:
        ids_list.append(id[0])

    return ids_list

def id_found(id):
    if id not in get_all_ids():
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
    if password_input != confirm_input:
        print("Passwords must be similar")
    else:
        password_hash = bcrypt.hashpw(password_input.encode(), bcrypt.gensalt()).decode()
        now = str(datetime.now())

        cursor.execute("INSERT INTO users (name, password_hash, balance, date_created) VALUES (?,?,?,?)",
                       (name_input, password_hash, 0, now))
        conn.commit()

        print(f"Added successfully, welcome {name_input}")

def add_new_password(id, current_password):
    password_hash = bcrypt.hashpw(current_password.encode(), bcrypt.gensalt()).decode()

    try:
        cursor.execute("UPDATE users SET password_hash = (?) WHERE id = (?)", (password_hash, id))
        conn.commit()
        print("Password changed successfully")
    except SQLITE_ERROR:
        print("Something went wrong please try again")


def get_bal(id):
    cursor.execute("SELECT balance FROM users WHERE id = (?)", (id,))
    bal = cursor.fetchone()[0]
    return bal

def send_to_acc(sender, receiver, send_amount):
    if not id_found(receiver):
        print("Something went wrong please try again")
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
        print(f"SUCCESSFULLY SENT {send_amount} to {receiver}")

    except SQLITE_ERROR:
        print("Something went wrong please try again")

def deposit_from_acc(id, amount):
    if not id_found(id):
        print("Error occurred, account not found")
        return

    if amount <= 0:
        print("Amount must be greater than 0")
        return

    balance = get_bal(id)

    try:
        balance = balance + amount

        cursor.execute("UPDATE users SET balance = (?) WHERE id = (?)", (balance, id))
        conn.commit()

        print(f"Successfully deposited {amount}, new balance is {balance}")

    except SQLITE_ERROR:
        print("Something went wrong, please try again")



def withdraw_from_acc(id, amount):
    if not id_found(id):
        print("Error occurred, account not found")
        return
    if amount <= 0:
        print("Amount must be greater than 0")
        return
    if amount > get_bal(id):
        print("Amount greater than your balance, please try again")
        return

    balance = get_bal(id)

    try:
        balance = balance - amount
        cursor.execute("UPDATE users SET balance = (?) WHERE id = (?)", (balance, id))
        conn.commit()

        print(f"Successfully sent {amount}, your new balance is {balance}")

    except SQLITE_ERROR:
        print("Something went wring please try again")


