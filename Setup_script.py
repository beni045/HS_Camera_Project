import time
import numpy as np
import PIL.Image
import os
import uuid
import sys
import datetime
import csv




print("Hello")


#create unique id for the session
Session_ID = uuid.uuid4()


#initialize variable for following block
Session_description_modify = "Not"

while (Session_description_modify != ""):
    #prompt for session info
    Session_description = input("Enter Session description (press enter to skip): ")
    #insert code to create txt file with session description here
    
    #show user the info so far and ask to confirm or modify    
    print("\nSession description: %s" %(Session_description))
    Session_description_modify = input("Session_ID: %s \n\nPress enter to confirm, type anything to modify:" %(Session_ID))
    

#variable initialization for the following block
Dataset_num_counter = 1
Check_if_more = "NotDone"
Edit_or_not = ""
 
#prompt user for dataset inputs and create folders, excel entries into Index.csv
while (Check_if_more != "Done" or Edit_or_not != ""):
    if(Edit_or_not != ""):
        Dataset_num_counter-=1
    Power, Speed, Layer_thickness, Num_Layers = input("Enter Parameters in this format 'Power Speed Layer_thickness Num_Layers':").split() 
    print("Dataset_%s:\n"%(Dataset_num_counter))    
    print("Power: ", Power) 
    print("Speed: ", Speed) 
    print("Layer_thickness: ", Layer_thickness) 
    print("Num_Layers: ", Num_Layers) 
    
    Dataset_description = input("Enter Dataset description (optional):")
    
    Edit_or_not = input("Press enter to continue or type anything to modify entry:") 
    
    Dataset_num_counter+=1
    
    if(Edit_or_not == ""):        
        d = datetime.datetime.today()    
        Date = d.strftime('%d-%m-%Y')
        
        list = [Power, Speed, Layer_thickness, Num_Layers, uuid.uuid4(),Session_ID, Date ]
        
        with open('Index.csv' , 'a', newline = '') as f:
            writer = csv.writer(f)   
            writer.writerow(list)
            
        Check_if_more = input("Type 'Done', or press enter for next Dataset: ")
#must add makedirs functions to create actual folders for corresponding layers and datasets!

print("list: %s" %(list))






