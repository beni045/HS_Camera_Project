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
num_frames = 200
pid = PID(2, 1, 0, setpoint=100, sample_time = None)
exposure_times = np.array([])
max_vals = np.array([])
#set path where images will be saved
os.chdir(r'C:\\Users\\n.gerdes\\Documents\\HSCam_PythonApi\\Trial_Files\\Imgs')
new_exp = 100


#create instance for first connected camera
cam = xiapi.Camera()
print('Opening first camera...')
cam.open_device()
print(cam.get_exposure_increment())

#settings
cam.set_imgdataformat('XI_RAW8')
cam.set_exposure(new_exp)
print('Exposure was set to %i us' %cam.get_exposure())


#create instance of Image to store image data and metadata
img = xiapi.Image()


#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()


#for timing the frame loop
start_time = time.time()


for x in range(num_frames):
    
    #get data and pass them from camera to img
    cam.get_image(img)
    data_raw_nda = img.get_image_data_numpy()
    
    
    #exposure time PID
    max_val = np.amax(data_raw_nda)
    max_vals = np.append(max_vals, ([max_val]),axis=0)                   
    output = pid(max_val)
    new_exp = new_exp + output
    new_exp = (round(new_exp / 5))*5
    new_exp = int(new_exp)
    if (new_exp < 50000 and new_exp > 0):            
            cam.set_exposure(new_exp)
    exposure_times = np.append(exposure_times, ([new_exp]),axis=0)    
#    exposure_times = np.append(exposure_times, ([output]),axis=0)
#    max_vals = np.append(max_vals, ([max_val]),axis=0)
#for timing the frame loop
print("--- %f seconds ---" % (time.time() - start_time))

#new_exposure = output
#obtain new frame with ROI applied
cam.get_image(img)
data_raw_nda = img.get_image_data_numpy()


#stop camera
cam.stop_acquisition()
cam.close_device()


#testing seaborn heatmap
print(max_vals)
print(exposure_times)
#print(int(new_exposure))
print(max_val)
sb.heatmap(data_raw_nda)
plt.show()



