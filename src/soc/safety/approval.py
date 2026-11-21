from datetime import datetime, timezone
from pathlib import Path
import json
import uuid

PROJECT = Path("/content/drive/MyDrive/Cehpoint_Hermes_AI_SOC")
APPROVAL_AUDIT = PROJECT / "audit_logs" / "response_approvals.jsonl"

# These actions are deliberately simulated. No production action is implemented.
DISRUPTIVE_ACTIONS = {
    "disable_account",
    "block_ip",
    "revoke_sessions",
    "isolate_host",
    "delete_file"
}


def _audit(record):
    APPROVAL_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with APPROVAL_AUDIT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def request_response_action(action, target, approved=False, analyst=""):
    """
    Record a response request.
    Approval is explicit, attributable, and audited.
    This function NEVER performs the requested production action.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    request_id = "APR-" + uuid.uuid4().hex[:10].upper()

    if action not in DISRUPTIVE_ACTIONS:
        result = {
            "request_id": request_id,
            "status": "REJECTED",
            "reason": "Action is not in the permitted response-action list.",
            "action": action,
            "target": target,
            "production_action_executed": False
        }
        _audit({"timestamp": timestamp, **result})
        return result

    if not isinstance(target, str) or not target.strip():
        result = {
            "request_id": request_id,
            "status": "REJECTED",
            "reason": "A non-empty target is required.",
            "action": action,
            "target": target,
            "production_action_executed": False
        }
        _audit({"timestamp": timestamp, **result})
        return result

    if approved is not True or not isinstance(analyst, str) or not analyst.strip():
        result = {
            "request_id": request_id,
            "status": "AWAITING_APPROVAL",
            "reason": "Explicit approval from an identified analyst is required.",
            "action": action,
            "target": target,
            "production_action_executed": False
        }
        _audit({"timestamp": timestamp, **result})
        return result

    result = {
        "request_id": request_id,
        "status": "APPROVED_SIMULATION_ONLY",
        "reason": "Approval recorded; no production action was executed.",
        "action": action,
        "target": target,
        "approved_by": analyst.strip(),
        "production_action_executed": False
    }
    _audit({"timestamp": timestamp, **result})
    return result
