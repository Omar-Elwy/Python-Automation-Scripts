# Module for talking to other APPs from Python
import requests

# Module for sending emails
import smtplib

# Module that provide OS dependent functionality
# so we use it to get us environment variables
import os

# Allows us to do SSH connections
import paramiko
# Linode library
import linode_api4

# Module to add sleep time
import time

import schedule

# UpperCase (best practice) because they are constant variables
# whose value cant be changed by the program
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')
# 28a2aa6d3ba3678f5cc67465b8ec475a8cc0c7ea11324cb85a2720b7f6b6bebc


def restart_server_and_container():
    # restart linode server
    print('Rebooting the server...')
    # Linode client will make it available for python to connect to linode
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    # load() fun can be used to connect to any resource in Linode
    nginx_server = client.load(linode_api4.Instance, 51111281)
    nginx_server.reboot()

    # restart the application
    while True:
        # iterate and check everytime if the server finished loading up and running
        nginx_server = client.load(linode_api4.Instance, 51111281)
        if nginx_server.status == 'running':
            # Give it 5 more seconds just to be 100% sure that the server is running
            # and ready to restart the container
            time.sleep(5)
            restart_container()
            break


def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()

    # That when we type 'yes' when connecting to the server for the first time..
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='194.233.175.87', username='root', key_filename='/home/omar3lwy/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start bc649bab30d1')

    # We used readline because this is a file and we want to read its contents..
    print(stdout.readlines())
    ssh.close()



def send_notification(email_msg):
    print('Sending an email...')

    ''' Configure that we want to use gmail platform
   "with" is part of python syntax that is used in exception handling 
   and clean up code to make it more cleaner
   -used with external or unmanged resources
   -so here if any problem happened with the login or anything
   this will clean up all the resources for us in the background
   '''
    # Connect python to our gmail address
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # Encrypt the communication from python to our mail
        smtp.starttls()
        # identefy python with our mail on this encrybted communication
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)



def monitor_application():
    try:
        response = requests.get('http://li1388-236.members.linode.com:8080/')
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application Down. Fix it!')
            msg = f'Application returned {response.status_code}'
           # send_notification(msg)
            restart_container()
            # Exception is a python object that represents an error
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = 'Application not accessible at all'
       # send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()

