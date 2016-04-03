import sqlite3  # Database

from hashlib import sha512  # Hashing for Passwords
from uuid import uuid4  # Salting for Passwords

from re import search

def valid_data(username, password, repeat_password, email, users):
    print "VALIDATING DATA"
    usernames = []
    emails = []
    for user in users:
        usernames.append(user[0])
        emails.append(user[1])
    if username in usernames:
        return [False, "Username is already taken."]
    if email in emails:
        return [False, "Email is already used."]
    if password != repeat_password:
        return [False, "Passwords do not match."]
    #if len(password) < 8:
    #    return [False, "Your password must be at least 8 characters."]
    #if not (bool(search(r'\d', password)) and bool(search('[a-z]', password)) and bool(search('[A-Z]', password))):
    #    return [False, "Your password must include a lowercase letter, an uppercase letter, and a number"]"""
    return [True, "Your information has been validated."]

def valid_create(username, password, repeat_password, name, email):
    print "CREATING USER"
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    q = 'CREATE TABLE IF NOT EXISTS user_database (user_id INT, username TEXT, password INT, salt INT, name TEXT, email TEXT)'
    c.execute(q)
    q = 'SELECT username, email FROM user_database'
    users = c.execute(q)
    valid = valid_data(username, password, repeat_password, email, users)
    if not valid[0]:
        conn.close()
        return valid
    else:
        salt = uuid4().hex
        hash_password = sha512((password + salt) * 10000).hexdigest()
        q = 'SELECT COUNT(*) FROM user_database'
        num_rows = c.execute(q).fetchone()[0]
        q = 'INSERT INTO user_database (user_id, username, password, salt, name, email) VALUES (?, ?, ?, ?, ?, ?)'
        c.execute(q, (num_rows + 1, username, hash_password, salt, name, email))
        conn.commit()
        conn.close()
        return [True, "Successful Account Creation"]

def valid_login(username, password):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    q = 'SELECT name FROM sqlite_master WHERE TYPE = "table" AND NAME = "user_database"'
    c.execute(q)
    if not c.fetchone():
        conn.close()
        return -1
    q = 'SELECT password, salt FROM user_database WHERE username = ?'
    pepper_and_salt = c.execute(q, (username,)).fetchone()
    if pepper_and_salt and sha512((password + pepper_and_salt[1]) * 10000).hexdigest() == pepper_and_salt[0]:
        q = "SELECT user_id FROM user_database WHERE username = ?"
        id = c.execute(q, (username,)).fetchone()
        conn.close()
        return id[0]
    conn.close()
    return -1