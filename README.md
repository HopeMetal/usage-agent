# AI Assistant Usage Optimization Agent

This is an AI agent that can read your local AI assistant session usage data and provide advice on how to optimize your own AI usage.

It supports the following AI assistants:
* Claude and Claude Code

## Installation

1. Make sure you have Python installed on your system.
2. Clone this repo locally.
3. Make a copy of .env.example, rename it to .env and fill in the URL to your Azure OpenAI endpoint and add your Azure OpenAI API key.
4. Run `launch.bat` on Windows or `./launch.sh` on Linux to set up a Python virtual environment on first run, then launch the agent.

You can also ask your AI assistant to install and run this app with the provided skill in .agents

## Usage

When you run the app, you can interact with the agent either with the "Get Claude Usage" button, or by prompting the agent with the chat box at the bottom.