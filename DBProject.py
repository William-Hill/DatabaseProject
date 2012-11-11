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

def menu():

    # set 'selection' something other (Q,q) so it goes into the loop
    selection = 'go'

    while(selection not in ('Q','q')):

        #Need to add queries to return all CRNs, all book titles, all ClassIDs,
        print "Please make a selection from the list (or 'q' to quit):"
        print "1:  Add a book:"
        print "2:  Find Candidate Textbooks"
        print "3:  Select Textbooks (for all sections)"
        print "4:  Select Textbooks (for a single section)"
        print "5:  Find Book Violations"
        print "6:  Find all Textbook Selections (for a single semester)"
        print "7:  Assign Professor to Course Section"
        print "8:  Find Textbooks for a Professor's Section (for a single semester)"
        print "9:  Input of Book Attributes from a file"
        print "10: Input of Courses and Teaching Assignments from a file (for a single semester)"
        print "11: Set Default Textbook (for a single semester)"
        print "12: List all ClassIDs"
        print "13: List all CRNs"
        print "14: List all Book Titles"
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
            print "Please enter a semester (format- yyyyss; y = year; ss - Semester code; 10 - Spring; 20 - Summer; Fall - 30): "
            term = raw_input()
            print "Please enter the title of the book: "
            bookTitle = raw_input()
            check = "UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.ClassID = '%s' AND s.Term = '%s' AND b.Title = '%s' " %(classID,term,bookTitle)
            print check
            cursor.execute("UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.ClassID = '%s' AND s.Term = '%s' AND b.Title = '%s' " %(classID,term,bookTitle))
        elif selection == '4':
            print "Please enter a CRN: "
            CRN = raw_input()
            print "Please enter the title of the book: "
            bookTitle = raw_input()
            check = "UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.CRN = '%s' AND b.Title = '%s' " %(CRN,bookTitle)
            print check
            cursor.execute("UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.CRN = '%s' AND b.Title = '%s' " %(CRN,bookTitle))
        elif selection == '6':
            req6()
        elif selection == '7':
            req7()
        elif selection == '8':
            req8()
        elif selection == '9':
            req9()
        elif selection == '10':
            req10()
        elif selection == '11':
            req11()
        elif selection == '12':
            print "All Class ClassIDs: \n {}".format(ClassIDs())
            #print cursor.fetchall()
        elif selection == '13':
            print "All Section CRNs: \n {}".format(CRNs())
        elif selection == '14':
            print "All Book Titles: \n {}".format(BookTitles())
        
        
        

def req6():
    '''
    U-6 Query by bookstore to retrieve all textbook selections for a specified semester
    SELECT * FROM `Choose` AS p JOIN Book AS b 
    ON (p.ISBN = b.ISBN AND p.Term = 200710)
    '''
    pass
    semester = raw_input ('Given Semester: ')
    query = "SELECT DISTINCT(Title) FROM `Choose` AS p JOIN Book AS b ON (p.ISBN = b.ISBN AND p.Term = {})".format(semester)
    print query
    cursor.execute(query)

    for count, book in enumerate([item[0] for item in cursor.fetchall()]):
        print count+1, repr(book)

def req7():
    '''
    G-1 Store relationships between of professors and sections
    A.  UPDATE `wmh80`.`Section` SET `NetID` = 'bgv7' WHERE `Section`.`CRN` =42;

    B.  INSERT INTO `wmh80`.`Section` (`CRN`, `ClassID`, `Term`, `NetID`, `ISBN`) VALUES (NULL, 'CSE1284', '201230', 'ck0', NULL);
    '''
    pass

    option = raw_input('Enter U(UPDATE) or I(INSERT): ')

    while(option not in ('U','u','I','i')):
        option = raw_input('Enter U(UPDATE) or I(INSERT): ')

    if option in ('U','u'):
        print "Valid Section CRNs: \n {}".format(CRNs())
        crn = raw_input("Enter a CRN: ")

        while(crn not in CRNs()):
            raw_input("Enter a VALID CRN: ")

        print "Valid Professor NetIDs: \n {}".format(NetIDs())
        netid = raw_input('Enter a NetID: ')

        while (netid in NetIDs()):
            raw_input("Enter a VALID NetID: ")

        query = "UPDATE `wmh80`.`Section` SET `NetID` = '{}' WHERE `Section`.`CRN` ={}".format(netid,crn)
        print query
        cursor.execute(query)

    elif option in ('I','i'):
        print "Valid Section CRNs: \n {}".format(CRNs())
        crn = raw_input("Enter a CRN: ")

        while(crn not in CRNs()):
            raw_input("Enter a VALID CRN: ")

        print "Valid Class ClassIDs: \n {}".format(ClassIDs())
        classID = raw_input("Enter a ClassID: ")

        while(classID not in ClassIDs()):
            raw_input("Enter a VALID ClassID: ")

        print "Valid Terms:\n 1) Must be six digits(0-9)\n 2) Last 2 digits must be 01, 02, or 03"
        term = raw_input("Enter a Term: ")

      





def req8():
    '''
    G-2 Query to retrieve all current textbooks for sections taught by a specified professor in a specified semester
    SELECT * FROM `Section` WHERE NetID = 'uih4' AND Term = 200930
    '''
    pass




def req9():
    '''
    G-3 Bulk input of attributes of books from a file
    '''
    pass

def req10():
    '''
    G-4 Bulk input from a file of a specified semester's courses/sections and teaching assignments
    '''
    pass

def req11():
    '''
    G-5 Set the default textbook to be the same as the last time the course was 
    taught for all textbooks with no textbook selection for a specified semester
    '''
    pass

def ClassIDs():
    # get valid ClassIDs
    cursor.execute('SELECT ClassID FROM `Class`')
    return [id[0] for id in cursor.fetchall()]

def CRNs():
    # get valid CRNs
    cursor.execute('SELECT CRN FROM `Section`')
    return [id[0] for id in cursor.fetchall()]

def NetIDs():
    # get valid NetIDs
    cursor.execute('SELECT NetID FROM `Professor`')
    return [id[0] for id in cursor.fetchall()]
    
def ISBNs():
    # get valid ISBNs
    cursor.execute('SELECT ISBN FROM `Book`')
    return  [id[0] for id in cursor.fetchall()]

def BookTitles():
    cursor.execute('SELECT TITLE FROM `Book`')
    return  [id[0] for id in cursor.fetchall()]

menu()

    



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
    
