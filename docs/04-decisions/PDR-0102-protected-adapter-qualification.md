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
state and a test provider. A protected result requires observed enforcement.
When a report claims a managed profile, HQ must have started the Soul through
the Soul runner. A direct vendor, IDE or web session remains unmanaged even if
Harbor policy or local hooks constrain it
([PDR-0055](PDR-0055-a-soul-is-managed-when-hq-starts-it.md)).
The run produces evidence for review. Its approval grants no authority for
ordinary HQ work, a reusable launch rule or release certification.
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

## Revocation-information freshness

The owner selected a maximum age of one hour (3,600 seconds) for revocation
information in the Stage 2a working session on 2026-11-21. The owner-signed
policy binds the timestamp of the revocation snapshot to its exact set.
At every protected launch, Machine rejects a missing or future-dated snapshot
and refuses when its age exceeds 3,600 seconds. A snapshot exactly 3,600
seconds old is still current. This check is independent of policy expiry and
qualification expiry. Reissuing a policy without a newly authenticated
revocation snapshot does not refresh the snapshot timestamp. HQ cannot reset
that timestamp, increase the limit or override a revocation. Machine checks
freshness offline.

This value does not qualify an adapter or installation. The owner-signed
policy, authenticated reports, release attestation, measured installed inputs
and protected-host results remain separate prerequisites.
