---
Status: Proposed
Doc-Type: index
Owner: protocol-maintainer
Last-Reviewed: 2026-11-07
---

# Repository ADRs that constrain a seam

Repository ADRs live in the repository that made them. This index lists only the few that constrain a seam or implement a PDR, so an agent changing a seam finds every local decision that pins it. An ADR that affects one repository's internals is not listed here, however important it is to that repository.

| Repository ADR | Seam or PDR | Consequence for other repositories |
|---|---|---|
| agent-comms ADR-0004 | `wire-v1` | Durable mailbox delivery, and waking idle agents through the daemon planes. |
| agent-comms ADR-0005 | `a2a-gateway` | A2A at the broker edge; tasks link to invocations. |
| agent-comms ADR-0028 | `wire-v1` | Broker federation only through explicitly enrolled remote hubs (owner-accepted 2026-10-11). |
| agent-comms ADR-0059 | `wire-v1` | Host apps embed agent-comms through a contract and platform seams. |
| agent-bot-identity ADR-1183 | topology | agent-bot splits into an HQ daemon and plugins (owner decision agent-bot-daemon D1). |
| agent-bot-identity ADR-0332 | `hq-v1` | Souls are the agent's territory, one daemon in the Souls' account; in conflict with S6 (DRIFT-003). |

## Rules

1. Add a row when a repository ADR that constrains a seam is accepted, with a one-line consequence for other repositories.
2. Mark a superseded ADR in place; never delete the row.
3. A decision that would bind another repository is not made as a repository ADR at all. It is raised as a Decisions discussion and recorded as a PDR; see [change control](../00-governance/change-control.md).
