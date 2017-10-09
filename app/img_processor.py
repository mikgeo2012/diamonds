import cv2, shutil, os
from PIL import Image
import pytesseract
import argparse


import matplotlib as mpl
mpl.use('TkAgg')

from pylab import array, plot, show, axis, arange, figure, uint8

imgs = ["cert1.jpg", "cert2.jpg", "cert3.jpg", "cert4.jpg"]
certs = ["cert.jpg", "certt.jpg"]



def _isolateCertNum(filename):

    try:

        image = cv2.imread("images/original/" + filename)


        cropped = image[67:100, 550:700]

        # cv2.imwrite("gia_certCROPPED.jpg", cropped)

        # # Image data
        # image2 = cv2.imread('gia_certCROPPED.jpg',0) # load as 1-channel 8bit grayscale


        # maxIntensity = 255.0 # depends on dtype of image data


        # x = arange(maxIntensity)

        # # Parameters for manipulating image data
        # phi = 1
        # theta = 1

        # # newImage1 = (maxIntensity/phi)*(image2/(maxIntensity/theta))**2
        # # newImage1 = array(newImage1,dtype=uint8)

        # newImage0 = (maxIntensity/phi)*(image2/(maxIntensity/theta))**2.5
        # newImage0 = array(newImage0,dtype=uint8)




        # # cv2.imshow('newImage1',newImage1)
        # # cv2.imwrite("gia_certBW.jpg", newImage1)

        r = 1600.0 / cropped.shape[1]
        dim = (1600, int(cropped.shape[0] * r))

        # perform the actual resizing of the newImage0 and show it
        resized = cv2.resize(cropped, dim, interpolation = cv2.INTER_AREA)

        # Mat imageMat = new Mat();
        # Utils.bitmapToMat(resized, imageMat);
        # Imgproc.cvtColor(imageMat, imageMat, Imgproc.COLOR_BGR2GRAY);
        # Imgproc.GaussianBlur(imageMat, imageMat, new Size(3, 3), 0);
        # Imgproc.threshold(imageMat, imageMat, 0, 255, Imgproc.THRESH_OTSU);

        # ret,thresh1 = cv2.threshold(resized,127,255,cv2.THRESH_BINARY)

        blur = cv2.GaussianBlur(resized,(11,11),0)

        cv2.imwrite("images/processed/" + filename, blur)

    except IOError as e:
        print(e)
        raise
    except Exception as ex:
        print(ex)
        raise
    else:
        os.remove("images/original/" + filename)


def _getGIANum(filename):
    imgPath = "images/processed/"
    try:
        text = pytesseract.image_to_string(Image.open(imgPath + filename))
    except Exception as e:
        print("Tesseract now working")
        print(e)
        raise
    else:
        os.remove(imgPath + filename)
        return text

def analyze(filename):
    try:
        _isolateCertNum(filename)
        text = _getGIANum(filename)
    except Exception as e:
        print(e)
        raise
    else:
        return text








