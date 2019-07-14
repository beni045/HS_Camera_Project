import time
import numpy as np
import PIL.Image
import os
import uuid
import sys


#print (sys.argv)




print("Hello")






Session_ID = uuid.uuid4()

#print (sys.argv)

Session_description = input("Enter Session description (press enter to skip): ")

print("\nSession description: %s" %(Session_description))
print("Session_ID: %s \n\nPress enter to confirm." %(Session_ID))



Dataset_num_counter = 1
Check_if_more = "NotDone"
Edit_or_not = ""
# taking three inputs at a time 

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
        Check_if_more = input("Type 'Done', or press enter for next Dataset: ")

    







