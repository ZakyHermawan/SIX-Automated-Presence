@echo off
echo Starting script...
call %~dp0\venv\Scripts\activate.bat
python %~dp0\main.py
call %~dp0\venv\Scripts\deactivate.bat
timeout 10