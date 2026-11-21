from datetime import datetime, timezone
from uuid import uuid4

from soc.tools.registry import execute_tool


def parse_timestamp(value):
    """Parse an ISO timestamp safely; return None if invalid."""
    if not isinstance(value, str):
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def assess_severity(events, alert):
    """
    Assess severity and confidence independently.
    Only use events returned by the approved local tools.
    """
    failed = [
        event for event in events
        if event.get("event_type") in ("failed_login", "login_failed")
    ]
    successful = [
        event for event in events
        if event.get("event_type") in ("successful_login", "login_success")
    ]
    host_events = [
        event for event in events
        if event.get("event_type") in ("host_login_observed", "host_activity")
    ]

    if len(failed) >= 50 and successful:
        severity = "High"
        severity_reason = (
            f"{len(failed)} failed login events and at least one successful "
            "login were found for the account."
        )
    elif failed and successful:
        severity = "Medium"
        severity_reason = (
            "Failed and successful login activity was found, but the "
            "available evidence does not meet the stronger threshold."
        )
    elif failed:
        severity = "Medium"
        severity_reason = "Failed login activity was found without a confirmed successful login."
    else:
        severity = "Low"
        severity_reason = "The retrieved events do not establish the supplied login pattern."

    if len(failed) >= 50 and successful and host_events:
        confidence = "High"
        confidence_reason = (
            "The login sequence is supported by matching account events "
            "and a related host event in the supplied dataset."
        )
    elif len(failed) >= 50 and successful:
        confidence = "Medium"
        confidence_reason = (
            "The login sequence is supported by account events, but "
            "independent host corroboration is absent."
        )
    else:
        confidence = "Low"
        confidence_reason = (
            "The expected event sequence is incomplete in the retrieved evidence."
        )

    return {
        "severity": severity,
        "severity_reason": severity_reason,
        "confidence": confidence,
        "confidence_reason": confidence_reason
    }


def build_timeline(events):
    timeline = []

    for event in events:
        timestamp = parse_timestamp(event.get("timestamp"))
        if timestamp is None:
            continue

        timeline.append({
            "timestamp": timestamp.astimezone(timezone.utc).isoformat(),
            "event_id": event.get("event_id", "UNKNOWN_EVENT_ID"),
            "event_type": event.get("event_type", "unknown"),
            "account": event.get("account"),
            "source_ip": event.get("source_ip"),
            "asset": event.get("asset"),
            "evidence_reference": event.get("_source_line")
        })

    timeline.sort(key=lambda item: item["timestamp"])
    return timeline


def run_investigation(alert):
    """Run a bounded investigation using only registered local tools."""
    incident_id = f"INC-{uuid4().hex[:10].upper()}"
    account = alert.get("account")
    source_ip = alert.get("source_ip")
    asset = alert.get("asset")

    investigation = {
        "incident_id": incident_id,
        "status": "UNDER_INVESTIGATION",
        "affected_entities": {
            "account": account,
            "asset": asset,
            "source_ip": source_ip
        },
        "tool_results": {},
        "timeline": [],
        "assessment": {},
        "evidence_gaps": [],
        "recommendations": []
    }

    # 1. Retrieve account events from the supplied synthetic log dataset.
    log_result = execute_tool(
        "search_logs",
        {"account": account}
    )
    investigation["tool_results"]["search_logs"] = log_result

    events = []
    if log_result.get("success"):
        events = log_result.get("evidence", [])
    else:
        investigation["evidence_gaps"].append(
            "Log search failed: " + str(log_result.get("error", "Unknown error"))
        )

    # 2. Look up the source IP in the local mock intelligence dataset.
    ip_result = execute_tool("lookup_ip", {"ip": source_ip})
    investigation["tool_results"]["lookup_ip"] = ip_result

    if not ip_result.get("success"):
        investigation["evidence_gaps"].append(
            "IP lookup failed: " + str(ip_result.get("error", "Unknown error"))
        )
    else:
        investigation["evidence_gaps"].append(
            "The IP lookup uses local mock intelligence only; "
            "it is not a live reputation assessment."
        )

    # 3. CVE lookup is only relevant if the alert supplies a product name.
    # Do not treat a workstation hostname as a software product.
    product = alert.get("affected_product")
    if isinstance(product, str) and product.strip():
        cve_result = execute_tool(
            "search_cve",
            {"product": product.strip()}
        )
        investigation["tool_results"]["search_cve"] = cve_result
        if not cve_result.get("success"):
            investigation["evidence_gaps"].append(
                "CVE lookup failed: " + str(cve_result.get("error", "Unknown error"))
            )
    else:
        investigation["tool_results"]["search_cve"] = {
            "success": True,
            "status": "NOT_RUN",
            "reason": (
                "No affected software product was supplied. "
                "A workstation name is not sufficient evidence for a CVE search."
            ),
            "matches": []
        }

    # 4. Build timeline and assess the retrieved evidence.
    investigation["timeline"] = build_timeline(events)
    investigation["assessment"] = assess_severity(events, alert)

    if not events:
        investigation["evidence_gaps"].append(
            "No matching log events were retrieved; the alert itself "
            "has not been independently corroborated."
        )

    if not any(
        event.get("event_type") in ("host_login_observed", "host_activity")
        for event in events
    ):
        investigation["evidence_gaps"].append(
            "No related host activity was found in the retrieved account logs."
        )

    if ip_result.get("success"):
        ip_data = ip_result.get("record")
        if not ip_data:
            ip_data = ip_result.get("result")
        if not ip_data:
            ip_data = ip_result.get("evidence")
        investigation["assessment"]["ip_lookup_result"] = ip_data

    investigation["assessment"]["conclusion"] = (
        "The supplied log dataset supports suspicious account login activity. "
        "This prototype cannot establish the real-world identity or intent "
        "of the source IP from the local mock lookup."
    )

    investigation["recommendations"] = [
        {
            "priority": 1,
            "action": "Ask the account owner to confirm whether the successful login was expected.",
            "expected_impact": "Helps distinguish legitimate activity from possible account compromise.",
            "approval_required": False
        },
        {
            "priority": 2,
            "action": "Review the account's recent authentication and host activity.",
            "expected_impact": "May identify additional suspicious activity not present in this sample.",
            "approval_required": False
        },
        {
            "priority": 3,
            "action": "Consider a password reset and session revocation if compromise is confirmed.",
            "expected_impact": "Can reduce continued unauthorized account access.",
            "approval_required": True
        }
    ]

    return investigation
