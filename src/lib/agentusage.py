import json
from json import JSONEncoder
from collections import defaultdict
from pathlib import Path
from typing import Any

claude_usage_map = {
    "input_tokens": "inputTokens",
    "cached_input_tokens": "cacheWriteTokens",
    "cache_write_input_tokens": "cacheReadTokens",
    "output_tokens": "outputTokens",
    "reasoning_output_tokens": 0,
    "total_tokens": 0,
}

class ModelUsage:
    model = "unknown"
    input_tokens = 0
    cached_input_tokens = 0
    cache_write_input_tokens = 0
    output_tokens = 0
    reasoning_output_tokens = 0
    total_tokens = 0

    def __init__(self, input_tokens= 0,
                 cached_input_tokens= 0,
                 cache_write_input_tokens = 0,
                 output_tokens = 0,
                 reasoning_output_tokens = 0,
                 total_tokens = 0,
                 model= "unknown"):
        self.model = model
        self.input_tokens = input_tokens
        self.cached_input_tokens = cached_input_tokens
        self.cache_write_input_tokens = cache_write_input_tokens
        self.output_tokens = output_tokens
        self.reasoning_output_tokens = reasoning_output_tokens
        self.total_tokens = total_tokens


def get_model_usage_as_json_list(usages: list[ModelUsage]) -> list[dict]:
    encoder = JSONEncoder()
    usage_json_list = []
    for usage in usages:
        usage_json_list.append(usage.__dict__)
    return encoder.encode(usage_json_list)


def totals_to_model_usage(totals: dict[str, Any]) -> list[ModelUsage]:
    final_list = []
    for model, usage in totals.items():
        model_usage = ModelUsage()
        model_usage.model = model
        for field in usage.keys():
            model_usage.__dict__[field] = usage[field]
        final_list.append(model_usage)
    return final_list


def get_codex_usage(path: str | Path) -> list[ModelUsage]:
    """Return token usage aggregated by model from a JSONL rollout file."""
    totals = defaultdict(lambda: {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "cache_write_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
        "total_tokens": 0,
    })

    default_model = "unknown"

    with Path(path).open("r", encoding="utf-8") as file:
        text = Path(path).read_text(encoding="utf-8")
        decoder = json.JSONDecoder()
        position = 0
        while position < len(text):
            while position < len(text) and text[position].isspace():
                position += 1

            if position == len(text):
                break

            try:
                record, position = decoder.raw_decode(text, position)
            except json.JSONDecodeError as exc:
                line_number = text.count("\n", 0, exc.pos) + 1
                raise ValueError(
                    f"Invalid JSON near line {line_number}: {exc.msg}"
                ) from exc
            
            if record.get("type") == "session_meta":
                default_model = (
                    record.get("payload", {})
                    .get("base_instructions", {})
                    .get("provenance", {})
                    .get("model", default_model)
                )

            if record.get("type") != "token_usage_record":
                continue

            payload = record.get("payload", {})
            usage = payload.get("usage", {})

            model = (
                payload.get("model")
                or usage.get("model")
                or default_model
            )

            for field in totals[model]:
                totals[model][field] += usage.get(field, 0) or 0

    return totals_to_model_usage(totals)


def get_claude_usage(path: str | Path) -> list[ModelUsage]:
    totals = defaultdict(lambda: {
            "input_tokens": 0,
            "cached_input_tokens": 0,
            "cache_write_input_tokens": 0,
            "output_tokens": 0,
            "reasoning_output_tokens": 0,
            "total_tokens": 0,
        })
    with Path(path).open("r", encoding="utf-8") as file:
        text = Path(path).read_text(encoding="utf-8")
        decoder = json.JSONDecoder()
        position = 0
        while position < len(text):
            while position < len(text) and text[position].isspace():
                position += 1

            if position == len(text):
                break

            try:
                record, position = decoder.raw_decode(text, position)
            except json.JSONDecodeError as exc:
                line_number = text.count("\n", 0, exc.pos) + 1
                raise ValueError(
                    f"Invalid JSON near line {line_number}: {exc.msg}"
                ) from exc
            
            models = dict(record.get("models"))
            
            if not models:
                continue
            
            for model in models.keys():
                for field in totals[model]:
                    add_to_field = models.get(model).get(claude_usage_map[field]) or 0
                    totals[model][field] += add_to_field
                    totals[model]["total_tokens"] += add_to_field

        return totals_to_model_usage(totals)