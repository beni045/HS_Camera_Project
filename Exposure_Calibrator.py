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
import seaborn as sb
import matplotlib
import matplotlib.pyplot as plt
from simple_pid import PID

#initialize variables
num_frames = 20
new_exposure = 100
pid = PID(1, 0.1, 0.05, setpoint=200)


#set path where images will be saved
os.chdir(r'C:\\Users\\n.gerdes\\Documents\\HSCam_PythonApi\\Trial_Files\\Imgs')


#create instance for first connected camera
cam = xiapi.Camera()
print('Opening first camera...')
cam.open_device()


#settings
cam.set_imgdataformat('XI_RAW8')
cam.set_exposure(100)
print('Exposure was set to %i us' %cam.get_exposure())


#create instance of Image to store image data and metadata
img = xiapi.Image()


#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()


#for timing the frame loop
start_time = time.time()


for 100 in range(num_frames):
    
    #get data and pass them from camera to img
    cam.get_image(img)
    data_raw_nda = img.get_image_data_numpy()
    
    
    #exposure time PID
    max_val = np.amax(data_raw_nda)
    if (max_val < 3):
        max_val = 3
    output = pid(max_val)
    if (output > 60000):
        output = 60000
    if (output < 100):
        output = 100
    cam.set_exposure(output)
    
    
#for timing the frame loop
print("--- %f seconds ---" % (time.time() - start_time))

new_exposure = output
#obtain new frame with ROI applied
cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()


#stop camera
cam.stop_acquisition()
cam.close_device()


#testing seaborn heatmap

print(new_exposure)
print(max_val)
sb.heatmap(data_raw_nda)
plt.show()


#print summary of calibration
print("ROI calibration summary:\n\n")
print("Number of frames used: %s\n" %(num_frames))
print("Centers of mass array: %s\n" %(Centers_of_mass))
print("Calibrated Width: %s\n" %(Width))
print("Calibrated Height: %s\n" %(Height))
print("Calibrated X_offset: %s\n" %(X_offset))
print("Calibrated Y_offset: %s\n\n" %(Y_offset))
print('Done.')
