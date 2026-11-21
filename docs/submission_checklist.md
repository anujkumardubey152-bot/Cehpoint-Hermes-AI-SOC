# Cehpoint AI SOC — Submission Checklist

## Project and documentation
- [ ] README explains the project, setup and execution.
- [ ] Architecture diagram is included.
- [ ] Demo script is included.
- [ ] Known limitations are documented.
- [ ] Hermes runtime integration status is stated accurately.

## Alert intake and tools
- [ ] Alert JSON schema is included.
- [ ] Synthetic account-compromise alert is included.
- [ ] `search_logs` is implemented.
- [ ] `lookup_ip` is implemented.
- [ ] `search_cve` is implemented.
- [ ] Tool schemas and approved registry are included.
- [ ] Invalid and unknown tool requests are rejected.

## Investigation and reporting
- [ ] Investigation workflow is reproducible.
- [ ] Timeline is timestamped and evidence-linked.
- [ ] Severity and confidence are reported separately.
- [ ] Evidence gaps and alternative explanations are documented.
- [ ] JSON incident report is generated.
- [ ] Markdown incident report is generated.

## Safety and audit
- [ ] Tool-call audit log is included.
- [ ] Investigation history is included.
- [ ] Unauthorized action is rejected.
- [ ] Human approval simulation is demonstrated.
- [ ] No production action is executed.
- [ ] Approval limitations are documented.

## Testing
- [ ] Python syntax verification passes.
- [ ] All imports pass.
- [ ] All automated tests pass.
- [ ] End-to-end demonstration is reproducible.
- [ ] Missing or malformed data cases are considered.

## Final packaging
- [ ] No API keys, passwords or private credentials are included.
- [ ] Synthetic data is clearly labelled.
- [ ] Repository contains source code, tests, schemas, data and docs.
- [ ] Sample incident reports are included.
- [ ] README and demo instructions match the actual implementation.
- [ ] ZIP archive is reviewed before submission.

## Important honesty check
Do not claim live Hermes runtime integration, live threat intelligence,
real SIEM connectivity, authenticated analyst approval or production
containment unless those capabilities have actually been implemented
and demonstrated.
