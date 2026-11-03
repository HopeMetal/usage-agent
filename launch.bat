@echo off
setlocal

if exist ".venv" (
    echo Starting Streamlit app...
    ".venv\Scripts\python.exe" -m streamlit run main.py
    if errorlevel 1 goto streamlit_error
    exit /b 0
) else (
    echo Creating Python virtual environment...
    python -m venv .venv
    if errorlevel 1 goto venv_error

    echo Installing dependencies...
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto install_error
    if not exist ".env" (
        echo Creating .env file that user will have to fill in later
        copy .env.example .env /A /Y /V
        if errorlevel 1 goto copy_env_error
    )
    echo Python virtual environment created and dependencies installed
    echo Complete setup in .env file and run launch.bat again to start the app
)

:venv_error
echo ERROR: Failed to create the Python virtual environment.
exit /b 1

:install_error
echo ERROR: Failed to install dependencies from requirements.txt.
exit /b 1

:copy_env_error
echo ERROR: Failed to copy .env.example into .env.
exit /b 1

:streamlit_error
set "APP_EXIT_CODE=%ERRORLEVEL%"
echo ERROR: Streamlit exited with code %APP_EXIT_CODE%.
exit /b %APP_EXIT_CODE%