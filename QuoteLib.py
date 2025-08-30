from pathlib import Path
import sqlite3
import os
import re
import subprocess
import platform

h = Path.home()
lib = Path(h / "Desktop" / "Livres" / "QuoteDatabase.db")
searchKey = ""
con = sqlite3.connect(lib)
cur = con.cursor()
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

#def remove(id):

def insert(quote, author, keywords = None):
    #keywords = lambda keywords: "None" if keywords is None else str(keywords) 
    if(keywords == None):
        row = (str(quote), str(author)) 
        cur.execute("INSERT INTO Library(Quote, Author) VALUES(?, ?)", row)
    else:
        row = (str(quote), str(author), str(keywords)) 
        cur.execute("INSERT INTO Library(Quote, Author, Keywords) VALUES(?, ?, ?)", row)
    con.commit()

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

def printRow(id):
    sql = "SELECT * FROM Library WHERE Id = '%i'" % int(id)
    res = cur.execute(sql)
    row = res.fetchone()
    print(row)
    print("\n")

def printAll():
    sql = "SELECT * FROM Library" 
    res = cur.execute(sql)
    rows = res.fetchall()
    for x in rows:
        print(x)
        print("\n")

def search(quote = None, author = None, keywords = None):
    searched = False
    cond = ""
    if(quote is not None and author is not None):
        cond1 = "Quote='" + str(quote) + "' AND "
        cond2 = "Author='" + str(author) + "'"
        cond = cond1 + cond2
    elif(quote is not None):
        cond = "Quote='" + str(quote) + "'"
    elif(author is not None):
        cond = "Author='" + str(author) + "'"
    else:
        return

    string = "SELECT FROM Library WHERE " + cond
    result = cur.execute(string)
    searched = True
    searchres = result.fetchall()
    for x in searchres:
        print(x + "\n")

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

print("Welcome to quote manager and storage!\n")
x = input()
activation = True
while activation:
    clearTerminal()
    print("Select the operation you wish to perform: \n")
    print("1 = add new quote\n")
    print("2 = search quotes\n")
    print("3 = remove or edit existing quote\n")
    print("4 = show library contents\n")
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
        continue
    elif(operation == "4"):
        clearTerminal()
        printAll()
        cont = input()
        if(cont == "q"):
            break
    elif(operation == "q"):
        break
    else:
        print("Your input matches no operation. Try again.")
        cont = input()
        continue

con.close()
print("See you later!")
#con.commit()
#We can verify that the data was inserted correctly by executing a SELECT que