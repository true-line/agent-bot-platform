---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-19
Last-Reviewed: 2026-11-19
Discussion: https://github.com/true-line/agent-bot-platform/discussions/93
Amends: PDR-0091
Affects-Repos: [agent-bot-platform, agent-bot-hq, agent-bot-machine, soul-conformance]
Affects: [daemon-machine-channel, R2, R3, trust-model]
---

# PDR-0093 Permit Secure Enclave signing in explicitly configured standalone HQ

Machine is the default. The owner explicitly approved one exception to
[PDR-0091](PDR-0091-host-privileged-custody.md) on 2026-11-19 because a
standalone installation may intentionally omit Agent Machine and still
need HQ to sign. [Approval record](https://github.com/true-line/agent-bot-platform/discussions/93).

## Conditions

HQ may sign locally using the Secure Enclave only when all three are true:

1. The operator explicitly configured a standalone HQ installation.
2. HQ runs under its own dedicated operating-system account.
3. Agent Machine is not installed.

A stopped or unreachable Machine, a missing socket, or a failed or revoked
pairing must never select or enable local signing. Machine-backed HQ fails
closed for the affected operation. HQ in an ordinary user account uses Machine
even when the host has a Secure Enclave. Uncertain eligibility confers no
permission to sign locally.

## Scope and verification

This exception covers only local Secure Enclave signing. It grants no local
software signing, encryption, decryption, or general protected-resource access.
Verify the authorized standalone case and verify refusal for an ordinary
account, implicit configuration, installed but unavailable Machine, and revoked
pairing. Exercise the ordinary Machine-backed path as the default.

The owner-approval and recorded-justification requirement in
[PDR-0091](PDR-0091-host-privileged-custody.md#change-control) remains in force.
No agent may broaden this exception without that approval and justification.
