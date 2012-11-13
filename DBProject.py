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
cursor2 = db.cursor()

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
        print "15: Show Class Table"
        print "16: Show Book Table"
        print "17: Show Professor Table"
        selection = raw_input()

        if selection == '1':
            req1()
        elif selection == '2':
            req2()
        elif selection =='3':
            req3()    
        elif selection == '4':
            req4()
        elif selection == '5':
            req5()
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
        #elif selection == '14':
            #print "All Book Titles: \n {}".format(BookTitles())
        elif selection == '15':
            req15()
        elif selection == '16':
            req16()
        elif selection == '17':
            req17()
        db.commit()
        

def req1():    #1.    Add a book
    
    print "Please enter an ISBN number (9 digits):"
    ISBN = raw_input()
    while(len(ISBN) !=9):
        ISBN = raw_input("Please enter a valid (9 digit) ISBN")
        
    print "Please enter a title: "
    title = raw_input()
    
    print "Please enter the price of the book: "
    price = raw_input()
    while(not(price.isdigit())):
        price = raw_input("Please enter a valid value for price:")
        
    print "Please enter the edition number of the book: "
    edition = raw_input()
    print "Does this book have online support (Y for yes, N for no): "
    oSupport = raw_input()
    while(oSupport not in ('Y','y','N','n')):
        oSupport = raw_input("Please enter a valid value (Y or N): Does this book have online support?")
        
    print "Is there a free copy of this book available(Y for yes, N for no): "
    free = raw_input()
    while (free not in ('Y','y','N','n')):
        free = raw_input("Please enter a valid value (Y or N): Is there a free copy of this book available?")
        
    check = "INSERT INTO Book(ISBN,Title,Price,Edition,Online_Support,Free_Copy) VALUES(%s,'%s',%s,'%s','%s','%s') " %(ISBN,title,price,edition,oSupport,free)
    #print check
    cursor.execute("INSERT INTO Book(ISBN,Title,Price,Edition,Online_Support,Free_Copy) VALUES(%s,'%s',%s,'%s','%s','%s') " %(ISBN,title,price,edition,oSupport,free)) 
    #db.commit()
    
def req2():     #2:  Find Candidate Textbooks
    
    #Test - passed
    print "Please enter the classID: "
    print "Valid Class ClassIDs: \n {}".format(ClassIDs())
    classID = raw_input()
    while(classID not in ClassIDs()):
        classID = raw_input("Enter a VALID ClassID: ")
            
    output =  "SELECT b.Title From Book b, Section s WHERE  s.ClassID = '%s' AND s.ISBN = b.ISBN " %(classID)
    #print output
    cursor.execute (output)
    #db.commit()
    print cursor.fetchall()
    
def req3():     #3:  Select Textbooks (for all sections)
    
    print "Valid Class ClassIDs: \n {}".format(ClassIDs())
    print "Please enter a classID: "
    classID = raw_input()
    while(classID not in ClassIDs()):
        classID = raw_input("Enter a VALID ClassID: ")
        
    print "Please enter a semester (format- yyyyss; y = year; ss - Semester code; 10 - Spring; 20 - Summer; Fall - 30): "
    term = raw_input()
    while ((not(term.isdigit())) or (len(term) != 6) or (term[-2:] not in ('10','20','30'))):
        term = raw_input("Please enter a valid term:")
    
    print "All Book Titles: \n {}".format(BookTitles())    
    print "Please enter the title of the book: "
    bookTitle = raw_input()
    while(bookTitle not in BookTitles()):
        bookTitle = raw_input("Please enter a valid book title:")
    
    check = "UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.ClassID = '%s' AND s.Term = '%s' AND b.Title = '%s' " %(classID,term,bookTitle)
    #print check
    cursor.execute("UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.ClassID = '%s' AND s.Term = '%s' AND b.Title = '%s' " %(classID,term,bookTitle))
    #db.commit()
    
def req4():     #4:  Select Textbooks (for a single section)
   
    print "Valid Section CRNs: \n {}".format(CRNs())
    print "Please enter a CRN: "
    CRN = raw_input()
    while(CRN not in CRNs()):
        CRN = raw_input("Please enter a valid CRN:")

    
    
    print "All Book Titles: \n {}".format(BookTitles())  
    print "Please enter the title of the book: "
    bookTitle = raw_input()
    while(bookTitle not in BookTitles()):
        bookTitle = raw_input("Please enter a valid book title:")
    
    check = "UPDATE Section s, Book b SET s.ISBN = b.ISBN WHERE s.CRN = '%s' AND b.Title = '%s' " %(CRN,bookTitle)
    #print check
    cursor.execute(check)
    #db.commit()
    
