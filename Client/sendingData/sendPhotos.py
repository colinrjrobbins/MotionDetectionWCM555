from paramiko import SSHClient
from scp import SCPClient
import subprocess as sp

def sendFiles():
    passwordFile = open("password.txt","r")
    passwordSave = passwordFile.read()
    password = passwordSave.replace("\n","")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname='192.168.0.26', username="pi", password=password)

    scp = SCPClient(ssh.get_transport())

    scp.put('images', recursive=True, remote_path='/home/pi/Pictures/')

    scp.close()

    sp.call(["sudo","rm","-r","images"])
    sp.call(["mkdir","images"])

    print("SSH Complete")