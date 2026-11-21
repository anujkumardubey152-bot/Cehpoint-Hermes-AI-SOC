# Hermes-Powered AI SOC — Demo Script

**Target duration:** 7–9 minutes

> Important: This prototype currently uses a deterministic investigation
> workflow and local synthetic tools. The actual Cehpoint-selected Hermes
> runtime has not yet been identified or integrated. Do not describe this
> demonstration as a live Hermes runtime demonstration.

## 1. Introduction — 30 seconds

Introduce the project as a prototype AI Security Operations Centre analyst.
Explain that it accepts a security alert, gathers evidence through approved
tools, assesses severity and confidence, and produces an incident report.

## 2. Scenario — 1 minute

Demonstrate the synthetic account-compromise alert:

- Account: `analyst.user`
- Asset: `WORKSTATION-042`
- Source IP: `198.51.100.42`
- Failed login attempts: 50
- Successful login: yes

Explain that the data is synthetic and the IP belongs to a documentation-
reserved address range. It must not be presented as a real attacker IP.

## 3. Approved tools — 1.5 minutes

Show the three local tools:

1. `search_logs` — searches the supplied synthetic authentication logs.
2. `lookup_ip` — checks the local mock IP intelligence catalogue.
3. `search_cve` — searches the local mock vulnerability catalogue.

Explain that the tools are restricted through the approved tool registry.
The mock catalogues do not make live external intelligence queries.

## 4. Investigation — 1.5 minutes

Run the investigation workflow and show:

- Retrieved log events.
- Timestamped event timeline.
- Account, asset and IP correlation.
- Severity and confidence as separate assessments.
- Evidence gaps and limitations.

Explain why repeated failed logins followed by a successful login are
suspicious, while acknowledging that the available evidence does not prove
who operated the source IP or their intent.

## 5. Incident report and audit — 1 minute

Open the generated JSON and Markdown incident reports.

Show the incident ID, status, severity, confidence, affected entities,
timeline, evidence references, gaps and recommendations.

Show the tool-call and investigation history audit files.

## 6. Human approval and safety — 1.5 minutes

Demonstrate that an unregistered action such as `disable_account` is rejected
by the approved tool registry.

Demonstrate the response approval workflow using a simulated action.

Emphasise:

- No production action is executed.
- Disruptive actions require an approval record.
- The prototype's analyst name is self-declared, not authenticated.
- This is a simulation, not a production authorization system.

## 7. Testing and limitations — 1 minute

Show the automated test results.

Discuss limitations honestly:

- Synthetic lab data only.
- Local mock IP and vulnerability intelligence.
- No live SIEM connection.
- No production response actions.
- Actual Cehpoint-selected Hermes runtime integration remains pending
  confirmation.

## 8. Closing — 30 seconds

Summarise the prototype's value: structured alert investigation, approved
tool access, evidence-based severity assessment, incident reporting,
auditability and human approval safeguards.
