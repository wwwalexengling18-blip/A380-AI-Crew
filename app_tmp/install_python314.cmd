@echo off
cd /d %~dp0

echo Installiere Module in Python 3.14...
"C:\Users\wwwal\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install SimConnect
"C:\Users\wwwal\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install wasimcommander
"C:\Users\wwwal\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install pyyaml

echo Fertig
pause
