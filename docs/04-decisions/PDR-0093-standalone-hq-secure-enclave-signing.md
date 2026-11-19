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

## Establishing eligibility on macOS

On a fresh installation, the installer records the administrator's explicit
choice of standalone signing for the dedicated HQ account and their declaration
that no custom Machine installation exists. HQ checks the supported Machine
executable locations and their code signatures, installation state and evidence
of prior pairing. A binary in an unexpected state or an inspection failure
prevents local signing. The declaration accounts for custom locations beyond
the installer's search. [Owner decision and justification](https://github.com/true-line/agent-bot-platform/discussions/93#discussioncomment-19759206).

A subsequent Machine installation or pairing retires that authorization before
Machine starts. HQ must enforce retirement even in a process that was already
running when the administrator changed the installation. Stopping or removing
Machine, or revoking its pairing, cannot revive the declaration.

## Standalone signer executable

The administrator installs the reviewed command-line helper in a protected
location. Standalone HQ verifies the exact release executable and its existing
Developer ID signature. The helper uses the Secure Enclave and keeps its
device-bound key reference in the dedicated HQ account's private file Keychain
under per-executable access control. These checks replace the app-specific
application identifier and Keychain access group entitlements for this helper.
Apple requires a profile-carrying bundle for those entitlements. The approved
command-line design uses the existing signing identity.
[Owner decision and justification](https://github.com/true-line/agent-bot-platform/discussions/93#discussioncomment-19759443).

## Scope and verification

This exception covers only local Secure Enclave signing. It grants no local
software signing, encryption, decryption, or general protected-resource access.
Verify the authorized standalone case and verify refusal for an ordinary
account, implicit configuration, installed but unavailable Machine, and revoked
pairing. Exercise the ordinary Machine-backed path as the default.

The owner-approval and recorded-justification requirement in
[PDR-0091](PDR-0091-host-privileged-custody.md#change-control) remains in force.
No agent may broaden this exception without that approval and justification.
