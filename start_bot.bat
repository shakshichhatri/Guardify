@echo off
REM ============================================================
REM  Guardify Discord Bot - Startup Script (Windows)
REM ============================================================
REM
REM  This script starts the Guardify Discord bot with auto-restart
REM  and automatic dependency installation
REM
REM ============================================================

setlocal enabledelayedexpansion

:menu
cls
echo ============================================================
echo  🛡️  GUARDIFY DISCORD BOT - STARTUP MENU
echo ============================================================
echo.
echo Choose an option:
echo.
echo 1) Run Bot (Normal Mode)
echo 2) Run Bot (Keep Running - Auto Restart)
echo 3) Check Dependencies
echo 4) Install/Update Dependencies
echo 5) Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto run_normal
if "%choice%"=="2" goto run_loop
if "%choice%"=="3" goto check_deps
if "%choice%"=="4" goto install_deps
if "%choice%"=="5" goto exit
goto menu

:run_normal
cls
echo ============================================================
echo 🚀 Starting Guardify Bot (Normal Mode)
echo ============================================================
echo.
python bot.py
pause
goto menu

:run_loop
cls
echo ============================================================
echo 🚀 Starting Guardify Bot (Auto-Restart Mode)
echo ============================================================
echo.
:restart_loop
python bot.py
echo.
echo ⚠️  Bot stopped. Restarting in 5 seconds...
timeout /t 5 /nobreak
goto restart_loop

:check_deps
cls
echo ============================================================
echo 📚 Checking Dependencies
echo ============================================================
echo.
pip freeze | find "discord.py"
pip freeze | find "better-profanity"
pip freeze | find "fuzzywuzzy"
pip freeze | find "python-Levenshtein"
echo.
pause
goto menu

:install_deps
cls
echo ============================================================
echo 📥 Installing Dependencies
echo ============================================================
echo.
pip install -r requirements.txt
echo.
echo ✅ Dependencies installed!
echo.
pause
goto menu

:exit
exit /b 0
