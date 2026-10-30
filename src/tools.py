from langchain.tools import tool
from src.lib.claudeusage import get_total_claude_usage

@tool
def get_claude_usage() -> str:
    """Get the Claude usage data from the user's file system.
    Triggered by the phrase: Show me my Claude usage data.
    Or any mention of Claude usage data, Claude use, Claude usage, etc."""
    try:
        return get_total_claude_usage()
    except FileNotFoundError:
        return "Claude data not found. Claude may be not installed."