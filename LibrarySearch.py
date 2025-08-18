from pathlib import Path
import os
import webbrowser
import re

import subprocess
import platform

class Main:

#DOWNLOADS FOLDER ORGANIZING
    h = Path.home()
    source = Path(h / "Desktop" / "Livres")
    foundFiles = list()
    searchKey = ""

    def fileSearch(self):
        self.newSearch()
        contents = os.listdir(self.source)
        if(len(contents) == 0):
            print("The library folder is empty!\nCannot conduct search")
            return
        else:
            amount = str(len(contents))
            print("\nSearching the pattern " + self.searchKey + "\nFrom " + amount + " files.\n")
            for x in contents:
                if (os.path.isfile(Path(self.source / x)) == False):
                    continue
                else:
                    self.checkFile(x, self.searchKey)

    def checkFile(self, item, key):
        regex = "(" + key + ")"
        result = re.search(regex, item, re.IGNORECASE)
        #IF FILE MATCHES SEARCH, ADD IT TO LIST
        if(result != None):
            self.foundFiles.append(item)
    
    def printResults(self):
        if(len(self.foundFiles) == 0):
            return False
        for x in self.foundFiles:
            a = str(self.foundFiles.index(x))
            print(a + ": " + x + "\n")
        return True
    
    def openFile(self, input):
        a = int(input)
        file = self.foundFiles[a]
        path = Path(self.source / file)
        print("opening file: " + str(path))
        #WORKS ONLY IF FILE IS IN PDF-FORMAT.
        try:
            webbrowser.open_new(path)
        except:
            print("Failed to open file!")

    def checkInput(self, input):
        #CHECK IF VALUE IS INT
        try:
            val = int(input)
            if(val < 0):
                print("Given index less than zero, try again.\n")
                return 0
            elif(val >= len(self.foundFiles)):
                print("Given index exceeds the amount of results. Try again\n")
                return 0
            else:
                return 2 
        except ValueError:
            #Input not an integer. Conducting a new search with given variable.
            return 1 

    def newSearch(self):
        self.foundFiles.clear() 


#DEFINE A FUNCTION TO CLEAR THE TERMINAL
def clearTerminal():
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

#INIT APP
print("Welcome to your library search app!\n")
instance = Main()
#GET THE FIRST PROMPT
key = input("Type what you want to search from your library\n")
instance.searchKey = key
#RUN THIS LOOP WHILE APP IS ACTIVE
active = True
while active: 
    #QUIT THE APP.
    if(instance.searchKey == "q"):
        clearTerminal()
        break
    #FIRST FILE SEARCH
    instance.fileSearch()
    clearTerminal()
    found = instance.printResults()
    if(not found):
        clearTerminal()
        key = input("No files found! Enter a new search!\n")
        instance.searchKey = key
        continue
    #THE FILES FOUND ARE PRINTED. ASK IF USER WANTS TO OPEN ONE OF THEM.
    print("If you wish to open one of the files, enter its index to open it.\nElse, conduct a new search by typing something else.\n")
    #VARIABLE 'NEXTPROCESS' INDICATES WHETHER NEXT PROCESS IS SELECTED.
    # 0 MEANS NOT SELECTED OR INCORRECT INPUT
    # 1 MEANS STRING --> CONDUCT A NEW SEARCH WITH GIVEN PROMPT.
    # 2 MEANS INTEGER --> OPEN FILE WITH GIVEN INDEX
    nextProcess = 0 
    index = 0
    #RUN THIS LOOP WHILE NEXT PROCESS IS NOT SELECTED.
    while nextProcess < 1:
        userInput = input()
        nextProcess = instance.checkInput(userInput)
        index = userInput
    #CONTINUE TO NEW SEARCH.
    if(nextProcess < 2):
        print("User input: " + index)
        instance.searchKey = index
    #OPEN THE FILE
    elif(nextProcess < 3):
        instance.openFile(index)
        active = False
    clearTerminal()
print("See you next time!")
