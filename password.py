"""
Functions for creating and modifying users
"""

import sqlite3
from passlib.hash import pbkdf2_sha256

db_path = "reviews.sqlite"

def create_user(username, password, email):
    """
    Adds a user to the database
    """
    # check for nd.edu email
    address = email[-6:-1] + email[len(email) - 1]
    # validate legality of username
    for letter in username:
        print letter
        if (not isLegal(letter)):
            return False, "Please only include letters, numbers, and underscores in your username" 
        print letter
    if address == "nd.edu":
        # check for existence of username already

        conn = sqlite3.connect(db_path)
        with conn:
            c = conn.cursor()
            sql = "select * from userInfo where username = " + "'" + username + "'"
            c.execute(sql)
            user = c.fetchone()
            if user:
                return False, "User already exists"
            else: # add user to the db
                pass_hash = pbkdf2_sha256.encrypt(password, rounds=200, salt_size=16)
                #sql = 'insert into userInfo values("' + username + '", "' + pass_hash + '")'
                data = [username, pass_hash, email]
                c.executemany('INSERT INTO userInfo (username, password, email) VALUES(?,?,?)', (data,))
                #c.execute(sql)
                return True, "User created successfully"

    else:
        return False, "Please register with a valid nd.edu email address"

def change_password(username, password):
    """
    Changes the username of user with username @username
    to have the password @password
    """
    pass_hash = pbkdf2_sha256.encrypt(password, rounds=200, salt_size=16)
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        sql = ("update userInfo set password = '" + str(pass_hash) +
               "' where username = '" + str(username) + "'")
        c.execute(sql)

def validate_user(userinfo, password, email):
    """
    Attempts to verify a user login

    returns True if an email with parameters
    @email and @password exist in user database.
    False otherwise.
    """
    if email: # then validate user via email
        conn = sqlite3.connect(db_path)
        with conn:
            c = conn.cursor()
            sql = "select * from userInfo where email = " + "'" + userinfo + "'"
            c.execute(sql)
            user = c.fetchone()

        if user is None:
            return False, "User not found"

        if pbkdf2_sha256.verify(password, user[1]):
            return True, "Login Successful"
        else:
            return False, "Incorrect password"

    else: # then validate user via username
        conn = sqlite3.connect(db_path)
        with conn:
            c = conn.cursor()
            sql = "select * from userInfo where username = " + "'" + userinfo + "'"
            c.execute(sql)
            user = c.fetchone()

        if user is None:
            return False, "User not found"

        if pbkdf2_sha256.verify(password, user[1]):
            return True, "Login Successful"
        else:
            return False, "Incorrect password"

def isLegal(letter):
    """
    checks to see if letter is a letter, number or  underscore
    """
    letter = ord(letter)
    if (48 <= letter >= 57) or (65 <= letter <= 90) or (97 <= letter <= 122) or (letter == 95):
        return True
    return False
