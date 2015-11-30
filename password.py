import sqlite3
from passlib.hash import pbkdf2_sha256

db_path = "pass.sqlite"



def create_user(username, password):
    
    # check for nd.edu email
    address = username[-6:-1] + username[len(username) - 1]
    if address == "nd.edu":
        # check for existence of username already

        conn = sqlite3.connect(db_path)
        with conn:
            c = conn.cursor()
            sql = "select * from passwords where username = " + "'" + username + "'" 
            c.execute(sql)
            user = c.fetchone()
            if user:
                return False, "User already exists"
            else: # add user to the db
                pass_hash = pbkdf2_sha256.encrypt(password, rounds=200, salt_size=16)
                sql = 'insert into passwords values("' + username + '", "' + pass_hash + '")'
                c.execute(sql)
                return True, "User created successfully"

    else:
        return False, "Please register with a valid nd.edu email address" 

        
def validate_user(username, password):
    
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        sql = "select * from passwords where username = " + "'" + username + "'" 
        c.execute(sql)
        user = c.fetchone()
    
    if user is None:
        return False, "Username not found"
    
    if pbkdf2_sha256.verify(password, user[1]):
        return True, "Login Successful"
    else:
        return False, "Incorrect password"
    