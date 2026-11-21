"""
Hermes integration boundary.

The actual Cehpoint-selected Hermes runtime must call this
adapter through its supported custom-tool mechanism.

This file does not simulate an LLM or claim Hermes execution.
"""

from soc.tools.registry import APPROVED_TOOLS, execute_tool


HERMES_TOOL_DEFINITIONS = [
    {
        "name": "search_logs",
        "description": (
            "Search the approved local authentication dataset "
            "for events associated with an account."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "account": {"type": "string"},
                "source_ip": {"type": ["string", "null"]},
                "event_type": {"type": ["string", "null"]}
            },
            "required": ["account"],
            "additionalProperties": False
        }
    },
    {
        "name": "lookup_ip",
        "description": (
            "Look up an IP in the local mock intelligence catalogue. "
            "This is not a live reputation lookup."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {"type": "string"}
            },
            "required": ["ip"],
            "additionalProperties": False
        }
    },
    {
        "name": "search_cve",
        "description": (
            "Search the local mock vulnerability catalogue by product."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product": {"type": "string"}
            },
            "required": ["product"],
            "additionalProperties": False
        }
    }
]


def execute_hermes_tool(tool_name, arguments):
    """
    Entry point for a verified Hermes tool-call adapter.
    Only tools in the approved registry can execute.
    """
    if tool_name not in APPROVED_TOOLS:
        return {
            "success": False,
            "error": "Tool not permitted",
            "tool": tool_name
        }

    if not isinstance(arguments, dict):
        return {
            "success": False,
            "error": "Tool arguments must be a JSON object",
            "tool": tool_name
        }

    return execute_tool(tool_name, arguments)


def get_hermes_tool_definitions():
    return HERMES_TOOL_DEFINITIONS
