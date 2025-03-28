# Load configuration from JSON
$configPath = Join-Path -Path $PSScriptRoot -ChildPath "email_config.json"
$config = Get-Content -Raw -Path $configPath | ConvertFrom-Json

