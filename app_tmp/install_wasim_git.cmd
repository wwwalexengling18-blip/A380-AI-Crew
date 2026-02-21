@echo off
cd /d %~dp0

echo Installiere WASimCommander von GitHub...
py -3.12 -m pip install git+https://github.com/mpaperno/WASimCommander.git

echo Fertig
pause
