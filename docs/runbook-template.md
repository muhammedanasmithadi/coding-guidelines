# Runbook template (every paging alert links one)

- Alert: name + query + severity (SEV1-4) + owner team + on-call rotation.
- Symptoms: how to confirm (dashboard links, log query with `trace_id`).
- Triage (5 min): which panel proves user impact, how to silence safely.
- Mitigation: kill-switch/flag name, rollback command, scale command.
- Escalation: when to SEV1, who pages next, comms channel.
- Post-incident: postmortem issue link within 48h.
