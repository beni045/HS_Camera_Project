import time
from ximea import xiapi
import numpy as np
import PIL.Image
import os
import cv2
import matplotlib.pyplot as plt
import glob
import math

#set path where images will be saved
os.chdir('C:\\Users\\n.gerdes\\Documents\\HSCam_PythonApi\\Trial_Files\\Imgs')

#create instance for first connected camera
cam = xiapi.Camera()

#start communication
#to open specific device, use:
#cam.open_device_by_SN('41305651')
#(open by serial number)
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
cam.set_width(1000)
cam.set_height(400)
cam.set_offsetX(700)
cam.set_offsetY(400)
"""

start_time = time.time()


for x in range(10):
    #get data and pass them from camera to img
    cam.get_image(img)

    #get raw data from camera
    #for Python2.x function returns string
    #for Python3.x function returns bytes
    data_raw = img.get_image_data_numpy()

   
    #print(type(data_raw))
    #transform data to list
    #data = list(data_raw)
    #start_time = time.time()
    max_val = np.amax(data_raw)
    #print("--- %f seconds ---" % (time.time() - start_time))
    #print("--- Max val =%f ---" % (max_val))
    f= open("10Images_%d" % (x),"w+b")
    f.write(data_raw)
    f.close()
    

    #print(type(data_raw))
    #print image data and metadata
    """print('Image number: ' + str(i))
    print('Image width (pixels):  ' + str(img.width))
    print('Image height (pixels): ' + str(img.height))
    print('First 10 pixels: ' + str(data[:10]))
    print('\n')"""

    
print("--- %f seconds ---" % (time.time() - start_time))
#print("--- Max val =%f ---" % (max_val))

#print(type(data_raw))






#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()




#stop communication
cam.close_device()


print(type(data_raw))
img = PIL.Image.fromarray(data_raw, 'L')
img.show()




Centers_of_mass = np.array([[],[]])

for filename in glob.glob(r'C:\Users\n.gerdes\Documents\HSCam_PythonApi\Trial_Files\Imgs\*', recursive=True):
    current_img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    
    # convert the grayscale image to binary image
    ret,thresh = cv2.threshold(current_img,127,255,0)
 
    # calculate moments of binary image
    M = cv2.moments(thresh)
 
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    Centers_of_mass = np.append(Centers_of_mass, ([cX],[cY]),axis=1)
    ROI = current_img[cY - 100:cY + 100,cX - 100:cX + 100]
    
#    cv2.imshow("Image", ROI)
#    cv2.waitKey(0)
    
#print(cX, cY)
#cv2.destroyAllWindows()

print(Centers_of_mass)
#print(Centers_of_mass.shape)

#print(Centers_of_mass[1])



Pre_width = (np.amax(Centers_of_mass[0])+100) - (np.amin(Centers_of_mass[0]-100))
Pre_height = (np.amax(Centers_of_mass[1])+100) - (np.amin(Centers_of_mass[1])-100)

print(Pre_width)
print(Pre_height)

Width = (round(Pre_width / 100))*100
Height = (round(Pre_height / 100))*100

print(Width)
print(Height)

Pre_X_offset = round(np.amin(Centers_of_mass[0]-100)/100)*100

print(Pre_X_offset)

Pre_Y_offset = round(np.amin(Centers_of_mass[1]-100)/100)*100

print(Pre_Y_offset)










print('Done.')

