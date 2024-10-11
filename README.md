# CyberArk PAReplicate Automation Script

This Python script automates the execution of CyberArk's `PAReplicate.exe` utility and securely emails the log file (`PAReplicate.log`) as a zipped and password-protected attachment.

## Description

This script streamlines the process of running CyberArk backups using `PAReplicate.exe` and ensures the secure handling of log files. It performs the following actions:

1. **Executes PAReplicate.exe:** Runs the `PAReplicate.exe` utility with specified configurations for backups.
2. **Manages Log Files:**  Handles the `PAReplicate.log` file, including moving and appending content to maintain a history of backups.
3. **Zips and Password-Protects:** Compresses the log file into a ZIP archive and protects it with a password for security.
4. **Emails the Log:** Sends an email with the zipped log file as an attachment to a designated recipient.

## Prerequisites

* **Python 3.12.x:** This script is compatible with Python 3.12.x.
* **CyberArk 14.x:**  This script supports CyberArk version 14.x.
* **7-Zip:** You need 7-Zip installed and accessible via the command line (`7z.exe`).
* **Email Credentials:** Ensure you have the necessary email credentials (sender address, password, SMTP server details) to send the email.
* **PAReplicate.exe:**  You need access to the `PAReplicate.exe` file in your CyberArk installation directory.

## Usage

1. **Configuration:**
   * **Update Paths:** Modify the script to reflect the correct paths for your CyberArk installation and 7-Zip.
   * **SMTP Settings:**  Update the `SMTP_SERVER`, `sender_email`, `sender_password`, and `receiver_email` variables with your email configuration.
   * **Password:**  Set a strong password for the ZIP archive by replacing `"StrongPassword123!"` in the `os.system()` command.
2. **Placement:** Place the `PAReplicate-new.py` script in the `C:\Scripts` folder (or adjust the path accordingly).
3. **Execution:** Open a command prompt, navigate to the script directory, and run:

   ```bash
   python PAReplicate-new.py
