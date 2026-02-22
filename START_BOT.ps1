<# 
.DESCRIPTION
    Guardify Discord Bot - PowerShell Startup Script
    
.NOTES
    Version: 2.0
    Author: Guardify Team
    Platform: Windows PowerShell
#>

param(
    [ValidateSet("run", "loop", "status", "install", "help")]
    [string]$Mode = "help"
)

function Show-Menu {
    Write-Host "`n============================================================"
    Write-Host "  🛡️  GUARDIFY DISCORD BOT - STARTUP MENU"
    Write-Host "============================================================`n"
    Write-Host "Usage: .\START_BOT.ps1 [mode]`n"
    Write-Host "Modes:"
    Write-Host "  run     - Run bot once (normal mode)"
    Write-Host "  loop    - Run bot with auto-restart on crash"
    Write-Host "  status  - Check bot status and dependencies"
    Write-Host "  install - Install/update all dependencies"
    Write-Host "  help    - Show this help message`n"
}

function Check-Python {
    try {
        $version = python --version 2>&1
        Write-Host "✅ Python found: $version"
        return $true
    }
    catch {
        Write-Host "❌ Python not found. Please install Python 3.8+"
        return $false
    }
}

function Check-Dependencies {
    Write-Host "`n📚 Checking dependencies...`n"
    
    $packages = @(
        "discord.py",
        "better-profanity",
        "fuzzywuzzy",
        "python-Levenshtein",
        "flask",
        "requests",
        "langdetect",
        "transformers",
        "textblob"
    )
    
    foreach ($package in $packages) {
        $installed = pip freeze | Select-String $package
        if ($installed) {
            Write-Host "✅ $package - Installed"
        }
        else {
            Write-Host "❌ $package - NOT installed"
        }
    }
}

function Install-Dependencies {
    Write-Host "`n📥 Installing dependencies...`n"
    pip install -r requirements.txt
    Write-Host "`n✅ Dependencies installed!`n"
}

function Run-Bot {
    Write-Host "============================================================"
    Write-Host "🚀 Starting Guardify Bot..."
    Write-Host "============================================================`n"
    python bot.py
}

function Run-BotLoop {
    Write-Host "============================================================"
    Write-Host "🚀 Starting Guardify Bot (Auto-Restart Mode)"
    Write-Host "============================================================`n"
    
    $restartCount = 0
    while ($true) {
        python bot.py
        $restartCount++
        Write-Host "`n⚠️  Bot stopped (Restart count: $restartCount). Restarting in 5 seconds...`n"
        Start-Sleep -Seconds 5
    }
}

function Show-Status {
    Write-Host "`n============================================================"
    Write-Host "📊 GUARDIFY BOT STATUS"
    Write-Host "============================================================`n"
    
    Check-Python
    Check-Dependencies
    
    if (Test-Path "bot.py") {
        Write-Host "✅ bot.py found"
    }
    else {
        Write-Host "❌ bot.py not found"
    }
    
    if (Test-Path "requirements.txt") {
        Write-Host "✅ requirements.txt found"
    }
    else {
        Write-Host "❌ requirements.txt not found"
    }
    
    Write-Host "`n============================================================`n"
}

# Main execution
switch ($Mode) {
    "run" {
        if (Check-Python) {
            Run-Bot
        }
    }
    "loop" {
        if (Check-Python) {
            Run-BotLoop
        }
    }
    "status" {
        Show-Status
    }
    "install" {
        Install-Dependencies
    }
    default {
        Show-Menu
    }
}

Write-Host "`nPress Enter to continue..."
Read-Host
