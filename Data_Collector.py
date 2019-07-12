import time
from ximea import xiapi
import numpy as np
import PIL.Image
import os

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
cam.set_imgdataformat('XI_RAW16')
cam.set_exposure(2000)
print('Exposure was set to %i us' %cam.get_exposure())


#create instance of Image to store image data and metadata
img = xiapi.Image()

#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()

#set ROI
cam.set_width(1000)
cam.set_height(400)
cam.set_offsetX(700)
cam.set_offsetY(400)


start_time = time.time()


for x in range(5):
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


print('Done.')
