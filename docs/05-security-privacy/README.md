---
Status: Draft
Doc-Type: index
Owner: security-reviewer
Last-Reviewed: 2026-11-07
---

# Security and privacy

What the platform protects, from whom, and where each secret and each piece of owner data may go. Security is the best-covered goal today; privacy is the weakest, as the [quality attributes](../02-requirements/quality-attributes.md) page records.

| Page | Contents |
|---|---|
| [Threat model](threat-model.md) | Assets, adversaries, trust boundaries and mitigations for the draft 0.4 surface |
| [Key boundaries](key-boundaries.md) | Which component holds which key, and how credentials flow |
| [Data flow and retention](data-flow-and-retention.md) | Data in motion and at rest, disclosure labels, retention and deletion |

Security reviews of a component happen in that component's repository. A finding that changes a trust boundary, a seam or a requirement comes here through a Decisions discussion, because it changes the platform's trust model.

This repository holds no personal or legal records. The rule and its automated check are in the repository's agent instructions.
