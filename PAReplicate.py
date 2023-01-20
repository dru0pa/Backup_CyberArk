# Welcome to our script that automates the execution of CyberArk PAReplicate.exe and emails the log file PAReplicate.log, 
# which has been zipped and password protected.
# This script was developed with the help of OpenAI.
#
# This script is designed to make the process of running PAReplicate.exe and managing the log files as efficient and secure as possible.
# The script will execute the PAReplicate.exe and create a log file named PAReplicate.log. 
# This log file will be zipped and password protected for added security. 
# Once the script has completed, an email will be sent to the specified recipient with the zipped, password-protected log file as an attachment.
#
# Before running the script, please ensure that you have the necessary dependencies installed, such as Python and the required libraries. 
# You will also need to have access to the PAReplicate.exe file, the email credentials and the email address of the recipient to whom the log file will be sent.
#
# The script is well commented and easy to understand, so it can be easily modified to suit your specific needs.
#
# Update the pathe to the file location from C drive to the appropriate location
#
# Update the SMTP variable accordingly as well as uncomment the #server.starttls()
#
# To run the script, simply navigate to the script directory in the command prompt and run the command: python PAReplicate.py
# Make sure to place the following files in the script directory: BackupUser.cred, BackupUser.cred.entropy, Vault.ini and Vault.ini
# Thank you for using our script, and please feel free to reach out to us if you have any questions or need any assistance.
#
import subprocess
import os
import datetime
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set the SMTP server variable
SMTP_SERVER = "192.168.10.1"
sender_email = "cyberark@cyberark.lan"
sender_password = "Password@4"
receiver_email = "cyberark@cyberark.lan"
subject = "CyberArk Backup"

# Set the password variable
password = "password"

# Get current day of the week
day_of_week = datetime.datetime.today().weekday()
# Command to execute
if day_of_week != 6:
    #print("Running Other")
    command = "C:\PROGRA~2\PrivateArk\Replicate\PAReplicate.exe  C:\PROGRA~2\PrivateArk\Replicate\Vault.ini /LogonFromFile C:\PROGRA~2\PrivateArk\Replicate\BackupUser.cred"
# Command to execute
else:
    #print("Running Sunday")
    command = "C:\PROGRA~2\PrivateArk\Replicate\PAReplicate.exe C:\PROGRA~2\PrivateArk\Replicate\Vault.ini /LogonFromFile C:\PROGRA~2\PrivateArk\Replicate\BackupUser.cred /FullBackup"

# Execute the command
subprocess.call(command)

# Copy data from PAReplicate.log to the main file C:\PROGRA~2\PrivateArk\Replicate\PAReplicate.log
with open("PAReplicate.log", "r") as f1, open("C:\PROGRA~2\PrivateArk\Replicate\PAReplicate.log", "a") as f2:
    f2.write(f1.read())

# Checking for Errors in the log file to name Subject accordingly
with open("PAReplicate.log", "r") as f:
    log = f.read()
    if "Error" in log:
        Subject = "CyberArk Backup Finished with Errors"
    else:
        Subject = "CyberArk Backup Finished Successfully"
# Email details
body = "Please find the attached Zip file with the password protected file  called PAReplicate.log."

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = Subject
msg.attach(MIMEText(body, "plain"))

# Password-protect and zip the PAReplicate.log file
os.system("7za a PAReplicate.zip -pPassword@5 PAReplicate.log")

# Get the current date and time
now = datetime.datetime.now()

# Format the date and time as a string
date_string = now.strftime("%Y-%m-%d %H-%M-%S")

# Print the date and time
#print("Current date and time:", date_string)

# Create the new file name
existing_file_name = "PAReplicate.zip"
new_file_name = "{}_{}.zip".format(existing_file_name.split(".")[0],date_string)

# Rename the existing file
os.rename(existing_file_name, new_file_name)

#print("File renamed to:", new_file_name)

# Open and attach the zip file
with open(new_file_name, "rb") as f:
    part = MIMEApplication(f.read(), Name=new_file_name)
    part.add_header('Content-Disposition', 'attachment', filename=new_file_name)
    msg.attach(part)

# Send the email
server = smtplib.SMTP(SMTP_SERVER)
#server.starttls()
server.login(sender_email, sender_password)
server.sendmail(sender_email, receiver_email, msg.as_string())
server.quit()

#cleen up
os.remove("PAReplicate.log")
os.remove(new_file_name)
