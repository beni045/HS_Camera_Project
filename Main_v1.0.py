import time
from ximea import xiapi
import numpy as np
import PIL.Image
import os
import cv2
import matplotlib.pyplot as plt
import math
from scipy import ndimage
import seaborn as sb
import matplotlib
from simple_pid import PID
import uuid
import sys
import datetime
import csv
import glob




#initialize variables here
    
Datasets = []
Layers = []
dataset_num=0
current_layer_num=1
roi_layer_counter = 1
data_raw_nda =0
global_off_counter=0
global_on_counter=0


def setup_folders():
    """ SET PATH OF SESSIONS FOLDER HERE"""
    global  Sessions_folder
    Sessions_folder = (r"C:\Users\n.gerdes\Documents\HSCam_PythonApi\Sessions")
    
    print("Hello")
    print("Sessions folder path: %s" %(Sessions_folder))
    print("Make sure the correct path for the Session folder is set!")
    Check_if_set = input("Press enter to continue. Type anything to terminate.")
    if (Check_if_set != ""):
        sys.exit()
    
    
    #create unique id for the session
    Session_ID = uuid.uuid4()
    
    #create a folder for Session
    os.chdir("%s" %(Sessions_folder))
    d = datetime.datetime.today()    
    Date_sesh = d.strftime('%d-%m-%Y')
    global Current_session_folder
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
            global Layers
            Layers.append(int(Num_Layers))
            os.chdir("%s" %(Sessions_folder))
            with open('Index.csv' , 'a', newline = '') as g:
                writer = csv.writer(g)   
                writer.writerow(list)
                
            #Make folder for dataset
            #make the description text file for the dataset
            os.chdir("%s\\%s" %(Sessions_folder,Current_session_folder))
            Current_dataset_folder = ("Dataset_%s_%s-%s-%s_%s" %(Dataset_num_counter-1,Power,Speed,Layer_thickness,Dataset_ID))
            if not os.path.exists('%s' %(Current_dataset_folder)):
                os.makedirs('%s' %(Current_dataset_folder))
                global Datasets
                Datasets.append(Current_dataset_folder)
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
    os.chdir(Sessions_folder)





def laser_on(on_threshold,count_threshold):
    global global_on_counter
    max_val = np.amax(data_raw_nda)
    if (max_val > on_threshold):
        global_on_counter+=1
    if (global_on_counter > count_threshold):
        global_on_counter = 0
        return 1
    else:
        return 0


def laser_off(off_threshold,count_threshold):
    global global_off_counter
    max_val = np.amax(data_raw_nda) 
    if (max_val < off_threshold):
        global_off_counter+=1
    if (global_off_counter > count_threshold):
        global_off_counter = 0
        return 1
    else:
        return 0




def breaktime():
    global data_raw_nda
    while(laser_on(5,5)==0):
        print("in breaktime")
        cam.get_image(img)
        data_raw_nda = img.get_image_data_numpy()
        max_val = np.amax(data_raw_nda)
        time.sleep(0.0001)
    
        
  



def calibrate_exposure(ce_num_frames , ce_num_layers, ce_setpoint, exp_limit):
    global new_exp
    pid = PID(1.3, 0, 0, setpoint=ce_setpoint, sample_time = None)

    ce_layer_counter = 0
    start_exposure = 80
    new_exp = start_exposure
    

    cam.set_exposure(start_exposure)

    
    for i in range(ce_num_frames):
        
        
        if (ce_layer_counter < ce_num_layers):
            
            #if (i > 10):
            """if (laser_off(200,5)==1):
                    ce_layer_counter+=1
                    print(ce_layer_counter)
                    breaktime()"""
                   
            #get data and pass them from camera to img
            cam.get_image(img)
            
            data_raw_calib = img.get_image_data_numpy()
            
            
            #exposure time PID
            max_val_calib = np.amax(data_raw_calib)       
            #max_vals = np.append(max_vals, ([max_val]),axis=0)
            if (max_val_calib > 0) :
                output = pid(max_val_calib)
                new_exp = new_exp + output
                if (new_exp < 100):
                    new_exp =100
                new_exp = (round(new_exp / 5))*5
                new_exp = int(new_exp)
                if(initial_calib_done == 1):
                    print("Set_%s - Exposure calibration: %s" %(dataset_num+1,new_exp))
                else:
                    print("Initial Exposure Calibration: %s" %(new_exp))                    
                if (new_exp < exp_limit and new_exp > 0):            
                        cam.set_exposure(new_exp)
        else:
            return

               
 
 
        
        
