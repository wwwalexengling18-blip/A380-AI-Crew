@echo off
cd /d %~dp0

echo Aktiviere pip in Python 3.14...
"C:\Users\wwwal\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m ensurepip --upgrade

echo Fertig
pause
