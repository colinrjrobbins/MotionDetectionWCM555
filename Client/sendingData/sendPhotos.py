# File Name: sendPhotos.py (Client Portion)
# Class: WCM555
# Date: 2020-04-10
# Author: Colin Robbins
# Partners: Xiang Zhang, Nimalan
# Purpose: To transfer photos from one raspberry pi to another.

# IMPORT SSH AND SCP MODULES
from paramiko import SSHClient
from scp import SCPClient

# GENERALIZED IMPORTS
import subprocess as sp

# FUNCTION: sendFiles
# PARAM: None
# Purpose: 
def sendFiles():
    # Open the file with the password located in it and prepare for use in SSH and SCP
    passwordFile = open("password.txt","r")
    passwordSave = passwordFile.read()
    password = passwordSave.replace("\n","")

    # initialize the SSH client and connect to the other RPi
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname='192.168.0.26', username="pi", password=password)

    # initialize the SCP client to prepare to send files
    scp = SCPClient(ssh.get_transport())

    # prepare all the images to send from one Pi to the Other
    scp.put('images', recursive=True, remote_path='/home/pi/Documents/flaskServer/static/')

    # Once done close the SCP client
    scp.close()

    # Remove all images from one raspberry pi and recreate the images folder
    sp.call(["sudo","rm","-r","images"])
    sp.call(["mkdir","images"])

    # notify in console that the job has been completed.
    print("SSH Complete")