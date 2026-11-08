---
Status: Proposed
Doc-Type: index
Owner: protocol-maintainer
Last-Reviewed: 2026-11-08
---

# Repository ADRs that constrain a seam

Repository ADRs live in the repository that made them. This index lists only the few that constrain a seam or implement a PDR, so an agent changing a seam finds every local decision that pins it. An ADR that affects one repository's internals is not listed here, however important it is to that repository.

| Repository ADR | Seam or PDR | Consequence for other repositories |
|---|---|---|
| agent-bot-comms ADR-0004 | `wire-v1` | Durable mailbox delivery, and waking idle agents through the daemon planes. |
| agent-bot-comms ADR-0005 | `a2a-gateway` | A2A at the broker edge; tasks link to invocations. |
| agent-bot-comms ADR-0028 | `wire-v1` | Broker federation only through explicitly enrolled remote hubs (owner-accepted 2026-10-11). |
| agent-bot-comms ADR-0059 | `wire-v1` | Host apps embed agent-bot-comms through a contract and platform seams. |
| agent-bot-identity ADR-1183 | topology | agent-bot splits into an HQ daemon and plugins (owner decision agent-bot-hq D1). Its identity-plugin bullet is superseded by agent-bot-identity ADR-1381. |
| agent-bot-identity ADR-0332 | `hq-v1` | Souls are the agent's territory. Decision 2 (one daemon in the Souls' account) is superseded by agent-bot-identity ADR-1381. |
| agent-bot-identity ADR-1381 | PDR-0027, `hq-plugin-contract` | HQ runs in its own account (agent-bot-hq D6); HQ identity authority is HQ core, and agent-bot-identity's plugin registers member surfaces only. Resolves DRIFT-003. |

## Rules

1. Add a row when a repository ADR that constrains a seam is accepted, with a one-line consequence for other repositories.
2. Mark a superseded ADR in place; never delete the row.
3. A decision that would bind another repository is not made as a repository ADR at all. It is raised as a Decisions discussion and recorded as a PDR; see [change control](../00-governance/change-control.md).
