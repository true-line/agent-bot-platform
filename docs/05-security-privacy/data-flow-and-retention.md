---
Status: Draft
Doc-Type: security
Owner: security-reviewer
Last-Reviewed: 2026-11-05
Scope: data in motion and at rest
---

# Data flow and retention

What data exists, where it goes, what leaves the machine, and how long it
stays. Specified unless marked otherwise.

## Outbound flows

| Route | What leaves | Restriction | Where specified |
|---|---|---|---|
| Remote model | task context the broker sends | destination checked against task **data restrictions** | §4, §9 |
| Relay | **outer frame only**: destination, epoch hint, message ID, expiry, size, wake class; content sealed | timing/size observable | §6 |
| Evaluation exports | eval data | same disclosure restrictions as the original task | §10 |
| Trace export | spans | **content excluded** | §12 |
| Diagnostics | receipts (content redacted), admission result, digests | **never member homes or workspaces** | §12 |
| Transfer/backup export | package life + protected history export | **secrets and reusable grants excluded** | §11, §15 |

## At rest

| Data | Location | Access policy | Retention |
|---|---|---|---|
| Receipts | HQ store | owner; sensitive payload stored **separately under its own access policy**, receipts carry a request digest | release criteria reference (§15); [proposed] retention window policy |
| Notes / memorial | package | self-reported memory, **not evidence** (§10) | travels with life |
| Task ledger, dedup records, nonces | HQ store | owner | protected export only |
| Diagnostics | bundle | content-free (§12) | [proposed] 90 days |
| Workspaces | package, mediated views | scope per grant | task lifetime + owner policy |

## Restriction knobs (owner)

- Destinations per grant; data restrictions on grants/tasks (Appendix A)
- Disclosure labels on tasks
- **Local model** as destination — no outbound model context (§4)
- Network allowlist + broker narrow API (§4)
- Relay: no content ever; inspect with
  `hq receipts <soul> --destination <id>` (proposed verb)

## Enterprise review notes

- No telemetry vendor default: traces are OpenTelemetry GenAI, export
  excludes content (§12) — point reviewers at the §12 storage baseline
- The request digest on receipts allows proving *that* a payload was sent
  without storing the payload
- The cooperation of disclosure rules across task → eval export (§10)
  is the property enterprise reviewers usually miss; state it up front

## Open items

- [UNSPECIFIED] concrete retention defaults per data class (receipts,
  traces, bundles) — propose and track
- [UNSPECIFIED] relay log retention on hub side
