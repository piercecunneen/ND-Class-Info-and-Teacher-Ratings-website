import sqlite3
from passlib.hash import pbkdf2_sha256

db_path = "pass.sqlite"

def create_user(username, password):
    
    pass_hash = pbkdf2_sha256.encrypt(password, rounds=200, salt_size=16)
    
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        sql = 'insert into passwords values("' + username + '", "' + pass_hash + '")'
        print sql
        c.execute(sql) 
        
def validate_user(username, password):
    
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        sql = "select * from passwords where username = " + "'" + username + "'" 
        c.execute(sql)
        user = c.fetchone()
    print user
    
    if user is None:
        return False
    
    return pbkdf2_sha256.verify(password, user[1])
    
#test script

x = validate_user("zj", "pass")
print x