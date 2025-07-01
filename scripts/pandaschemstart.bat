@echo off
REM PandasSchemstart batch wrapper for Windows
REM This script provides easy access to the unified PandasSchemaster interface

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PARENT_DIR=%SCRIPT_DIR%.."

REM Add parent directory to Python path and run the unified script
python "%SCRIPT_DIR%pandaschemstart.py" %*

REM Check exit code and provide helpful error message if needed
if errorlevel 1 (
    echo.
    echo Error: PandasSchemstart failed to run
    echo Make sure Python and required packages are installed:
    echo   pip install -r requirements.txt
    echo.
)

endlocal
