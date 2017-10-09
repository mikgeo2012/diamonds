from matplotlib import pyplot as plt
import cv2, shutil, os
from PIL import Image
import pytesseract
import argparse
import numpy as np






from pylab import array, plot, show, axis, arange, figure, uint8


image = cv2.imread("images/cert2.jpg")

# Crops the diamond diagram
cropped = image[470:670, 455:645]

maxIntensity = 255.0 # depends on dtype of image data


x = arange(maxIntensity)

# Parameters for manipulating image data
phi = 1
theta = 1

# newImage1 = (maxIntensity/phi)*(image2/(maxIntensity/theta))**2
# newImage1 = array(newImage1,dtype=uint8)

newImage0 = (maxIntensity/phi)*(cropped/(maxIntensity/theta))**2.5
newImage0 = array(newImage0,dtype=uint8)

r = 1600.0 / newImage0.shape[1]
dim = (1600, int(newImage0.shape[0] * r))

# perform the actual resizing of the newImage0 and show it
resized = cv2.resize(newImage0, dim, interpolation = cv2.INTER_AREA)



blur = cv2.GaussianBlur(resized,(11,11),0)


edges = cv2.Canny(blur,100,200)

plt.subplot(121),plt.imshow(blur,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

# cv2.imwrite("images/cert222.jpg", blur)
