# main_lite.py

# Execute using the launcher or command line!

"""
reference a banlist.csv, and swipe cards. After each cardswipe, a color coded
responce will be displayed. Finally, once the program is instructed to close,
a report will be generated.
"""
# imports
import csv
import pip
from os.path import exists
from os import getlogin, system
from datetime import datetime
try:
    from colorama import init
except ModuleNotFoundError:
    if hasattr(pip, 'main'):
        pip.main(['install', 'colorama'])
    else:
        pip._internal.main(['install', 'colorama'])
    from colorama import init
try:
    from termcolor import colored
except ModuleNotFoundError:
    if hasattr(pip, 'main'):
        pip.main(['install', 'termcolor'])
    else:
        pip._internal.main(['install', 'termcolor'])
    from termcolor import colored

# Party Name
name = input("Please input party name: ")
valid = False
while not valid:
    confirm = input("If '{name}' is correct, please type 'CONFIRM', otherwise enter corrected name: ".format(name=name))
    if confirm == "CONFIRM":
        valid = True
    else:
        name = confirm

# populate bannedIDs from banlist.csv
# .csv files can be written and modified in Excel
bannedIDs = []
if exists('banlist.csv'):
    with open('banlist.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        csvreader.__next__()
        for row in csvreader:
            bannedIDs.append(row[0])
else:
    with open('banlist.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["ID", "Name", "Notes"])
bannedIDsOG = bannedIDs.copy()

# begin log
log = open(name+".log", "w")

# main loop
print("All set! To end the party, type 'DONE'\nTo ban someone mid party, type 'BAN' without hitting enter then swipe their ID.")
enteredIDs = []
inpt = input("> ")
log.write("Party name: {name}\n\nLog started at: {datetime}\nLog started by: {user}\n\n".format(name=name,  datetime=str(datetime.now().strftime('%H:%M:%S')), user=getlogin()))
while inpt != "DONE":
    if inpt[0:3] == "BAN" and len(inpt) > 23:      # Ban someone mid party
        ID = inpt.split(";")[-1][1:9]
        bannedIDs.append(ID)
        note = input("comments: ")
        log.write("{time}\t\tBanned\t{ID}\t{note}\n".format(time=str(datetime.now().strftime('%H:%M:%S')), ID=ID, note = note))
    else:                       # Respond to a normal swipe
        if len(inpt) == 21 and inpt[0] == ";" and inpt[-1] == "?":
            ID = inpt.split(";")[-1][1:9]
            if ID.isnumeric() and not "." in ID:    # valid swipe
                if ID in bannedIDs:
                    print(colored('Banned', 'white', 'on_red'))
                    log.write("{time}\t\tSwipe\t{ID}\trejected\n".format(time=str(datetime.now().strftime('%H:%M:%S')), ID=ID))
                elif ID in enteredIDs:
                    print(colored("Repeat", 'grey', 'on_yellow'))
                    log.write("{time}\t\tSwipe\t{ID}\trepeat\n".format(time=str(datetime.now().strftime('%H:%M:%S')), ID=ID))
                else:
                    print(colored("Welcome!", 'grey', 'on_green'))
                    log.write("{time}\t\tSwipe\t{ID}\n".format(time=str(datetime.now().strftime('%H:%M:%S')), ID=ID))
                    enteredIDs.append(ID)
            elif inpt != "DONE":
                print(colored('Invalid ID', 'white', 'on_red'))
    inpt = input("> ")

# close log
log.write("\nParty closed at {datetime}\n".format(datetime=str(datetime.now().strftime('%H:%M:%S'))))
log.write("\nPeople: {n}".format(n=str(len(enteredIDs))))
log.close()

# update banlist
n = len(bannedIDs) - len(bannedIDsOG)
with open('banlist.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for ID in bannedIDs[n-1:]:
        print(ID)
        csvwriter.writerow([ID])

# finished
print("All done, {name}.log is available and banlist.csv has been updated!".format(name=name))
