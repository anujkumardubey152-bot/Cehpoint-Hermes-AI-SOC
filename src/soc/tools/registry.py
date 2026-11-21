"""Central allowlist for approved SOC investigation tools."""

from .search_logs import search_logs
from .lookup_ip import lookup_ip
from .search_cve import search_cve

APPROVED_TOOLS = {
    "search_logs": search_logs,
    "lookup_ip": lookup_ip,
    "search_cve": search_cve,
}


def execute_tool(tool_name, arguments):
    """Execute only approved tools."""

    if not isinstance(tool_name, str) or tool_name not in APPROVED_TOOLS:
        return {
            "success": False,
            "error": "Tool not permitted",
            "tool": str(tool_name)
        }

    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": "Tool arguments must be a JSON object",
            "tool": tool_name
        }

    try:
        return APPROVED_TOOLS[tool_name](**arguments)

    except TypeError as exc:
        return {
            "success": False,
            "error": f"Invalid tool arguments: {exc}",
            "tool": tool_name
        }

    except Exception as exc:
        return {
            "success": False,
            "error": f"Tool execution failed: {exc}",
            "tool": tool_name
        }
