---
name: run-usage-agent
description: 'Install, configure, launch, or troubleshoot this Usage Agent app on Windows. Use when setting up Python dependencies, preparing .env, running launch.bat, or starting the Streamlit UI.'
user-invocable: false
---

# Install and Run the Usage Agent

Use these steps when setting up or launching this repository. Run commands from the repository root.

## Prerequisites

- Windows with Python 3 available as `python` on `PATH`.
- Azure OpenAI access and a deployment named `gpt-4o`. The app uses API version `2024-10-21`.

## Configure

1. If `.env` does not exist, copy `.env.example` to `.env`. Never overwrite an existing `.env`.
2. Set `OPENAI_BASE_URL` to the Azure OpenAI endpoint without a trailing slash, and set `OPENAI_API_KEY` to the corresponding key.
3. Keep credentials in the local `.env`; do not print them, commit them, or ask the user to paste them into chat. If credentials are unavailable, ask the user to configure `.env` locally.

PowerShell command for the first step:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

## Install and Launch

Run the launcher from the repository root:

```powershell
./launch.bat
```

On first run, `launch.bat` creates `.venv`, installs `requirements.txt`, and starts Streamlit with `main.py`. Open `http://localhost:8501` when Streamlit reports that it is ready, and keep the terminal process running while using the app.

If `.venv` already exists and dependencies have changed, update them before launching:

```powershell
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./launch.bat
```

## Troubleshooting

- If `python` is not recognized, install Python 3 and ensure it is available on `PATH`.
- If dependency installation fails, run `./.venv/Scripts/python.exe -m pip install -r requirements.txt` and inspect the first package error.
- If Azure requests fail, verify the endpoint, key, API access, and `gpt-4o` deployment in `.env` and Azure. Do not include secret values in diagnostic output.
- If port 8501 is already occupied, start Streamlit on another port with `./.venv/Scripts/python.exe -m streamlit run main.py --server.port 8502` and open `http://localhost:8502`.