import os
import re
from glob import glob
import colorama
from colorama import Fore, Back, Style
from playsound import playsound
import time
import datetime

####################################################################################################################
#My Classes

class MyIntel:
    user        = "UNKNWON"
    body        = "UNKNOWN"
    regionsta   = "GREEN"
    
    location    = "UNKNOWN"
    ship        = "UNKNOWN"
    cynochance  = 0

####################################################################################################################
def getlog():
    #Open channel file for logs
    file_path = os.path.join(os.path.dirname(__file__),"watchlist_channel.txt")
    file = open(file_path)
    
    channel = file.readline()
    
    return channel

####################################################################################################################

def logcheck(prefix):
    latest = "log.txt"
    found = glob(rf'C:\Users\*\Documents\EVE\logs\Chatlogs\{prefix}*.txt')
    if found:
        latest = sorted(found)[-1]
    with open(rf"{latest}",encoding='utf-16-le') as file:
        lines = file.read().splitlines()
    file.close()
    #Truncating the timestamp from the string
    return lines[-1][25:]

####################################################################################################################

def parseintel(intel):
    
    intelobject = MyIntel
    
    #Parse reporter username, split from text body
    intelobject.user = intel.split('>')[0]
    #Trim blankspace from end of name
    intelobject.user = intelobject.user[:-1]
    
    #Parse intel text, split body from user
    intelobject.body = intel.split('>')[1]
    #Trim blankspace from start of body
    intelobject.body = intelobject.body[1:]
    
    intel = intelobject.body
    
    intel = str.lower(intel)
    
    #Parse intel for cyno keywords
    intelobject.cynochance = 0
    if "cyno" in intel:
        if "possible" in intel or "possibly" in intel:
            intelobject.cynochance += 50
        else:
            intelobject.cynochance += 100
            
    #Open systems file for comparison against intel string
    file_path = os.path.join(os.path.dirname(__file__),"watchlist_ships.txt")
    file = open(file_path)
    
    #Parse body for ship string
    if "spike" in intel:
        intelobject.ship = "SPIKE"
    elif "clr" in intel or "clear" in intel:
        intelobject.ship = "CLEAR"
    else:
        for x in file:
            x = x.rstrip('\n')
            if re.search(rf'\b{str.lower(x)}\b', intel):
                intelobject.ship = x
                file.close()
                break
            intelobject.ship = "UNKNOWN"
    #If a matched ship is not found
    file.close()

    #Open systems file for comparison against intel string
    file_path = os.path.join(os.path.dirname(__file__),"watchlist_systems.txt")
    file = open(file_path)
    
    #Parse body for location string
    for x in file:
        x = x.rstrip('\n')
        if re.search(rf'\b{str.lower(x)}\b', intel):
            intelobject.location = x
            file.close()
            return intelobject
    #If a matched location is not found
    file.close()
    intelobject.location = "UNKNOWN"
    return intelobject

####################################################################################################################

def output():
    #Prevent displaying the first (Last) line in the log, usually not relevent
    channel         = getlog()
    temp_message    = logcheck(channel)
    intelobject     = MyIntel
    alert_path       = os.path.join(os.path.dirname(__file__),"Alerts","Alert1.mp3")
    while 1:
        intel = logcheck(channel)
        
        if intel != temp_message:
            #Update time
            current_time = datetime.datetime.now()
            
            intelobject = parseintel(intel)
            if(intelobject.location != "UNKNOWN"):
                if intelobject.ship == "CLEAR":
                    print(f"{current_time.hour + 7:02}:{current_time.minute:02}:{current_time.second:02} >>> " + Back.GREEN + f"{intelobject.user:<25}{intelobject.location:<12}{intelobject.ship:<12}{intelobject.cynochance:03}%")
                    playsound(alert_path)
                else:
                    print(f"{current_time.hour + 7:02}:{current_time.minute:02}:{current_time.second:02} >>> " + Back.RED + f"{intelobject.user:<25}{intelobject.location:<10}{intelobject.ship:<12}{intelobject.cynochance:03}%")
                    playsound(alert_path)
            temp_message = intel
        time.sleep(.5)

####################################################################################################################
#Initial Variables

current_time = datetime.datetime.now()
colorama.init(autoreset=True)

####################################################################################################################
#PROGRAM START / Splash Screen Header

print("----------------------------------------------------------------")
print("WatchDog, Created by Harry Kashuken")
print("----------------------------------------------------------------")
print("Time         Reporter Name            System    Ship        Cyno")
print("----------------------------------------------------------------")
print(f"{current_time.hour + 7:02}:{current_time.minute:02}:{current_time.second:02} >>> SESSION STARTED")

####################################################################################################################
while 1:
    #Update Time every refresh, + 7 modifier to match EVE time
    current_time = datetime.datetime.now()
    
    #Consolidated terminal output to a seperate function for organization
    output()