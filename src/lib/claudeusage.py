import os
import platform
import regex
from src.lib import agentusage
from src.lib.agentusage import ModelUsage

claude_paths = ["Claude", "Claude-3p"]

homepath = os.path.expanduser("~")

match platform.system():
    case "Windows":
        homepath = os.getenv("LOCALAPPDATA")
    case "Linux":
        homepath = os.path.join(homepath, ".config")
    case "Darwin":
        homepath = os.path.join(homepath, "Library", "Application Support")

pattern = regex.compile("\\d+-\\d+-\\d+\\.ndjson")

def get_claude_usage_data_files():
    path = ""
    for claude_dir in claude_paths:
        path = os.path.join(homepath, claude_dir, "local-agent-mode-sessions")
        if not os.path.exists(path):
            path = ""
        else:
            break
    if path == "":
        raise FileNotFoundError
    matching = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #print(file)
            if pattern.match(file):
                matching.append(os.path.join(root, file))
    return matching


def aggregate_claude_usages_from_files(files: list[str]) -> list[ModelUsage]:
    claude_usages = []
    for file in files:
        usages = agentusage.get_claude_usage(file)
        claude_usages = claude_usages + usages

    claude_models = []
    for usage in claude_usages:
        if usage.model not in claude_models:
            claude_models.append(usage.model)

    total_claude_usages = []
    for model in claude_models:
        model_usage = ModelUsage()
        for usage in claude_usages:
            if usage.model != model:
                continue
            model_usage_dict = model_usage.__dict__
            for key, value in usage.__dict__.items():
                if key == "model":
                    model_usage_dict[key] = value
                model_usage_dict[key] += value
        total_claude_usages.append(model_usage)
    return total_claude_usages


def get_total_claude_usage():
    claude_files = get_claude_usage_data_files()
    claude_usages = aggregate_claude_usages_from_files(claude_files)

    return f"--Total Claude Usage--\n{agentusage.get_model_usage_as_json_list(claude_usages)}"