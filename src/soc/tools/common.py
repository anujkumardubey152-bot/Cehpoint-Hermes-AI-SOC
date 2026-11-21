from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

PROJECT = Path("/content/drive/MyDrive/Cehpoint_Hermes_AI_SOC")
AUDIT_FILE = PROJECT / "audit_logs" / "tool_calls.jsonl"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def validate_string(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    if len(value) > 255:
        raise ValueError(f"{field} exceeds 255 characters")
    return value.strip()


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def record_tool_call(tool, inputs, output, status):
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "call_id": "TOOL-" + uuid.uuid4().hex[:12].upper(),
        "timestamp": utc_now(),
        "tool": tool,
        "inputs": inputs,
        "outputs": output,
        "status": status
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
