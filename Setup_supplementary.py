import time
import numpy as np
import PIL.Image
import os
import uuid
import sys
import datetime
import csv




print("Hello")
print("Make sure the correct path for the Session folder is set!")
Check_if_set = input("Press enter to continue. Type anything to terminate.")
if (Check_if_set != ""):
    sys.exit()

#create unique id for the session
Session_ID = uuid.uuid4()

#create a folder for Session. THe format is Session_Date_Session_ID

Sesh_folder = "C:\\Users\\Beni\\Documents\\Ximea cam Python\\Testing_Makedirs\\Sessions"

print(Sesh_folder)
os.chdir("%s" %(Sesh_folder))
d = datetime.datetime.today()    
Date_sesh = d.strftime('%d-%m-%Y')
if not os.path.exists('Session_%s_%s' %(Date_sesh,Session_ID)):
       os.makedirs('Session_%s_%s' %(Date_sesh,Session_ID))
       
       
       
       