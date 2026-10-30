@echo off
setlocal

if exist ".venv" (
    echo ".venv already exists"
) else (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 goto venv_error

    echo Installing dependencies...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto install_error
)

echo Starting Streamlit app...
".venv\Scripts\python.exe" -m streamlit run main.py
if errorlevel 1 goto streamlit_error
exit /b 0

:venv_error
echo ERROR: Failed to create the Python virtual environment.
exit /b 1

:install_error
echo ERROR: Failed to install dependencies from requirements.txt.
exit /b 1

:streamlit_error
set "APP_EXIT_CODE=%ERRORLEVEL%"
echo ERROR: Streamlit exited with code %APP_EXIT_CODE%.
exit /b %APP_EXIT_CODE%