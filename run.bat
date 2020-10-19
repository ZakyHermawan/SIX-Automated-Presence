@echo off
echo Starting script...
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0main.py"
call "%~dp0venv\Scripts\deactivate.bat"
timeout 10