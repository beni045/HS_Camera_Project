import time
from ximea import xiapi
import numpy as np
import PIL.Image
import os
import cv2
import matplotlib.pyplot as plt
import glob
import math
from scipy import ndimage



#initialize variables
Centers_of_mass = np.array([[],[]])
num_frames = 10


#set path where images will be saved
os.chdir(r'C:\\Users\\n.gerdes\\Documents\\HSCam_PythonApi\\Trial_Files\\Imgs')


#create instance for first connected camera
cam = xiapi.Camera()
print('Opening first camera...')
cam.open_device()


#settings
cam.set_imgdataformat('XI_RAW8')
cam.set_exposure(60000)
print('Exposure was set to %i us' %cam.get_exposure())


#create instance of Image to store image data and metadata
img = xiapi.Image()


#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()


#set ROI
"""
cam.set_width(200)
cam.set_height(200)
cam.set_offsetX(900)
cam.set_offsetY(500) """


#for timing the frame loop
start_time = time.time()


for x in range(num_frames):
    #get data and pass them from camera to img
    cam.get_image(img)
    data_raw_nda = img.get_image_data_numpy()
    #calculate COM for frame array and store it in Centers_of_mass array
    CM = ndimage.measurements.center_of_mass(data_raw_nda)
    cX = CM[1]
    cY = CM[0]
    Centers_of_mass = np.append(Centers_of_mass, ([cX],[cY]),axis=1)
  


#for timing the frame loop
print("--- %f seconds ---" % (time.time() - start_time))


#to to check if COM is correct
#img = PIL.Image.fromarray(data_raw_nda, 'L')
#img.show()


#Calculate min,max valeues for both x and y centers of mass, then add 100 for an outer boundary
Pre_width = (np.amax(Centers_of_mass[0])+100) - (np.amin(Centers_of_mass[0]-100))
Pre_height = (np.amax(Centers_of_mass[1])+100) - (np.amin(Centers_of_mass[1])-100)
#correct the width and height to the nearest 100 to make it a valid parameter
Width = (round(Pre_width / 4))*4
Height = (round(Pre_height / 2))*2
#calculate requred offset and round to nearest 100
X_offset = round(np.amin(Centers_of_mass[0]-100)/4)*4
Y_offset = round(np.amin(Centers_of_mass[1]-100)/2)*2


#Convert ROI parameters to integers
Width = int(Width)
Height = int(Height)
X_offset = int(X_offset)
Y_offset = int(Y_offset)


#checking if parameters are the right type
print(type(Width))
print(type(Height))
print(type(X_offset))
print(type(Y_offset))


cam.set_width(Width)
cam.set_height(Height)
cam.set_offsetX(X_offset)
cam.set_offsetY(Y_offset)

cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()


img = PIL.Image.fromarray(data_raw_nda, 'L')
img.show()
#stop camera
cam.stop_acquisition()
cam.close_device()


"""#create instance for first connected camera
cam = xiapi.Camera()
print('Opening first camera...')
cam.open_device()


#settings
cam.set_imgdataformat('XI_RAW8')
cam.set_exposure(60000)
print('Exposure was set to %i us' %cam.get_exposure())


#create instance of Image to store image data and metadata
img = xiapi.Image()


#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()

#get a frame with new ROI    
cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()


#stop camera
cam.stop_acquisition()
cam.close_device()


#to to check if COM is correct
img = PIL.Image.fromarray(data_raw_nda, 'L')
img.show()
"""

#print summary of calibration
print("ROI calibration summary:\n\n")
print("Number of frames used: %s\n" %(num_frames))
print("Centers of mass array: %s\n" %(Centers_of_mass))
print("Calibrated Width: %s\n" %(Width))
print("Calibrated Height: %s\n" %(Height))
print("Calibrated X_offset: %s\n" %(X_offset))
print("Calibrated Y_offset: %s\n\n" %(Y_offset))
print('Done.')
