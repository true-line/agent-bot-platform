---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-20
Last-Reviewed: 2026-11-20
Discussion: https://github.com/true-line/agent-bot-platform/discussions/98
Affects-Repos: [agent-bot-platform, agent-bot-machine, agent-bot-hq, agent-bot-identity]
---

# PDR-0098 Owner approval to provision macOS harness accounts

On a paired Mac with a dedicated HQ account, the operator needs Machine to
create the local accounts where agents will run. The operator can then install
the agents in those accounts. The product owner approved a separate, single-use
account provisioning operation. [Decision discussion](https://github.com/true-line/agent-bot-platform/discussions/98).

Machine plans the exact accounts, private groups and homes, together with
any broker directories needed for those accounts. The owner sees which
resources already exist, which Machine proposes to create, and the reviewed
numeric user and group IDs. If a managed harness home needs its permissions
repaired, the plan shows its current mode and the proposed private mode (0700). HQ transports the plan and proof over its paired
channel. The owner approves the displayed plan with the existing owner key.

Machine verifies the live pairing, the purpose of the proof and the exact
plan before applying it. Changes to the planned resources or their properties
require a fresh review. A proof expires and can authorize a single application.
Provisioning the HQ account, installing or upgrading a service, and installing
or retiring a harness launch rule each retain their own approval scope.

## Verification

Exercise an account-only plan and one that includes broker directories. Check
that a changed account or directory, a proof for a different operation, a
replayed or expired proof, and a revoked pairing prevent application. On a
physical Mac, create the accounts through the reviewed product flow and verify
their identities, private homes, groups and directory permissions.
[Implementation tracking](https://github.com/true-line/agent-bot-machine/issues/581).
