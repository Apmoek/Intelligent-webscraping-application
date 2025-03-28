# Load configuration from JSON
$configPath = Join-Path -Path $PSScriptRoot -ChildPath "email_config.json"
$config = Get-Content -Raw -Path $configPath | ConvertFrom-Json

# Convert password to secure string
$SecurePass = ConvertTo-SecureString $config.AppPassword -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($config.EmailFrom, $SecurePass)

# Compose and send email
try {
    Send-MailMessage -From $config.EmailFrom `
                     -To $config.EmailTo `
                     -Subject "📬 PowerShell Test Email (Gmail SMTP)" `
                     -Body "Hello! This is a test email sent via config-based PowerShell script." `
                     -SmtpServer $config.SmtpServer `
                     -Port $config.SmtpPort `
                     -UseSsl `
                     -Credential $Credential

    Write-Host "✅ Email sent successfully!"
}
catch {
    Write-Host "❌ Failed to send email:`n$($_.Exception.Message)"
}