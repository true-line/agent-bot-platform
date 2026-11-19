---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-18
Date: 2026-11-18
Discussion: https://github.com/true-line/agent-bot-platform/discussions/89
Affects-Repos: [agent-bot-machine, agent-bot-identity, agent-bot-hq]
Affects: [daemon-machine-channel, trust-model]
---

# PDR-0089 Owner approval for the first HQ account on macOS

The product owner chose a one-time transfer for the first HQ setup on a fresh
Mac. The operator takes Machine's saved plan to the local Approvals UI and
returns its signed proof to Machine. The decision record awaits formal PR
approval. [Owner choice](https://github.com/true-line/agent-bot-platform/discussions/89#discussioncomment-19724884)

## Context

Machine requires a signed approval before it can create the HQ account. The
account must already exist to request the HQ pairing challenge. The first
installation therefore needs a way to approve the account plan before HQ can
retrieve plans over its signed channel.
[Machine #524](https://github.com/true-line/agent-bot-machine/issues/524)

## Decision

The proposed first-install flow has four steps.

1. The prefix administrator pins the independently verified public key of the signer
   in the owner's session. Machine presents a fresh challenge and its saved first-HQ plan for the
   operator to transfer to the local Approvals UI.
2. The UI recomputes the plan digest and shows the exact steps. The plan covers
   the first HQ account and, when explicitly included, the HQ service unit and
   owner-only control socket directory. After confirmation, the signer in the owner's session
   requests presence and signs the first-HQ provisioning action, binding it to
   this Machine, the plan ID and digest, the nonce and the expiry.
3. The operator returns the public proof to Machine. Machine verifies it against
   the pinned key, saved plan and outstanding challenge, and consumes the
   challenge once. The human runs the existing root apply, which revalidates
   the approved plan before changing the host.
4. HQ then pairs from its dedicated account with a fresh key. After enrollment,
   only the authenticated HQ client may list and retrieve plans over the signed
   channel. Existing enrollment, replacement and key rotation follow their
   own flows. [Service installation decision](https://github.com/true-line/agent-bot-platform/discussions/49)
   · [Plan retrieval decision](https://github.com/true-line/agent-bot-platform/discussions/50)

## Consequences

- Machine owns challenge issuance, proof verification and execution. Its
  channel contract must document the one-time first-install exchange.
- Identity owns the local Approvals UI, digest calculation and owner-session
  signature. Its displayed steps must match the steps Machine applies. The
  standalone macOS approval app exercises this role for qualification. The
  [owner interface plan](https://github.com/true-line/agent-bot-hq/blob/main/docs/daemon-plugin-split.md#7-owner-interface-hqv1-for-geniusbar-and-the-hq-cli)
  identifies GeniusBar and the HQ CLI as the product interfaces.
- HQ uses the enrolled channel after setup. Verify the full sequence on a
  clean macOS installation, including cancellation and expiry with the plan
  and host unchanged, one authorized apply, pairing from the dedicated HQ
  account, and a verified signed Machine status. Prove the root install on a
  disposable CI runner as required by the service installation decision.
  The physical [pilot qualification](https://github.com/true-line/agent-bot-hq/issues/56)
  retains its own acceptance criteria.

## Alternatives considered

A narrowly scoped local endpoint could carry the same challenge and proof.
It would save the operator a transfer, but would require a pre-enrollment
service with cross-account authentication, startup handling and delivery
across the participating clients. Discussion #89 recommends the explicit
transfer for first installation.
