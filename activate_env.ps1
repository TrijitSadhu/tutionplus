# Auto-activate Python virtual environment and load .env
$WorkspaceRoot = "c:\Users\newwe\Desktop\tution\tutionplus"
$VenvPath = Join-Path $WorkspaceRoot "env\Scripts\Activate.ps1"
$EnvFile = Join-Path $WorkspaceRoot "django\django_project\genai\.env"

# Activate virtual environment
if (Test-Path $VenvPath) {
    & $VenvPath
    Write-Host "[+] Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "[-] Virtual environment not found at $VenvPath" -ForegroundColor Red
}

# Load .env file variables
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -notmatch '^\s*#' -and $_ -notmatch '^\s*$') {
            $key, $value = $_ -split '=', 2
            if ($key -and $value) {
                [System.Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim(), "Process")
            }
        }
    }
    Write-Host "[+] Environment variables loaded from .env" -ForegroundColor Green
} else {
    Write-Host "[-] .env file not found at $EnvFile" -ForegroundColor Red
}

# Set working directory
Set-Location $WorkspaceRoot
Write-Host "[+] Working directory: $WorkspaceRoot" -ForegroundColor Green
