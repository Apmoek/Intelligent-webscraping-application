# === Config ===
$EmailFrom    = "your_email@gmail.com"
$EmailTo      = "your_email@gmail.com"
$Subject      = "📬 PowerShell Test Email (Gmail SMTP)"
$Body         = "Hello! This is a test email sent from PowerShell via Gmail SMTP."

# App password from https://myaccount.google.com/apppasswords
$AppPassword  = "your_app_password_here"

# SMTP Settings
$SmtpServer   = "smtp.gmail.com"
$SmtpPort     = 587

# Convert app password to a secure string
$SecurePass = ConvertTo-SecureString $AppPassword -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($EmailFrom, $SecurePass)

# Send the email
try {
    Send-MailMessage -From $EmailFrom -To $EmailTo -Subject $Subject -Body $Body -SmtpServer $SmtpServer -Port $SmtpPort -UseSsl -Credential $Credential
    Write-Host "✅ Email sent successfully!"
}
catch {
    Write-Host "❌ Failed to send email:`n$($_.Exception.Message)"
}
