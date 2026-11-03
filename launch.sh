#!/usr/bin/env bash

set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" || {
    echo "ERROR: Failed to locate the application directory." >&2
    exit 1
}
cd "$SCRIPT_DIR" || {
    echo "ERROR: Failed to enter the application directory." >&2
    exit 1
}

if [ -d ".venv" ]; then
    echo "Starting Streamlit app..."
    ".venv/bin/python" -m streamlit run main.py
    app_exit_code=$?
    if [ "$app_exit_code" -ne 0 ]; then
        echo "ERROR: Streamlit exited with code $app_exit_code." >&2
    fi
    exit "$app_exit_code"
fi

echo "Creating Python virtual environment..."
if command -v python3 >/dev/null 2>&1; then
    python_command=python3
elif command -v python >/dev/null 2>&1; then
    python_command=python
else
    echo "ERROR: Python is not installed or not available on PATH." >&2
    exit 1
fi

if ! "$python_command" -m venv .venv; then
    echo "ERROR: Failed to create the Python virtual environment." >&2
    exit 1
fi

echo "Installing dependencies..."
if ! ".venv/bin/python" -m pip install -r requirements.txt; then
    echo "ERROR: Failed to install dependencies from requirements.txt." >&2
    exit 1
fi

if [ ! -e ".env" ]; then
    echo "Creating .env file that user will have to fill in later"
    if ! cp .env.example .env; then
        echo "ERROR: Failed to copy .env.example into .env." >&2
        exit 1
    fi
fi

echo "Python virtual environment created and dependencies installed"
echo "Complete setup in .env file and run launch.sh again to start the app"