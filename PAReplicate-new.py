# Welcome to our script that automates the execution of CyberArk PAReplicate.exe and emails the log file PAReplicate.log, 
# which has been zipped and password protected.
# This script was developed with the help of OpenAI.
#
# This script is designed to make the process of running PAReplicate.exe and managing the log files as efficient and secure as possible.
# The script will execute the PAReplicate.exe and create a log file named PAReplicate.log. 
# This log file will be zipped and password-protected for added security. 
# Once the script has been completed, an email will be sent to the specified recipient with the zipped, password-protected log file as an attachment.
#
# Before running the script, please ensure that you have the necessary dependencies installed, such as Python and 7zip. 
# You will also need to have access to the PAReplicate.exe file, the email credentials and the email address of the recipient to whom the log file will be sent.
#
# The script is well-commented and easy to understand, so it can be easily modified to suit your specific needs.
#
# Place the PAReplicate-new.py in the folder called C:\Scripts
#
# Note PROGRA~2 is the short file name for Program Files (x86)
#
# Update the path to the file location from C drive to the appropriate drive location
#
# Update the SMTP variable accordingly as well as uncomment the # Set the SMTP server variable
#
# To run the script, simply navigate to the script directory in the command prompt and run the command: python PAReplicate.py
# 
# Thank you for using our script, and please feel free to reach out to us if you have any questions or need any assistance.
#
# Support CyberArk 14.x and Pyhton 3.12.x
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
#zip_password = "StrongPassword123!" # Replace with a strong password. Working on this.

# Get current day of the week
day_of_week = datetime.datetime.today().weekday()

# Command to execute
command_base = "PAReplicate.exe"
vault_config = "Vault.ini"
backup_user_cred = "user.ini"
#temp_log = "C:\\Scripts\\PAReplicate.log"

# Function to move a file
def move_file(source, destination):
  """Moves a file from source to destination path.

  Args:
      source (str): Path to the source file.
      destination (str): Path to the destination file.
  """
  try:
    os.rename(source, destination)
    print(f"File moved successfully from {source} to {destination}")
  except OSError as e:
    print(f"Error moving file: {e}")

# Define file paths
log_file = "C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.log"
backup_log_file = "C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.Back"
final_log_file = "C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.log"

# Move the log file (using the function)
move_file(log_file, backup_log_file)

#test command
#PAReplicate.exe Vault.ini /LogonFromFile user.ini /FullBackup

# Change the current directory
# to CyberArk Replicate directory
os.chdir(r"C:\\PROGRA~2\\PrivateArk\\Replicate\\")
#If the Replicate folder is on anoythe drive coment out the line above and uncoment the like below
#os.chdir(r"E:\\PROGRA~2\\PrivateArk\\Replicate\\")

# Command to execute
if day_of_week != 6:
    #print("Running Other Days")
    command = f"{command_base} {vault_config} /LogonFromFile {backup_user_cred}"
# Command to execute
else:
    #print("Running Sunday")
    command = f"{command_base} {vault_config} /LogonFromFile {backup_user_cred} FullBackup"

# Execute the command
subprocess.call(command)

# Copy data from PAReplicate.log to the main file C:\PROGRA~2\PrivateArk\Replicate\PAReplicate.log
#with open("PAReplicate.log", "r") as f1, open("C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.log", "a") as f2:f2.write(f1.read())

#copy file to script folder
#os.chdir(r"C:\\Scripts")

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

# Password-protect and zip the PAReplicate.log file. Update password StrongPassword123! to whatever you like
os.system("C:\\PROGRA~1\\7-Zip\\7z.exe a PAReplicate.zip -pStrongPassword123! PAReplicate.log")

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

log_file = "C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.log"
backup_log_file_2 = "C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.Back"
The_final_log_file = "C:\\PROGRA~2\\PrivateArk\\Replicate\\PAReplicate.log"  # Final filename

# Append the log file content
try:
  with open(log_file, "r") as f_in, open(backup_log_file_2, "a") as f_out:
    f_out.write(f_in.read())  # Append content from source to backup
  print(f"Content appended from {log_file} to {backup_log_file_2}")
except OSError as e:
  print(f"Error appending files: {e}")

# Delete the original source file (if needed)
try:
   os.remove(log_file)
   print(f"Original file {log_file} deleted.")
except OSError as e:
   print(f"Error deleting file: {e}")


# Rename the backup file to the final log file
try:
  os.rename(backup_log_file_2, The_final_log_file)
  print(f"File renamed from {backup_log_file_2} to {The_final_log_file}")
except OSError as e:
  print(f"Error renaming file: {e}")


os.chdir(r"C:\\PROGRA~2\\PrivateArk\\Replicate\\")
# Delete old zip files

try:
  os.remove(new_file_name)
  print(f"Deleted file: {new_file_name}")
except OSError as e:
  print(f"Error deleting file: {e}")
