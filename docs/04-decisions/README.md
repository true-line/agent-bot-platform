---
Status: Proposed
Doc-Type: index
Owner: product-owner
Last-Reviewed: 2026-11-12
---

# Decisions

Platform decision records (PDRs) are the decisions that bind more than one repository: requirements and scope, trust model, seams and repository topology. Everything else is decided, and recorded, in the one repository it affects.

## Platform decision records

| PDR | Title | Status |
|---|---|---|
| [PDR-0001](PDR-0001-platform-repository-is-the-product-source-of-truth.md) | The platform repository is the product source of truth | Accepted 2026-11-07 |
| [PDR-0002](PDR-0002-repository-topology-and-admission.md) | Repository topology and admission | Accepted 2026-11-07 |
| [PDR-0020](PDR-0020-components-read-the-platform-at-main.md) | Components read the platform at main | Accepted 2026-11-07; amends PDR-0001 |
| [PDR-0023](PDR-0023-hq-observation-uplink-for-presence-bindings-and-events.md) | HQ observation uplink for presence, bindings and events | Accepted 2026-11-08 |
| [PDR-0024](PDR-0024-comms-mirrors-task-v1-and-frames-wire-v1.md) | agent-comms mirrors task-v1 and frames wire-v1 | Accepted 2026-11-07 |
| [PDR-0027](PDR-0027-hq-identity-authority-lives-in-agent-bot-daemon.md) | HQ identity authority lives in agent-bot-daemon | Accepted 2026-11-08 |
| [PDR-0037](PDR-0037-agent-bot-executables-are-daemon-plugins-behind-a-shim.md) | agent-bot executables are daemon plugins behind a shim | Accepted 2026-11-08 |
| [PDR-0040](PDR-0040-repository-renames-and-transfers-to-true-line.md) | Repository renames and transfers to true-line | Accepted 2026-11-08 |
| [PDR-0053](PDR-0053-soul-life-and-agent-replace-member.md) | Soul, Life and agent replace member | Accepted 2026-11-12 |
| [PDR-0055](PDR-0055-a-soul-is-managed-when-hq-starts-it.md) | A Soul is managed when HQ starts it | Accepted 2026-11-12 |
| [PDR-0047](PDR-0047-harbor-is-the-control-plane-of-a-linked-machine.md) | Harbor is the control plane of a linked machine; HQ alone stays a complete deployment | Proposed |
| [PDR-0048](PDR-0048-notes-live-in-dreams-inputs-held-in-memory-and-synced-in-batches.md) | Notes live in dreams/inputs, held in memory and synced to the Soul in batches | Proposed |
| [PDR-0047](PDR-0047-harbor-is-the-control-plane-of-a-linked-machine.md) | Harbor is the control plane of a linked machine; HQ alone stays a complete deployment | Accepted 2026-11-11; rewords R2, amends PDR-0002 |
| [PDR-0048](PDR-0048-notes-live-in-dreams-inputs-held-in-memory-and-synced-in-batches.md) | Notes live in dreams/inputs, held in memory and synced to the Soul in batches | Accepted 2026-11-11 |

## How a decision is made

1. Check the [platform test](../00-governance/change-control.md#is-it-a-platform-decision). If exactly one repository would change, stop and record it there.
2. Open a discussion in [Decisions](https://github.com/true-line/agent-bot-platform/discussions/categories/decisions). Its number is the PDR number.
3. Deliberate in the discussion; the owner marks the chosen answer.
4. Record it as `PDR-NNNN-slug.md` from the PDR template, Proposed, then Accepted when the owner approves the PR.

## Related pages

- [Decision log](decision-log.md): decisions made before this repository existed, and the open decisions the whitepaper already names.
- [Repository ADRs that constrain a seam](cross-repo-adr-index.md).