def req5():     #5:  Find Book Violations
    
    print "Please enter a semester (format- yyyyss; y = year; ss - Semester code; 10 - Spring; 20 - Summer;  30 - Fall): "
    term = raw_input()
    while ((not(term.isdigit())) or (len(term) != 6) or (term[-2:] not in ('10','20','30'))):
        term = raw_input("Please enter a valid term:")
    #tested and working; need to run a few more test cases.
    check = "SELECT * FROM Choose C, Section S WHERE S.Term = '%s' AND S.ISBN != C.ISBN AND ((SUBSTRING(S.Term, 1,4) - SUBSTRING(C.Term,1,4))< 3 OR (SUBSTRING(S.Term, 1,4) - SUBSTRING(C.Term,1,4) = 3 AND SUBSTRING(S.Term, 5,2) - SUBSTRING(C.Term,5,2) < 0)) AND S.ClassID = C.ClassID " %(term)
    #print check
    cursor.execute(check)
    #db.commit()
    #Need to change print statement to give more details
    print cursor.fetchall()
    
         
        

def req6():
    '''
    U-6 Query by bookstore to retrieve all textbook selections for a specified semester
    SELECT * FROM `Choose` AS p JOIN Book AS b 
    ON (p.ISBN = b.ISBN AND p.Term = 200710)
    '''
    pass
    semester = raw_input ('Given Semester: ')
    query = "SELECT DISTINCT(Title) FROM `Choose` AS p JOIN Book AS b ON (p.ISBN = b.ISBN AND p.Term = {})".format(semester)
    #print query
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

        while (netid not in NetIDs()):
            raw_input("Enter a VALID NetID: ")

        cursor.execute("SELECT * FROM Section WHERE CRN = %s" %(crn))
        print cursor.fetchall()
        #query = "UPDATE `Section` SET `NetID` = '{}' WHERE `CRN` = {}".format(netid,crn)
        query = "UPDATE `Section` SET `NetID` = '%s' WHERE `CRN` = %s" %(netid,crn)
        #print query
        cursor.execute(query)
        cursor.execute("SELECT * FROM Section WHERE CRN = %s" %(crn))
        print cursor.fetchall()

    elif option in ('I','i'):
        #print "Valid Section CRNs: \n {}".format(CRNs())
        #crn = raw_input("Enter a CRN: ")

        #while(crn not in CRNs()):
        #    crn = raw_input("Enter a VALID CRN: ")
        #
        print "Valid Class ClassIDs: \n {}".format(ClassIDs())
        classID = raw_input("Enter a ClassID: ")

        while(classID not in ClassIDs()):
            classID = raw_input("Enter a VALID ClassID: ")

        print "Valid Terms:\n 1) Must be six digits(0-9)\n 2) Last 2 digits must be 01, 02, or 03"
        term = raw_input("Enter a Term: ")

        while ((not(term.isdigit())) or (len(term) != 6) or (term[-2:] not in ('10','20','30'))):
            print "isdigit: {}\nlen: {}\n[-2:] {}".format(not(term.isdigit()),len(term) != 6,term[-2:] not in ('01','02','03'))
            term = raw_input("Enter six digit Term that  \nends in 01, 02, or 03: ")
        print "isdigit: {}\nlen: {}\n[-2:] {}".format(not(term.isdigit()),len(term) != 6,term[-2:] not in ('01','02','03'))

        print "Valid Professor NetIDs: \n {}".format(NetIDs())
        netid = raw_input("Enter a NetID (or leave BLANK): ")

        while (netid.strip() != '' and netid not in NetIDs()):
            netid = raw_input("Enter a VALID NetID (or leave BLANK): ")

        if netid == '':
            netid = 'NULL'
        else:
            netid = repr(netid)

        print "Valid Book ISBNs: \n {}".format(ISBNs())
        isbn = raw_input("Enter a ISBN (or leave BLANK): ")

        while (isbn.strip() != '' and isbn not in ISBNs()):
            isbn = raw_input("Enter a VALID ISBN (or leave BLANK): ")

        if isbn == '':
            isbn = 'NULL'
        else:
            isbn = repr(isbn)

        query = "INSERT INTO `Section` (`CRN`, `ClassID`, `Term`, `NetID`, `ISBN`) VALUES (NULL, '{}', '{}', {}, {})".format(classID,term,netid,isbn)
        #print query
        cursor.execute(query)

def req8():
    '''
    G-2 Query to retrieve all current textbooks for sections taught by a specified professor in a specified semester
    SELECT * FROM `Section` WHERE NetID = 'uih4' AND Term = 200930
    SELECT DISTINCT(Title) FROM `Section` AS s JOIN Book AS b ON(s.ISBN = b.ISBN) WHERE NetID = 'hs3' AND s.Term = 200730
    '''
    pass

    print "Valid Professor NetIDs: \n {}".format(NetIDs())
    netid = raw_input('Enter a NetID: ')

    while (netid not in NetIDs()):
        raw_input("Enter a VALID NetID: ")

    print "Valid Terms:\n 1) Must be six digits(0-9)\n 2) Last 2 digits must be 01, 02, or 03"
    term = raw_input("Enter a Term: ")

    while ((not(term.isdigit())) or (len(term) != 6) or (term[-2:] not in ('10','20','30'))):
        print "isdigit: {}\nlen: {}\n[-2:] {}".format(not(term.isdigit()),len(term) != 6,term[-2:] not in ('01','02','03'))
        term = raw_input("Enter six digit Term that  \nends in 01, 02, or 03: ")
    print "isdigit: {}\nlen: {}\n[-2:] {}".format(not(term.isdigit()),len(term) != 6,term[-2:] not in ('01','02','03'))



    query = "SELECT DISTINCT(Title) FROM `Section` AS s JOIN Book AS b ON(s.ISBN = b.ISBN) WHERE NetID = '{}' AND s.Term = {}".format(netid,term)
    #print query
    cursor.execute(query)

    for count, book in enumerate([item[0] for item in cursor.fetchall()]):
        print count+1, repr(book)

