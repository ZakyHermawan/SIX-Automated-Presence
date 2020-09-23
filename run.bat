@echo off
echo Starting script...
call venv\Scripts\activate.bat
python main.py
call deactivate
pause