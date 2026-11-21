# Hermes Runtime Integration Status

## Current implementation

The SOC prototype has a deterministic investigation planner and
a restricted tool registry.

The following tools are available through the adapter interface:

- search_logs
- lookup_ip
- search_cve

## Security boundary

All tool calls pass through the approved tool registry.

Unregistered tools are rejected.

No disruptive production action is exposed through this adapter.

## Runtime integration status

The adapter defines the interface required by a Hermes runtime.

The actual Hermes runtime has not yet been identified or verified
against the supplied Cehpoint assessment brief.

Therefore, this prototype must not be described as having
completed live Hermes orchestration until the selected runtime
is configured and a genuine tool-call trace is recorded.

## Required integration evidence

1. Confirm the intended Hermes framework and version.
2. Configure its supported custom-tool mechanism.
3. Register the three approved SOC tools.
4. Run an investigation through Hermes.
5. Preserve the runtime tool-call trace.
6. Demonstrate rejection of an unapproved tool.
