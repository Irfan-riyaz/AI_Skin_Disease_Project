import sqlite3
from datetime import datetime
import hashlib

conn = sqlite3.connect('app.db')
cur = conn.cursor()

# Create admin user
username = 'admin'
email = 'admin@skincare.ai'
password = 'admin123'
account_type = 'admin'
created_at = datetime.now().isoformat()

# Hash password
password_hash = hashlib.sha256(password.encode()).hexdigest()

try:
    cur.execute("""
        INSERT INTO users (username, email, password, account_type, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (username, email, password_hash, account_type, created_at))
    conn.commit()
    print("Admin user created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
except sqlite3.IntegrityError as e:
    print(f"User already exists: {e}")

conn.close()
