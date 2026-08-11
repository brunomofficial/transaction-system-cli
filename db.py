import sqlite3
import uuid

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            date_created TEXT NOT NULL,
            balance_cents INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR(20) PRIMARY KEY,
            user_id INTEGER NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()

init_db()

def id_exists(id: int) -> bool :
    return cursor.execute("SELECT 1 FROM users WHERE id = (?)", (id, )).fetchone() is not None

def fetch_name(id: int) -> str | None:
    row = cursor.execute("SELECT name FROM users WHERE id = (?)", (id,)).fetchone()
    return row[0] if row else None

def insert_user(name: str, password_hash: str, balance_cents: int, date_created: str):
    cursor.execute('''
        INSERT INTO users (name, password_hash, balance_cents, date_created)
        VALUES (?, ?, ?, ?)
    ''', (name, password_hash, balance_cents, date_created)
    )
    conn.commit()

def update_name(id: int, new_name: str):
    cursor.execute("UPDATE users SET name = (?) WHERE id = (?)", (new_name, id))
    conn.commit()

# Passwords
def fetch_password_hash(id: int) -> str | None:
    row = cursor.execute("SELECT password_hash FROM users WHERE id = (?)", (id,)).fetchone()
    return row[0] if row else None

def update_password(id: int, password_hash: str):
    cursor.execute('''
        UPDATE users
        SET password_hash = (?)
        WHERE id = (?)
    ''', (password_hash, id))

    conn.commit()

# Balance
def fetch_balance(id: int) -> int | None:
    row = cursor.execute('''
        SELECT balance_cents FROM users WHERE id = (?)
    ''', (id,)
    ).fetchone()
    return row[0] if row else None

def update_balance(id, balance_cents):
    cursor.execute('''
        UPDATE users 
        SET balance_cents = (?)
        WHERE id = (?)
    ''', (balance_cents, id))
    conn.commit()

# Transactions

def insert_transaction(user_id: int, note: str, created_at: str):
    transaction_id = str(uuid.uuid4()) # will swap to uuid7 later
    cursor.execute('''
        INSERT INTO transactions (transaction_id, user_id, note, created_at) 
        VALUES (?, ?, ?, ?)''',
        (transaction_id, user_id, note, created_at)
    )

    conn.commit()
    

def fetch_transactions(user_id: int):
    return cursor.execute('''
        SELECT note, created_at 
        FROM transactions 
        WHERE user_id = (?)
        ORDER BY transaction_id
        ''', 
        (user_id,)).fetchall()
