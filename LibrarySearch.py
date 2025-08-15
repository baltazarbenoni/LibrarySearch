from pathlib import Path
import os
import re

class Main:

#DOWNLOADS FOLDER ORGANIZING
    h = Path.home()
    source = Path(h / "Desktop" / "Livres")
    foundFiles = list()

    def fileSearch(self, key):
        contents = os.listdir(self.source)
        if(contents.count == 0):
            print("The library folder is empty!\nCannot conduct search")
            return
        else:
            for x in contents:
                if (os.path.isfile(Path(self.source / x)) == False):
                    continue
                else:
                    self.checkFile(x, key)

    def checkFile(self, item, key):
        regex = "(" + key + ")$"
        result = re.search(regex, item)
        #IF FILE MATCHES SEARCH, ADD IT TO LIST
        if(result != None):
            self.foundFiles.append(item)
            #IF ONLY ONE FILE FOUND, OPEN FILE?
            #OR OPEN FILE RIGHT AWAY?

#INIT APP
print("Welcome to your library search app!")
instance = Main()
key = input("Type what you want to search from your library")
if(key == 'or'):
    instance.organizefiles()



