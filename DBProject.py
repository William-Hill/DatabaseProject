'''
Created on Sep 28, 2012

@author: william
'''
import MySQLdb
import random

#For tunnel
#ssh wmh80@pluto.cse.msstate.edu -L 3306:localhost:3306 
#random.choice
db = MySQLdb.connect('127.0.0.1', 'wmh80', 'ab1234', 'wmh80')

cursor = db.cursor()

#cursor.execute('describe Book')
cursor.execute("INSERT INTO Book(ISBN,Title) VALUES('2352325', 'C Programming') ")
#cursor.execute("INSERT INTO Book(Title) VALUES('Algorithms')")
#cursor.execute("INSERT INTO Book(Title) VALUES('New book') ")

cursor.execute("SELECT * FROM Book")
db.commit()
#print "This is a test"
#name = raw_input()
#print "Hi," , name

print cursor.fetchall()
#rows = cursor.fetchall()

#for row in rows:
    #print row
    