# === Load AppPassword from JSON config ===
$configPath = Join-Path -Path $PSScriptRoot -ChildPath "email_config.json"
$config = Get-Content -Raw -Path $configPath | ConvertFrom-Json
$AppPassword = $config.AppPassword

# === Hardcoded values ===
$EmailFrom    = "tfontys@gmail.com"
$EmailTo      = "vanderhorstjeffrey@gmail.com"
$Subject      = "📬 PowerShell Test Email (Gmail SMTP)"
$Body         = "Hello! This is a test email sent from PowerShell via Gmail SMTP."
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