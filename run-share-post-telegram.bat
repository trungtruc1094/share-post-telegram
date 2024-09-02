@echo off

:: Kill any running Chrome processes
taskkill /F /IM chrome.exe /T

:: Kill any running ChromeDriver processes
taskkill /F /IM chromedriver.exe /T

set PYTHONPATH=%PYTHONPATH%;C:\Users\trung\Documents\share-post-telegram
cd C:\Users\trung\Documents\share-post-telegram
python share-post-telegram.py
pause

