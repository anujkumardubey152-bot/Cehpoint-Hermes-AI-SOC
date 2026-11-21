import json

from .common import PROJECT, validate_string, record_tool_call


def search_logs(account, source_ip=None, event_type=None):
    inputs = {
        "account": account,
        "source_ip": source_ip,
        "event_type": event_type
    }

    try:
        account = validate_string(account, "account")

        if source_ip is not None:
            source_ip = validate_string(source_ip, "source_ip")

        if event_type is not None:
            event_type = validate_string(event_type, "event_type")

        path = PROJECT / "data" / "logs" / "authentication.jsonl"
        if not path.exists():
            raise FileNotFoundError("Authentication log dataset not found")

        evidence = []
        malformed_lines = 0

        with path.open("r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    malformed_lines += 1
                    continue

                if not isinstance(event, dict):
                    malformed_lines += 1
                    continue

                if event.get("account") != account:
                    continue

                if source_ip is not None and event.get("source_ip") != source_ip:
                    continue

                if event_type is not None and event.get("event_type") != event_type:
                    continue

                event["_source_line"] = line_number
                evidence.append(event)

        output = {
            "success": True,
            "tool": "search_logs",
            "count": len(evidence),
            "evidence": evidence,
            "source_type": "synthetic_local_dataset",
            "malformed_lines_skipped": malformed_lines,
            "message": (
                "Matching records found"
                if evidence else "No matching records found"
            )
        }

        record_tool_call("search_logs", inputs, output, "success")
        return output

    except Exception as exc:
        output = {
            "success": False,
            "tool": "search_logs",
            "error": str(exc),
            "evidence": []
        }
        record_tool_call("search_logs", inputs, output, "failure")
        return output
