"""
db_backup.py 
Used to backup all of the data in the current database, make schema changes, and then reinput data
"""

import sqlite3 as lite

def getName():
	"""
	get current db version and then update it 
	"""
	
	f = open('database_version.txt', 'r')
	version = f.read()
	f = open('database_version.txt', 'w')
	f.close()
	db_name = 'reviews' + str(version) + '.sqlite'
	# update version
	version = int(version)
	version += 1
	f.write(str(version))
	f.close()
	return db_name

db_name = 'reviews.sqlite'

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
	data = [] 
	conn = lite.connect(db_name)
	with conn:
		c = conn.cursor()
		for i in xrange(table_number): # get schema of each table
			sql = 'SELECT * FROM ' + str(tables[i]) 
			c.execute(sql)
			data.append(c.fetchall())
	print data