def req9():
    '''
    G-3 Bulk input of attributes of books from a file
    '''
    pass

    filename = raw_input("filename: ")

    query = "LOAD DATA LOCAL INFILE '%s' INTO TABLE `Book` FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\r\n'"%(os.getcwd()+'/'+filename)
    print(query)
    cursor.execute(query)

def req10():
    '''
    G-4 Bulk input from a file of a specified semester's courses/sections and teaching assignments
    '''
    pass
    
    filename = raw_input("filename: ")

    query = "LOAD DATA LOCAL INFILE '%s' INTO TABLE `Section` FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\r\n'"%(os.getcwd()+'/'+filename)
    print(query)
    cursor.execute(query)

def req11():
    '''
    G-5 Set the default textbook to be the same as the last time the course was 
    taught for all textbooks with no textbook selection for a specified semester
    '''
    pass

    # get term
    term = validTerm()

    # get CRNs, ClassIDs from given term
    query = "SELECT CRN, ClassID FROM `Section` where ISBN IS NULL AND term = {} ".format(term)
    ##print query
    cursor.execute(query)

    bookless = cursor.fetchall()

    for section in bookless:
        print section, section[0], section[1]
        query = "SELECT isbn, crn FROM `Section` where term = (Select Max(term) From Section where term < {0} AND ClassID in ('{1}')) AND ClassID in ('{1}')".format(term,section[1])
        ##print query
        cursor.execute(query)

        lastbook = [book for book in cursor.fetchall()]

        print len(lastbook)
        if len(lastbook) != 0:
            print lastbook, lastbook[0]
        
            if lastbook[0] is None:
                isbn = 'NULL'
            else:
                isbn = repr(lastbook[0][0])
        else:
            isbn = 'NULL'

        query = "UPDATE `Section` SET `ISBN` = {0} WHERE `CRN` = {1};".format(isbn,section[0])
        #print '\t',query
        cursor.execute(query)

def req15():        #15: Show Class Table
    check = "SELECT * FROM Class"
    print check
    cursor.execute(check)
    print "ClassID        Title"
    for item in cursor.fetchall():
        print repr(item).rjust(10)
        
    #print cursor.fetchall()
    
   
    #db.commit()
    
def req16():        #16: Show Book Table
    check = "SELECT * FROM Book"
    #columns = "show columns FROM Book"
    #print columns
    print check
    #cursor2.execute(columns)
    cursor.execute(check)
    #for item in cursor2.fetchall():
        #print repr(item).rjust(10)
    for item in cursor.fetchall():
        print repr(item).rjust(10)
    #print cursor.fetchall()
    
def req17():        #Show Professor Table
    check = "SELECT * FROM Professor"
    print check
    cursor.execute(check)
    for item in cursor.fetchall():
        print repr(item).rjust(10)




def validTerm():
    print "Valid Terms:\n 1) Must be six digits(0-9)\n 2) Last 2 digits must be 01, 02, or 03"
    term = raw_input("Enter a Term: ")

    while ((not(term.isdigit())) or (len(term) != 6) or (term[-2:] not in ('10','20','30'))):
        print "isdigit: {}\nlen: {}\n[-2:] {}".format(not(term.isdigit()),len(term) != 6,term[-2:] not in ('01','02','03'))
        term = raw_input("Enter six digit Term that  \nends in 01, 02, or 03: ")
    #print "isdigit: {}\nlen: {}\n[-2:] {}".format(not(term.isdigit()),len(term) != 6,term[-2:] not in ('01','02','03'))

    return term

def ClassIDs():
    # get valid ClassIDs
    cursor.execute('SELECT ClassID FROM `Class`')
    pkid = [str(id[0]) for id in cursor.fetchall()]
    pkid.sort()
    return pkid

def CRNs():
    # get valid CRNs
    cursor.execute('SELECT CRN FROM `Section`')
    pkid = [str(id[0]) for id in cursor.fetchall()]
    pkid.sort()
    return pkid

def NetIDs():
    # get valid NetIDs
    cursor.execute('SELECT NetID FROM `Professor`')
    pkid = [str(id[0]) for id in cursor.fetchall()]
    pkid.sort()
    return pkid
    
def ISBNs():
    # get valid ISBNs
    cursor.execute('SELECT ISBN FROM `Book`')
    pkid = [str(id[0]) for id in cursor.fetchall()]
    pkid.sort()
    return pkid
def BookTitles():
    cursor.execute('SELECT Title FROM `Book`')
    pkid = [str(id[0]) for id in cursor.fetchall()]
    pkid.sort()
    return pkid

menu()