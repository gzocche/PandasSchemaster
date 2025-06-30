@echo off
REM Simple batch script for Windows to run the schema generator
REM Usage: generate_schema.bat input_file [options]
REM
REM Examples:
REM   generate_schema.bat data.csv
REM   generate_schema.bat data.csv -o schema.py -c MySchema

python "%~dp0generate_schema.py" %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Schema generation failed. Check the error messages above.
    pause
)
