---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-21
Last-Reviewed: 2026-11-21
Discussion: https://github.com/true-line/agent-bot-platform/discussions/102
Affects-Repos: [agent-bot-platform, agent-bot-machine, agent-bot-hq, soul-adapters, soul-contracts, soul-conformance]
Affects: [R8, trust-model]
---

# PDR-0102 Verify protected adapter qualification offline

The owner approved this trust model for protected adapter launches. A package
build identifies what was produced. Qualification also requires independent
evidence of how the exact package and harness behaved on the declared host.
[Owner decision](https://github.com/true-line/agent-bot-platform/discussions/102#discussioncomment-19798348).

## Evidence and certification

Only a designated qualification host may sign test evidence. Ordinary device
enrollment grants no such authority. On macOS, the independent conformance
runner supplies a fixed report. Machine/keyd signs that report under the
administrator account. HQ cannot request signatures over arbitrary input.
The physical Mac gate requires T01, T02 and T03 under protected enforcement
and T21 under cooperative enforcement. [macOS pilot decision](PDR-0085-macos-first-protected-pilot.md).

To collect evidence before an adapter's first certification, the owner may
approve a single qualification run on a designated test Mac. The approval
identifies the exact candidate adapter and test plan and is consumed once.
The independent runner exercises the real controls with disposable member
state and a test provider. It records which controls were in force and submits
the results for review. Ordinary HQ work and reusable launch grants still
require the certified adapter and a separately approved launch-rule installation.
[Owner decision on first qualification](https://github.com/true-line/agent-bot-platform/discussions/102#discussioncomment-19798697).

One designated release workflow in `true-line/soul-adapters` may certify a
qualification after verifying the host-signed passing results. The owner pins
the release source, workflow identity and authorized evidence signers in signed
policy. The qualification attestation has its own type. Its subject is the digest
of the exact bytes of `qualification.json`. The record binds the package and
native harness digests, executable, ordered arguments, code inputs, host,
enforcement profile, suite revision and results. The adapter manifest references
the signed attestation. Build provenance alone cannot authorize a protected launch.

## Offline verification and local approval

Machine ships with an initial signed policy covering trust and revocation. HQ
may deliver a newer signed revision. Machine verifies it locally, rejects a
rollback to an older revision and enforces expiry. Only the owner authorizes
changes to trusted identities. HQ can withhold an update. It cannot extend
expiry, add a signer or override a revocation. Machine needs no internet access.

Refuse a protected launch when qualification has expired, revocation information
is stale, the evidence or signer is unknown or revoked, the installed inputs
have changed, or the required Machine pairing is unavailable. Cooperative
execution requires an explicit choice. The operator still approves each exact
local launch-rule installation.

## Open policy value

The maximum permitted age of revocation information remains open. This
decision grants no provisional interval and qualifies no adapter or installation.
