import sqlite3 as lite


datebase = "textbooks.db"

def Create_Textbook_DB():
	conn = lite.connect(datebase)

	with conn:
		c = conn.cursor()
		query = '''CREATE TABLE TextBookPosts (date text, textbook_name text,seller text, email text, price text, description text)'''
		c.execute(query)
		conn.commit()

def Insert(date, text, seller, email, price, description):

	conn = lite.connect(datebase)
	data = [date, text, seller, email, price, description]
	with conn:
		c = conn.cursor()
        c.executemany('INSERT INTO TextBookPosts VALUES(?,?,?,?,?,?)',(data,))
        conn.commit()



Insert("f", "Textbook1", "Pierce", "pcunneen@nd.edu", "100", "Cool textbook")
