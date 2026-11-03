# AI Assistant Usage Optimization Agent

This is an AI agent that can read your local AI assistant session usage data and provide advice on how to optimize your own AI usage.

It supports the following AI assistants:
* Claude and Claude Code

## Requirements

* OS: Windows or Linux
* Python 3.x
* A web browser with JavaScript support
* Access to an Azure OpenAI provider

## Installation

1. Make sure you have Python installed on your system.
2. Clone this repo locally.
3. Run `launch.bat` on Windows or `./launch.sh` on Linux to set up a Python virtual environment and stub .env file.
4. Edit the .env file with your Azure OpenAI endpoint and API key.
5. Run the same script as in Step 3. This will launch the agent app.

## Usage

When you run the app, you can interact with the agent either with the "Get Claude Usage" button, or by prompting the agent with the chat box at the bottom.