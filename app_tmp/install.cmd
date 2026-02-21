@echo off
cd /d %~dp0

echo Installiere Module...
python -m pip install SimConnect
python -m pip install wasimcommander
python -m pip install pyyaml

echo Fertig
pause
