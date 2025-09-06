from pathlib import Path
import sqlite3
import os
import re
import subprocess
import platform

h = Path.home()
lib = Path(h / "Desktop" / "Livres" / "QuoteDatabase.db")
exists = os.path.exists(lib)

if(exists is False):
    lib = Path(h / "Desktop" / "QuoteData")
    os.mkdir(lib)

connection= sqlite3.connect(lib)
cur = connection.cursor()
result = cur.execute("SELECT name FROM sqlite_master WHERE name='Library'")
foundIndexes = list()
print(result.fetchone())

def clearTerminal():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def getEntryInput():
    print("Type the quote you want to enter: \n")
    quote = ""
    while quote == "":
        quote = input() 
        if(quote == ""):
            print("Invalid input, you must enter the quote")
    print("Type the author of the quote: \n")
    author = ""
    while author == "":
        author = input() 
        if(author == ""):
            print("Invalid input, you must enter the author")
    print("Type the keywords:")
    keywords = input()
    insert(quote, author, keywords)

def insert(quote, author, keywords = None):
    #keywords = lambda keywords: "None" if keywords is None else str(keywords) 
    if(keywords == None):
        row = (str(quote), str(author)) 
        cur.execute("INSERT INTO Library(Quote, Author) VALUES(?, ?)", row)
    else:
        row = (str(quote), str(author), str(keywords)) 
        cur.execute("INSERT INTO Library(Quote, Author, Keywords) VALUES(?, ?, ?)", row)
    connection.commit()

def generalSearch(key):
    foundIndexes.clear() 
    if(key is not None):
        regex = "(" + key + ")"
        #GET THE ROWS (IDS) WHICH MATCH THE SEARCH
        for row in cur.execute("SELECT Id, Author, Quote, Keywords FROM Library"):
            for a in range(1, 4):
                item = str(row[a])
                if(item == None):
                    continue
                result = re.search(regex, item, re.IGNORECASE)
                if(result != None):
                    foundIndexes.append(row[0])
                    break
        clearTerminal()
        for x in foundIndexes:
            printRow(x)

def remove(index):
    #ccreatePoubelle()
    #copy = "INSERT INTO Poubelle SELECT * FROM Library WHERE Id Id = '%i'" % int(index)
    #cur.execute(copy)
    cur.execute("DELETE FROM Library WHERE Id = '%i'" % int(index))
    print("Entry deleted!")
    connection.commit()

def createPoubelle():
    sql = "SELECT * FROM sqlite_master WHERE name = 'Poubelle'"
    cur.execute(sql)
    result = cur.fetchone()
    if(result):
        return
    else:
        create_table = "CREATE TABLE Poubelle AS (SELECT TOP 0 * FROM Library)" 
        cur.execute(create_table)
        return

def printRow(id):
    sql = "SELECT * FROM Library WHERE Id = '%i'" % int(id)
    res = cur.execute(sql)
    row = res.fetchone()
    print(row)
    print("\n")

def getRow(id):
    sql = "SELECT * FROM Library WHERE Id = '%i'" % int(id)
    res = cur.execute(sql)
    row = res.fetchone()
    return row

def printAll():
    sql = "SELECT * FROM Library" 
    res = cur.execute(sql)
    rows = res.fetchall()
    for x in rows:
        print(x)
        print("\n")

def getFromTable(column, key):
    col = ""
    col = str(col).upper()
    if(col == "QUOTE" or column == 1):
        col = "Quote" 
    elif(col == "AUTHOR" or column == 2):
        col = "Author" 
    elif(col == 3):
        col = "Keywords"
    string = "SELECT FROM Library WHERE " + col + "(?)" 
    result = cur.execute(string, key)
    return result.fetchall()

def quitUpdate():
    clearTerminal()
    print("Press enter to continue to main menu.")

def update():
    id = None
    while id is None:
        printAll()
        print("Here are all library contents, enter the number of the entry you wish to update. Press 'q' to exit.")
        id = input()
        try:
            id = int(id)
            row = getRow(id)
            if(row is None):
                clearTerminal()
                print("Invalid input! Try again.")
                x = input()
                id = None
                continue
        except:
            if(id == "q"):
                quitUpdate()
                return
            print("Invalid input, try again!")
            id = None
            clearTerminal()
            continue

        clearTerminal()
        print("So you wish to update the quote: \n")
        printRow(id)
        ok = input("Press any key to continue. Press 'q' if you want to change a different entry.\nPress 'Q' if you want to exit\n")
        if(ok == "q"):
            id = None
        elif(ok == "Q"):
            quitUpdate()
            return
        clearTerminal()
        print("\nNow enter which column you want to change:")

    column = ""
    while column == "":
        column = input()
        if(column.upper() == "QUOTE"):
            column = "Quote"
        elif(column.upper() == "AUTHOR"):
            column = "Author"
        elif(column.upper() == "KEYWORDS"):
            column = "Keywords"
        elif(column.upper() == "Q"):
            quitUpdate()
            return
        else:
            print("Invalid input, try again!")
            column = ""
            continue

        clearTerminal()
        print("So you wish to change the column %s from the quote \n" % column)
        printRow(id)
        ok = input("Press any key to continue. Press 'q' if you want to change a different column.")
        if(ok == "q"):
            column = ""
        else:
            clearTerminal()
        
    ok = "q"
    while ok == "q":
        print("Enter the value you wish to update the cell with:")
        val = input()
        print("The value you entered is: %s " % val)
        ok = input("Press any key to continue. Press 'q' if you want to enter a different value.")
    clearTerminal()
    updateRow(id, column, val)

def updateRow(id, column, value):
    sql = "UPDATE Library SET " + column + " = '%s' WHERE Id = '%i'" % (value, id)
    cur.execute(sql)
    connection.commit()
    print("Updated row is now: \n")
    printRow(id)

#PROGRAM EXECUTION
print("Welcome to quote manager and storage!\n")
x = input()
activation = True
while activation:
    clearTerminal()
    print("Select the operation you wish to perform: \n")
    print("1 = add new quote\n")
    print("2 = search quotes\n")
    print("3 = edit an existing entry\n")
    print("4 = show library contents\n")
    print("5 = remove an entry\n")
    print("q = exit application\n")
    operation = input()
    if(operation == "1"):
        getEntryInput()
    elif(operation == "2"):
        clearTerminal()
        key = input("Enter the search you wish to conduct:\n")
        generalSearch(key)
        cont = input()
        if(cont == "q"):
            break
    elif(operation == "3"):
        clearTerminal()
        update()
        cont = input()
        if(cont == "q"):
            break
    elif(operation == "4"):
        clearTerminal()
        printAll()
        cont = input()
        if(cont == "q"):
            break
    elif(operation == "5"):
        ind = 0
        while (ind == 0):
            clearTerminal()
            printAll()
            ind = input("Enter the index of the entry you want to remove!\n")
            try:
                ind = int(ind)
                remove(ind)
            except:
                if(ind == "q"):
                    break
                print("Invalid input, try again!")
                ind == 0
    elif(operation == "q"):
        break
    else:
        print("Your input matches no operation. Try again.")
        cont = input()
        continue

connection.close()
print("See you later!")