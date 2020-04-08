# File Name: motion.py (Client Portion)
# Class: WCM555
# Date: 2020-04-10
# Author: Colin Robbins
# Partners: Xiang Zhang, Nimalan
# Purpose: To detect the motion, take a photo and initialize the
#          sendPhotos.py script to SCP the images to the Server
#          portion. 

# import modules 
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from signal import pause
from datetime import datetime
from sendPhotos import sendFiles
import os

# GPIO is generic set to BCM mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# initialize the GPIO for motion detection / sensor
GPIO.setup(4, GPIO.IN)

# initialize the PiCamera
camera = PiCamera()
camera.rotation = 90

# FUNCTION: take_photo
# take photo when motion is detected
def take_photo():
        # find datetime for image being taken
        currentTime = str(datetime.now())
        hold = currentTime.replace("-","")
        currentTime = hold.replace(":","")
        hold = currentTime.replace(" ","-")
        currentTime = hold[0:15]
        
        # start the camera and capture the image
        camera.start_preview()
        camera.capture('/home/pi/Documents/motionCheck/images/image_%s.jpg' % currentTime)
        camera.stop_preview()

        # display that the photo is taken
        print('Photo taken.')

        sendFiles()

        # let sensor and camera rest
        sleep(2)

# Run loop for photo checking
while True:
        # gather motion input
        motionIn = GPIO.input(4)

        # check to see if motion is detected
        if motionIn == 0:
                take_photo()
        else:
                print("Waiting...")
        # wait 10ms before checking again
        sleep(0.1)