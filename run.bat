@echo off
echo Starting script...
D:
cd SourceCode\SIX-Automated-Presence
call venv\Scripts\activate.bat
echo %CD%
python D:\SourceCode\SIX-Automated-Presence\main.py
call venv\Scripts\deactivate.bat
timeout 10