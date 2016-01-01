"""
db_backup.py 
Used to backup all of the data in the current database, make schema changes, and then reinput data
"""

import sqlite3 as lite

def getName():
	f = open('database_version.txt')
	version = f.read()
	f.close()
	db_name = 'reviews' + str(version) + '.sqlite'
	return db_name

db_name = getName()

def getTables():
	conn = lite.connect(db_name)
	with conn:
		c = conn.cursor()
		sql = 'SELECT * FROM sqlite_master WHERE type="table"'
		c.execute(sql)
		x = c.fetchall()

	table_list = []
	for i in xrange(len(x)):
		table_list.append(x[i][1])

	return table_list

def table_schema():
	tables = getTables()
	table_number = len(tables)
	