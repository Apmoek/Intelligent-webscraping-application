# === Laad een bestand met wachtwoorden en settings. ===
. "C:\Projects\CryptoMonitor\Intelligent-webscraping-application\AppPassword.ps1"

# === Config ===
$EmailFrom    = $AppSendingGmail
$EmailTo      = $AppReceivingGmail
$Subject      = "PowerShell Test Email (Gmail SMTP)"
$Body         = "Hello! This is a test email sent from PowerShell via Gmail SMTP."

# App password van https://myaccount.google.com/apppasswords
$AppPassword  = $AppPasswordGmail

# SMTP instellingen
$SmtpServer   = "smtp.gmail.com"
$SmtpPort     = 587

# Het wachtwoord wordt omgezet naar een secure stukje tekst.
$SecurePass = ConvertTo-SecureString $AppPassword -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($EmailFrom, $SecurePass)

# Verstuur de email.
try {
    Send-MailMessage -From $EmailFrom -To $EmailTo -Subject $Subject -Body $Body -SmtpServer $SmtpServer -Port $SmtpPort -UseSsl -Credential $Credential
    Write-Host "✅ Email sent successfully!"
}
catch {
    Write-Host "❌ Failed to send email:`n$($_.Exception.Message)"
}
