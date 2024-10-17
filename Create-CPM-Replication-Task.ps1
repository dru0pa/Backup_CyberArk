<#
.SYNOPSIS
    Configures a scheduled task for CyberArk Vault replication.

.DESCRIPTION
    This PowerShell script automates the creation of a scheduled task to perform CyberArk Vault replication. It includes the following steps:

    * Creates a local user account named "CyberArk-Backup" if it doesn't exist, or resets the password if it does.
    * Adds the user to the local Administrators group.
    * Creates a scheduled task named "CyberArk Vault Replication" to run PAReplicate.exe with the specified arguments.
    * Sets the task to run daily at 2:00 AM under the SYSTEM account.
    * Configures the task to run on battery power and allows multiple instances.
    * Sets the working directory for the task to "C:\Program Files (x86)\PrivateArk\Replicate".
    * Sets the registry value "disabledomaincreds" to 0 to allow domain credentials to be stored.

.PARAMETER None
    This script does not accept any parameters.

.NOTES
    Author: Andrew Price
    Created: 2024-10-17

    Manual Steps Required:
    * After running the script, manually edit the scheduled task to:
        * Set the "Start in (optional)" field to "C:\Program Files (x86)\PrivateArk\Replicate".
        * Change the user to "CyberArk-Backup" and provide the password.
        * Set "Run with highest privlages"

    Security Considerations:
    * Password Handling: In production environments, avoid hardcoding passwords or prompting for them in plain text. Use secure methods like fetching the password from a secure vault or using a credential object.
    * Least Privilege: Evaluate if the task requires the high privileges of the SYSTEM account or if it can be run under a less privileged account.
    * Error Handling: Consider adding error handling (e.g., try...catch blocks) to gracefully handle potential issues.

.EXAMPLE
    To run the script, save it as a .ps1 file (e.g., Configure-CyberArkVaultReplication.ps1) and execute it from an elevated PowerShell prompt:
    .\Configure-CyberArkVaultReplication.ps1
#>


# Prompt for the password for the CyberArk-Backup user
$password = Read-Host -Prompt "Enter the password for the CyberArk-Backup user" -AsSecureString

# Check if the user already exists
if (Get-LocalUser -Name "CyberArk-Backup") {
    echo "User 'CyberArk-Backup' already exists. Resetting password..."

    # Reset the password for the existing user (using the provided $password)
    Set-LocalUser -Name "CyberArk-Backup" -Password $password
    echo "Password reset for user 'CyberArk-Backup'."
} else {
    # Create the CyberArk-Backup user
    New-LocalUser -Name "CyberArk-Backup" -Password $password -AccountExpires ([DateTime]::MaxValue) -Description "User for CyberArk backup scheduled task" -PasswordNeverExpires | Out-Null

    echo "User 'CyberArk-Backup' created successfully."
}
# Add the CyberArk-Backup user to the local Administrators group (if not already a member)
if (!(Get-LocalGroupMember -Group "Administrators" -Member "CyberArk-Backup")) {
    Add-LocalGroupMember -Group "Administrators" -Member "CyberArk-Backup"
    echo "User 'CyberArk-Backup' added to Administrators group."
} else {
    echo "User 'CyberArk-Backup' is already a member of the Administrators group."
}

# Define the task name
$taskName = 'CyberArk Vault Replication'

# Define the action (command to run)
$action = New-ScheduledTaskAction -Execute '"C:\Program Files (x86)\PrivateArk\Replicate\PAReplicate.exe"' -Argument 'Vault.ini /LogonFromFile user.ini /FULLBACKUP'

# Define the trigger (daily at 10:00 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At 2am 

# Define the settings (options for the task)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances Parallel

# Define the principal (user context to run the task)
# Example: Using the SYSTEM account
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType S4U

# Create the scheduled task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force -Description 'Scheduled task to perform CyberArk Vault replication'

# Set the working directory
#Set-ScheduledTask -TaskName $taskName -WorkingDirectory 'C:\Program Files (x86)\PrivateArk\Replicate'

# Check the current value of disabledomaincreds
$currentValue = Get-ItemPropertyValue -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "disabledomaincreds"

# Change the value to 0 only if it's not already 0
if ($currentValue -ne 0) {
    Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "disabledomaincreds" -Value 0 -Type DWord
    echo "Registry value 'disabledomaincreds' changed to 0."
} else {
    echo "Registry value 'disabledomaincreds' is already set to 0."
}

echo "Scheduled task '$taskName' created successfully."
echo "Scheduled task still needs to add C:\Program Files (x86)\PrivateArk\Replicate to the 'Start in (Optional)'."
echo "Scheduled task Set the user to CyberArk-Backup"
echo "Scheduled task Set Run with highest privlages"
