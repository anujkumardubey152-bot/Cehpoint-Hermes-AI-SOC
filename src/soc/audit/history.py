from pathlib import Path
from datetime import datetime, timezone
import json

PROJECT = Path("/content/drive/MyDrive/Cehpoint_Hermes_AI_SOC")
HISTORY_FILE = PROJECT / "audit_logs" / "investigation_history.jsonl"


def record_investigation(report):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "incident_id": report.get("incident_id"),
        "status": report.get("status"),
        "severity": report.get("severity"),
        "confidence": report.get("confidence"),
        "json_report": report.get("json_report"),
        "markdown_report": report.get("markdown_report")
    }

    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry


def read_investigation_history():
    if not HISTORY_FILE.exists():
        return []

    entries = []
    with HISTORY_FILE.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                entries.append({
                    "error": "Malformed history record",
                    "line_number": line_number
                })

    return entries
