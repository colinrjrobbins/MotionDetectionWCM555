# File Name: app.py (Server Portion)
# Class: WCM555
# Date: 2020-04-10
# Author: Colin Robbins
# Partners: Xiang Zhang, Nimalan
# Purpose: To display visually the photos taken, 
#          turn on an LED when new photos are 
#          recieved and to send an email to the user.

# FLASK IMPORTS
from flask import Flask, request
from flask import render_template

# THREADING IMPORTS TO USE WITH FLASK
from threading import Thread

# WEBHOOKS NOTIFICATION IMPORT
import requests

# RASPBERRY PI IMPORTS
import RPi.GPIO as GPIO

# GENERALIZED IMPORTS
import time
import os

# Initialization for the Flask Application
app = Flask(__name__,
            static_folder="static", 
            template_folder="templates")

# ROUTE
# Used to direct the user to the main page when the hostname is called.
@app.route("/")
def main():
    # Save the list of images into a list and send the list to the HTML document to load
    images = os.listdir(os.path.join(app.static_folder,"images"))
    return render_template('index.html', title="Recorded Photos" ,images=images)

# CLASS: checkFileSystemThread
# PARAM: Thread
# Purpose: Used to run in the background at all times and check to see if the file system containing the
#          images has had extra photos added to it through SCP connection.
class checkFileSystemThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        # create path to check for images uploaded and the changes.
        self.path_to_watch = "/home/pi/Documents/flaskServer/static/images/"
        # set the directory before by identifying what files were already existing
        self.before = dict([(f, None) for f in os.listdir(self.path_to_watch)])
        # initialize the General input and output pins for the LED
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12,GPIO.OUT)

    # Function to execute file change check and to set the LED on as well as send notification
    def run(self):
        while True:
            # wait 10 seconds inbetween each loop before checking data again.
            time.sleep(10)
            # check to see if the files have changed from the before list created in the initilization
            after = dict([(f, None) for f in os.listdir(self.path_to_watch)])
            # check to see if anything is different between before list and after list
            added = [f for f in after if not f in self.before]
            # if added has had a modification made to it
            if added: 
                # set the LED to high to notify the user
                GPIO.output(12,GPIO.HIGH)
                # send a phone notification
                requests.post('https://maker.ifttt.com/trigger/photoTaken/with/key/mFJcPs0GfZCjSl6uFLKED3PYPvbt3zrJ6zRgrDR9ZvS')
                print("Added: ", ", ".join(added))
            # set the before list to after so if changes are made in the future it will know
            self.before = after

    def stop(self):
        self.running = False

# CLASS: checkButtonPress
# PARAM: Thread
# Purpose: To keep a constant monitor on the button press and if the button is pressed to turn the LED off.
class checkButtonPress(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        # initialize the pin for the button
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # function to check if button is pressed and if so to turn off the LED
    def run(self):
        while True:
            if GPIO.input(10) == GPIO.HIGH:
                GPIO.output(12,GPIO.LOW)

    def stop(self):
        self.running = False

# Start the server
if __name__ == "__main__":
    # initialize the image system class check and start it running
    fileSystemCheck = checkFileSystemThread()
    fileSystemCheck.start()
    # initialize the button press class and start it running
    buttonPressCheck = checkButtonPress()
    buttonPressCheck.start()
    # start the server on standard open host.
    app.run(host='0.0.0.0')