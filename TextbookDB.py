import sqlite3 as lite
import datetime as dt

datebase = "reviews.sqlite"

def Create_Textbook_table():
	conn = lite.connect(datebase)

	with conn:
		c = conn.cursor()
		query = '''CREATE TABLE TextBookPosts (ID  INTEGER PRIMARY KEY AUTOINCREMENT, textbook_name , email text, price text, description text, department text, course text, date text)'''
		c.execute(query)
		conn.commit()

def Insert_Textbook(seller):

	conn = lite.connect(datebase)
	now = dt.datetime.now()
	date = str(now.year) + '/' + str(now.month) + '/' + str(now.day)

	data = [seller['textbook_title'],seller['email'] , seller['price'] ,seller['textbook_description'] , seller['textbook_department'],seller['course'], date]
	data = [str(i) for i in data]
	with conn:
		c = conn.cursor()
        c.executemany('INSERT INTO TextBookPosts(textbook_name , email , price , description , department , course , date) VALUES(?,?,?,?,?,?,?)',(data,))
        conn.commit()


def Get_Textbooks():
	conn = lite.connect(datebase)
	with conn:
		c = conn.cursor()
        c.execute('SELECT * FROM TextBookPosts')
        textbooks = c.fetchall()
        return [textbook for textbook in textbooks[::-1]]


def Get_Textbook(ID):
	conn = lite.connect(datebase)
	with conn:
		c = conn.cursor()
        c.execute('SELECT * FROM TextBookPosts WHERE ID = ' + str(ID))
        textbooks = c.fetchone()
        return textbooks


def Destroy_Table():
	conn = lite.connect(datebase)

	with conn:
		c = conn.cursor()
		query = '''DROP TABLE TextBookPosts'''
		c.execute(query)
		conn.commit()