def calibrate_ROI(roi_num_frames , roi_num_layers,roi_extra_space):
#initialize variables
    Centers_of_mass = np.array([[],[]])
    roi_layer_counter=1
   
    for x in range(roi_num_frames):
        if (roi_layer_counter < roi_num_layers):            
            #if (x > 10):
            """while (laser_status(20,30)==1):
                roi_layer_counter+=1                   
                breaktime()"""
            #get data and pass them from camera to img
            cam.get_image(img)
            data_raw_nda = img.get_image_data_numpy()
            #calculate COM for frame array and store it in Centers_of_mass array
            CM = ndimage.measurements.center_of_mass(data_raw_nda)
            print("ROI_Calibraton - CENTER OF MASS: (X , Y): (%.d , %.d)" %(CM[1],CM[0])) 
            cX = CM[1]
            cY = CM[0]
            Centers_of_mass = np.append(Centers_of_mass, ([cX],[cY]),axis=1)
            
            
        else:            
            return     

    #Calculate min,max valeues for both x and y centers of mass, then add 100 for an outer boundary
    Pre_width = (np.amax(Centers_of_mass[0])+roi_extra_space) - (np.amin(Centers_of_mass[0]-roi_extra_space))
    Pre_height = (np.amax(Centers_of_mass[1])+roi_extra_space) - (np.amin(Centers_of_mass[1])-roi_extra_space)
    #correct the width and height to the nearest 100 to make it a valid parameter
    Width = (round(Pre_width / 4))*4
    Height = (round(Pre_height / 2))*2
    #calculate requred offset and round to nearest 100
    X_offset = round(np.amin(Centers_of_mass[0]-roi_extra_space)/4)*4
    Y_offset = round(np.amin(Centers_of_mass[1]-roi_extra_space)/2)*2
    
    
    #Convert ROI parameters to integers
    Width = int(Width)
    Height = int(Height)
    X_offset = int(X_offset)
    Y_offset = int(Y_offset)
     
    
    #set ROI
    cam.set_width(Width)
    cam.set_height(Height)
    cam.set_offsetX(X_offset)
    cam.set_offsetY(Y_offset)
    #cam.set_exposure(100)

    #print summary of calibration
    print("ROI calibration summary:\n\n")
    print("Centers of mass array: %s\n" %(Centers_of_mass))
    print("Calibrated Width: %s\n" %(Width))
    print("Calibrated Height: %s\n" %(Height))
    print("Calibrated X_offset: %s\n" %(X_offset))
    print("Calibrated Y_offset: %s\n\n" %(Y_offset))
    print('Done.')       
    




def worktime():
    global dataset_num
    global data_raw_nda
    global current_layer_num
    framecount=1
    if(current_layer_num ==1):
        calibrate_exposure(400, 3,150,60000)
        print("worktime exposure calibration done")
        cam.get_image(img)
    data_raw_nda = img.get_image_data_numpy()

    sb.heatmap(data_raw_nda)
    plt.show()
    if os.path.exists("%s\\%s\\%s\\Layer_%s" %(Sessions_folder,Current_session_folder,Datasets[dataset_num],current_layer_num)):
        os.chdir("%s\\%s\\%s\\Layer_%s" %(Sessions_folder,Current_session_folder,Datasets[dataset_num],current_layer_num))
    else:       
        cam.stop_acquisition()
        cam.close_device()          
        sys.exit()

    while(laser_off(20,30)==0):
        cam.get_image(img)
        data_raw_nda = img.get_image_data_numpy()
        #print("--- %f seconds ---" % (time.time() - start_time))
        #print("--- Max val =%f ---" % (max_val))
        f= open("%d" % (framecount),"w+b")
        f.write(data_raw_nda)
        f.close()
        print("Set_%s - Layer_%s - Frame_%s" %(dataset_num,current_layer_num,framecount))
        framecount+=1

    current_layer_num+=1
    if(current_layer_num > Layers[dataset_num]):
        dataset_num+=1
        current_layer_num=1
        if((dataset_num+1) > len(Datasets)):
            #stop camera
            cam.stop_acquisition()
            cam.close_device()          
            sys.exit()




initial_calib_done = 0

setup_folders()

print("Setup_folders done!")

cam = xiapi.Camera()
print('Opening first camera...')
cam.open_device()


#settings
cam.set_imgdataformat('XI_RAW8')
cam.set_exposure(1000)
print('Exposure was set to %i us' %cam.get_exposure())


#create instance of Image to store image data and metadata
img = xiapi.Image()


#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()

cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()


print("\nFirst image recieved, going into breaktime to wait for source to turn on:")


breaktime()


print("\n Breaktime over, starting exposure calibration")

calibrate_exposure(300 , 20, 150, 20000)

print("\n Exposure calibration done. Exposure time set: %s" %(new_exp))
initial_calib_done = 1

cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()

sb.heatmap(data_raw_nda)
plt.show()

print("Going into ROI calibation")
calibrate_ROI(200 , 2, 100)

print("ROI calbration done")

cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()

sb.heatmap(data_raw_nda)
plt.show()

print("Going into superloop")

try:
    while True:
        worktime()
except KeyboardInterrupt:
    cam.close_device()          
    sys.exit()
    
    pass




