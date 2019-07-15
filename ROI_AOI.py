import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import math

Centers_of_mass = np.array([[],[]])

for filename in glob.glob(r'C:\Users\Beni\Documents\Ximea cam Python\ROI_supp_imgs\*.tif', recursive=True):
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
    
    cv2.imshow("Image", ROI)
    cv2.waitKey(0)
    
print(cX, cY)
#cv2.destroyAllWindows()

print(Centers_of_mass)
print(Centers_of_mass.shape)

print(Centers_of_mass[1])



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
