import cv2
import shutil
import os
from PIL import Image
import pytesseract
import argparse
import imutils
import numpy as np

import matplotlib as mpl
mpl.use('TkAgg')

from matplotlib import pyplot as plt

from pylab import array, plot, show, axis, arange, figure, uint8




def run(img):
    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread("images/original/" + img, 0)
    img = cv2.imread("images/original/" + img)
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, h = cv2.findContours(thresh, 1, 2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        print len(approx)
        if len(approx) == 5:
            print "pentagon"
            cv2.drawContours(img, [cnt], 0, 255, -1)
        elif len(approx) == 3:
            print "triangle"
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
        elif len(approx) == 4:
            print "square"
            cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
        elif len(approx) == 9:
            print "half-circle"
            cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
        elif len(approx) > 15:
            print "circle"
            cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # resized = imutils.resize(image, width=300)
    # ratio = image.shape[0] / float(resized.shape[0])
    # ret,thresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    # cv2.imwrite("images/processed/" + img, thresh)
    # find contours in the thresholded image and initialize the
    # shape detector
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]


def isolateCertNum(filename):
    try:

        image = cv2.imread("images/original/" + filename)

        cropped = image[485:660, 465:645]

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

        r = 1000.0 / cropped.shape[1]
        dim = (1000, int(cropped.shape[0] * r))

        # perform the actual resizing of the newImage0 and show it
        resized = cv2.resize(cropped, dim, interpolation=cv2.INTER_AREA)

        # Mat imageMat = new Mat();
        # Utils.bitmapToMat(resized, imageMat);
        # Imgproc.cvtColor(imageMat, imageMat, Imgproc.COLOR_BGR2GRAY);
        # Imgproc.GaussianBlur(imageMat, imageMat, new Size(3, 3), 0);
        # Imgproc.threshold(imageMat, imageMat, 0, 255, Imgproc.THRESH_OTSU);

        # ret,thresh1 = cv2.threshold(resized,127,255,cv2.THRESH_BINARY)

        blur = cv2.GaussianBlur(resized, (11, 11), 0)

        cv2.imwrite("images/processed/" + filename, blur)
    except:
        raise

def histo(filename):
    img = cv2.imread("images/processed/" + filename, 0)
    plt.hist(img.ravel(),256,[0,256]); plt.show()


# isolateCertNum('2baa6705_a17d_11e7_aac8_60f81db7d7c0.jpg')
histo('2baa6705_a17d_11e7_aac8_60f81db7d7c0.jpg')
histo('1c171dbd_a19f_11e7_8831_60f81db7d7c0.jpg')

