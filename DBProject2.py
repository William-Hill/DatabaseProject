'''
Created on Nov 09, 2012

-author: william
and Marlon
'''
import MySQLdb
import random
import os

#For tunnel
#ssh wmh80@pluto.cse.msstate.edu -L 3306:localhost:3306 
#random.choice
db = MySQLdb.connect('127.0.0.1', 'wmh80', 'ab1234', 'wmh80')

cursor = db.cursor()

print "Please make a selection from the list:"
print "1: Add a book:"
print "2: Find Candidate Textbooks"
print "3: Select Textbooks (for single section or all sections)"
print "4: Find Book Violations"
selection = raw_input()

#selection = raw_input("Would you like to enter a book?\n")

if selection == '1':
    print "Please enter an ISBN number:"
    ISBN = raw_input()
    print "Please enter a title: "
    title = raw_input()
    print "Please enter the price of the book: "
    price = raw_input()
    print "Please enter the edition number of the book: "
    edition = raw_input()
    print "Does this book have online support: "
    oSupport = raw_input()
    print "Is there a free copy of this book available: "
    free = raw_input()
    cursor.execute("INSERT INTO Book(ISBN,Title) VALUES(%s, %s) ", (ISBN, title))
    #print "book selected"
elif selection == '2':
    #print "Please enter the classID: "
    print "Please enter the classID: "
    classID = raw_input()
    #bISBN = raw_input()
    
    output =  "SELECT b.Title From Book b, Section s WHERE  s.ClassID = '%s' AND s.ISBN = b.ISBN " %(classID)
    #print output
    cursor.execute (output)
    #cursor.execute("SELECT b.Title From Book AS b JOIN Use AS u ON u.ISBN = b.ISBN AND u.ISBN = %s", (bISBN))
    print cursor.fetchall()
elif selection =='3':
    print "Please enter a classID: "
    classID = raw_input()
    print "Please enter a semester (format- yyyycc; y = year; cc - Semester code; 10 - Spring; 20 - Summer; Fall - 30): "
    term = raw_input()
    print "Please enter the title of the book: "
    bookTitle = raw_input()
    check = "UPDATE SET s.ISBN = b.ISBN FROM Book b, Section s WHERE s.ClassID = '%s' AND s.Term = '%s' AND b.Title = '%s' " %(classID,term,bookTitle)
    print check
    cursor.execute("UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.ClassID = '%s' AND s.Term = '%s' AND b.Title = '%s' " %(classID,term,bookTitle))

else:
    print "Invalid selection. "

    

    



#cursor.execute('describe Book')
#cursor.execute("INSERT INTO Book(ISBN,Title) VALUES('13523251', 'C Programming 2') ")
#cursor.execute("INSERT INTO Book(Title) VALUES('Algorithms')")
#cursor.execute("INSERT INTO Book(Title) VALUES('New book') ")

#cursor.execute("SELECT * FROM Book")
db.commit()
#cursor.execute('describe Book')
#print "This is a test"
#name = raw_input()
#print "Hi," , name

#print cursor.fetchall()
#rows = cursor.fetchall()

#for row in rows:
    #print row
    
