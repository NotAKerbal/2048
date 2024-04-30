@echo off
ECHO Checking for python install...
winget install -e --id Python.Python.3.11

ECHO Installing Dependancies...
pip install pygame
pip install mediapipe


ECHO Completed...
set /p any=Press any key to exit
