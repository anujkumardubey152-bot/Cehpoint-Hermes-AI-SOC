import ipaddress

from .common import PROJECT, load_json, validate_string, record_tool_call


def lookup_ip(ip):
    inputs = {"ip": ip}

    try:
        ip = validate_string(ip, "ip")
        parsed_ip = ipaddress.ip_address(ip)

        path = PROJECT / "data" / "intelligence" / "ip_reputation.json"
        catalogue = load_json(path)

        if not isinstance(catalogue, dict):
            raise ValueError("IP intelligence catalogue must be a JSON object")

        record = catalogue.get(ip)

        output = {
            "success": True,
            "tool": "lookup_ip",
            "ip": ip,
            "record": record,
            "found": record is not None,
            "address_scope": (
                "reserved_or_special_use"
                if not parsed_ip.is_global else "global"
            ),
            "source_type": "local_mock_intelligence",
            "live_lookup_performed": False,
            "message": (
                "Local mock record found"
                if record is not None
                else "No local intelligence record found"
            )
        }

        record_tool_call("lookup_ip", inputs, output, "success")
        return output

    except Exception as exc:
        output = {
            "success": False,
            "tool": "lookup_ip",
            "error": str(exc),
            "live_lookup_performed": False
        }
        record_tool_call("lookup_ip", inputs, output, "failure")
        return output
