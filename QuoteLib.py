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
searchres = list()
print(result.fetchone())

def clearTerminal():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def getEntryInput():
    print("Type the quote you want to enter: \n")
    quote = input() 
    print("Type the author of the quote: \n")
    author = input()
    print("Type the keywords:")
    keywords = input()
    insert(quote, author, keywords)

#def remove(id):

def insert(quote, author, keywords = None):
    #keywords = lambda keywords: "None" if keywords is None else str(keywords) 
    row = (str(quote), str(author)) 
    cur.execute("INSERT INTO Library(Quote, Author) VALUES(?, ?)", row)
    con.commit()

def searchAndPrint():
    for x in searchres:
        print(x + " \n")

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

def printAll():
    return 0

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
        quote = input("Enter the quote you wish to search:\n")
        author = input("Enter the author you wish to search:\n")
        searchres = search(quote, author)
##        searchAndPrint()
    elif(operation == "3"):
        continue
    elif(operation == "4"):
        printAll()
    elif(operation == "q"):
        break
    else:
        print("Your input matches no operation. Try again.")
        con = input()
        continue
print("See you later!")
#con.commit()
#We can verify that the data was inserted correctly by executing a SELECT que