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

def insert(quote, author, keywords = None):
    keywords = lambda keywords: "None" if keywords is None else str(keywords) 
    row = (str(quote), str(author), keywords) 
    cur.execute("INSERT INTO Library VALUES", row)
    con.commit()

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
    return result.fetchall()

def getFromTable(column, key):
    col = ""
    col = str(col).upper()
    if(col == "QUOTE" or column == 1):
        col = "Quote" 
    elif(col == "AUTHOR" or column == 2):
        col = "Author" 
    elif(col == 3):
        col = "Keywords"
    string = "SELECT FROM Library WHERE " + col + "='" + str(key) + "'" 
    result = cur.execute(string, key)
    return result.fetchall()

print("Welcome to quote manager and storage!\n")
getEntryInput()

#con.commit()
#We can verify that the data was inserted correctly by executing a SELECT que