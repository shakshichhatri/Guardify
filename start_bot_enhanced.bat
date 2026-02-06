@echo off
echo ========================================
echo    GUARDIFY BOT - ENHANCED VERSION
echo    Auto-Moderation System
echo ========================================
echo.

REM Check if token is set
if not defined DISCORD_BOT_TOKEN (
    echo WARNING: DISCORD_BOT_TOKEN environment variable not set!
    echo The bot will try to use the token from config.json
    echo.
)

echo Starting Guardify Bot with enhanced abuse detection...
echo.
echo Features Active:
echo   [X] AI-Powered Abuse Detection (100+ keywords)
echo   [X] Spam Detection
echo   [X] Caps Lock Filter
echo   [X] Comprehensive Activity Logging
echo   [X] Auto-Warnings and Timeouts
echo.
echo Logs will be saved to: forensics_logs/
echo.
echo Press Ctrl+C to stop the bot
echo ========================================
echo.

D:\project\Guardify\.venv\Scripts\python.exe bot.py

pause
