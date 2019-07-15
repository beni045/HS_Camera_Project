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

#create a folder for Session
Sessions_folder = "C:\\Users\\Beni\\Documents\\Ximea cam Python\\Testing_Makedirs\\Sessions"
print(Sessions_folder)
os.chdir("%s" %(Sessions_folder))
d = datetime.datetime.today()    
Date_sesh = d.strftime('%d-%m-%Y')
Current_session_folder = ("Session_%s_%s" %(Date_sesh,Session_ID))
if not os.path.exists('%s' %(Current_session_folder)):
       os.makedirs('%s' %(Current_session_folder))


#initialize variable for following block
Session_description_modify = "Not"

while (Session_description_modify != ""):
    #prompt for session info
    Session_description = input("Enter Session description (press enter to skip): ")
    #insert code to create txt file with session description here
    
    #show user the info so far and ask to confirm or modify
    #create the session folder with a txt file inside, which contains the session ID and description.
    print("\nSession description: %s" %(Session_description))
    Session_description_modify = input("Session_ID: %s \n\nPress enter to confirm, type anything to modify:" %(Session_ID))
    if (Session_description_modify == ""):
        os.chdir("%s" %(Current_session_folder))
        f = open("Session_description.txt" , "w+")
        f.write("Session_ID:%s\n\nSession_description: %s" %(Session_ID,Session_description))
        f.close()
        
        
#variable initialization for the following block
Dataset_num_counter = 1
Check_if_more = "NotDone"
Edit_or_not = ""
 
#Prompt user for datasets info input
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
 
    #write the dataset that was just entered into the Index.csv file
    if(Edit_or_not == ""):        
        d = datetime.datetime.today()    
        Date = d.strftime('%d-%m-%Y')
        Dataset_ID = uuid.uuid4()
        list = [Power, Speed, Layer_thickness, Num_Layers, Dataset_ID,Session_ID, Date ]
        os.chdir("%s" %(Sessions_folder))
        with open('Index.csv' , 'a', newline = '') as f:
            writer = csv.writer(f)   
            writer.writerow(list)
            
        #Make folder for dataset
        #make the description text file for the dataset
        os.chdir("%s\\%s" %(Sessions_folder,Current_session_folder))
        Current_dataset_folder = ("Dataset_%s_%s-%s-%s_%s" %(Dataset_num_counter-1,Power,Speed,Layer_thickness,Dataset_ID))
        if not os.path.exists('%s' %(Current_dataset_folder)):
            os.makedirs('%s' %(Current_dataset_folder))
            os.chdir("%s\\%s\\%s" %(Sessions_folder,Current_session_folder,Current_dataset_folder))
            f = open("Dataset_description.txt" , "w+")
            f.write("Dataset_ID:%s\n\nDataset_description: %s" %(Dataset_ID,Dataset_description))
            f.close()
            
            #Create a folder for every layer within the dataset                  
            for i in range(1,int(Num_Layers)+1):
                os.makedirs('Layer_%s' %(i)) 
                i+=1
       
        #Prompt for another dataset or if done with all datasets    
        Check_if_more = input("Type 'Done', or press enter for next Dataset: ")


#exit the new directories to avoid external bugs
os.chdir("%s" %(Sessions_folder))





        

       
       