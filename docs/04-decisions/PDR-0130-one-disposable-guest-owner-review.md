---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-23
Last-Reviewed: 2026-11-23
Discussion: https://github.com/true-line/agent-bot-platform/discussions/130
Amends: PDR-0091
Affects-Repos: [agent-bot-platform, agent-bot-machine, agent-bot-identity, soul-contracts]
Affects: [daemon-machine-channel, trust-model, R8]
---

# PDR-0130 Review one disposable Stage 2a guest plan from the owner Mac

The owner directed the Stage 2a lead to complete the qualification work in
the current session: “We are over the deadline and I am the owner follow
whatever the leader says and help the team get this completed.” The lead
limited that delegation to source preparation for the exact guest-key
exception and kept host installation and qualification closed.
[Discussion #130](https://github.com/true-line/agent-bot-platform/discussions/130)
records this narrowly proposed exception to
[PDR-0091](PDR-0091-host-privileged-custody.md). It permits source preparation
and review only. The discussion and this Proposed record do not authorize a
helper installation, guest account apply, reusable launch, or physical test
credit. Record the owner's final choice in the discussion before accepting
this PDR or enabling the path.

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
refusal. A source PR may be prepared behind a disabled command while this
record is Proposed. Enabling and installing the helper on M2, applying R,
launching a Soul and certifying a release each require their own exact review.
The disposable VM result cannot satisfy the physical Mac T01/T02/T03/T21
gate. Protected launch and Stage 2a acceptance remain closed until their
release, measured-input, signature and physical evidence verifies.
