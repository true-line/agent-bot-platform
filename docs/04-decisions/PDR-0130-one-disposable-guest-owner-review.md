---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Date: 2026-11-23
Accepted: 2026-11-23
Last-Reviewed: 2026-11-26
Discussion: https://github.com/true-line/agent-bot-platform/discussions/130
Amends: PDR-0091
Affects-Repos: [agent-bot-platform, agent-bot-machine, agent-bot-identity, soul-contracts]
Affects: [daemon-machine-channel, trust-model, R8]
---

# PDR-0130 Review one disposable Stage 2a guest plan from the owner Mac

The owner delegated Stage 2a completion to the lead in the active session and
answered “Yes” to the exact proposal in
[Discussion #130](https://github.com/true-line/agent-bot-platform/discussions/130).
The lead recorded that approval as source authority for this one guest-key
review design. This narrow exception to
[PDR-0091](PDR-0091-host-privileged-custody.md) permits source preparation
and review. It does not authorize helper installation, guest account apply,
reusable launch, or physical test credit. The ordinary same-host owner
commands remain pinned to the local Machine key.

## Exact scope

The only candidate is the accepted disposable Tart VM
`stage2a-bootstrap-2a80-20261124`, whose Machine public-key SHA-256 is
`2718659ba5fc81e5f199e7adaca1904b4ecb4df7a1e95f466acbe04c4356fb66`.
The physical M2 Machine public-key SHA-256 is
`c11ecaf6a108cfb8a1fcadd83dc32e763a947653a87272107bd76b26052432e0`.
The guest request is limited to the saved one-runner R account plan
`plan-20261124T014505Z-09b5`, digest
`aa91f21346030d11751b364415de70cbbe605791af3b43014627f9f428f18155`.
Its earlier challenge expired without a proof or account apply; a new
challenge must bind these same plan bytes and receive a separate owner review.
Any changed VM, key, plan or purpose requires a new decision.

## Candidate authority and refusal

1. The physical Machine authenticates the guest VM identity and key through
   independently verifiable local evidence. A Tart name, guest statement or
   unverified file hash alone is insufficient. If it cannot establish this
   binding, it refuses. It receives a fixed, authenticated request under
   [PDR-0091](PDR-0091-host-privileged-custody.md); a direct local request
   outside that route needs its own explicit owner decision.
2. After a separate purpose-bound owner approval for the exact VM, Machine
   signs a domain-separated permit in its secure administrative account.
   The permit binds physical and guest Machine keys, the VM evidence, exact
   signed guest challenge bytes, plan ID and digest, nonce and expiry. Machine
   durably claims one permit identity before issuance and refuses duplicate,
   replay, changed or uncertain state. Permit and guest challenge freshness
   must each be at most 120 seconds.
3. A separately named owner-helper command verifies the permit under the
   physical Mac's already installed Machine pin. It shows both Machine
   identities, VM evidence and the complete exact guest plan, obtains fresh
   owner presence, then signs only that guest challenge. The guest Machine
   consumes its own challenge once. Ordinary commands retain their same-host
   pin check and cannot accept a guest key or caller-selected trust root.

Machine/keyd perform protected signing in the secure administrative account
without direct network access. No private key moves to the guest, HQ or runner.
The physical owner account's Secure Enclave key may sign only the exact
reviewed guest challenge after the separate permit verification and fresh
presence. A compromised permit producer or incorrect VM binding could
authorize the wrong guest plan; the authenticated VM evidence, durable claim,
short expiry and full owner review are required controls.

## Implementation and acceptance gates

The fixed signed permit bytes, VM evidence semantics and negative fixtures
belong in `soul-contracts` before a positive product path is enabled. Machine
and Identity must verify each other's exact bytes, reject foreign keys,
changed plans, expired or replayed permits, and keep the ordinary local-pin
refusal. Source may be prepared behind a disabled command. Current Tart name,
config hash and ECID data do not establish an authenticated running VM/key
binding, so Machine must refuse a positive permit until that evidence exists.
Enabling and installing the helper on M2, applying R, launching a Soul and
certifying a release each require their own exact review.
The disposable VM result cannot satisfy the physical Mac T01/T02/T03/T21
gate. Protected launch and Stage 2a acceptance remain closed until their
release, measured-input, signature and physical evidence verifies.

## Recorded outcome

On November 24, 2026, Machine superseded the named plan without applying it.
The replacement, `plan-20261124T201315Z-5f72`, had the same digest and a
new plan ID. It received separate owner presence and paired HQ approval.
Machine applied the replacement and the account readback confirmed the runner
at UID/GID 310. This decision records source preparation for the original
plan only. The tracker records zero physical test passes at that checkpoint.
[Plan replacement](https://github.com/true-line/agent-bot-platform/issues/68#issuecomment-7143294856)
and [application receipt and readback](https://github.com/true-line/agent-bot-platform/issues/68#issuecomment-7143490544).
