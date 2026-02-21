@echo off
cd /d %~dp0

echo Installiere Module in Python 3.11...
py -3.11 -m pip install SimConnect
py -3.11 -m pip install wasimcommander
py -3.11 -m pip install pyyaml

echo Fertig
pause
