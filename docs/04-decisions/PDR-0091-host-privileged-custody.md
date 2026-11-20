---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-19
Date: 2026-11-19
Discussion: https://github.com/true-line/agent-bot-platform/discussions/91
Affects-Repos: [agent-bot-platform, agent-bot-hq, agent-bot-machine, agent-bot-identity, soul-conformance]
Affects: [daemon-machine-channel, identity-service-api, R2, R3, trust-model, governance]
---

# PDR-0091 Machine holds and uses privileged host keys and resources

The owner reaffirmed the administrative custody boundary for every platform,
profile, deployment mode and entry point. Agent Machine is the sole local
authority for access to privileged keys and protected host resources. Its
trusted executor and keyd perform those operations in the secure
administrative account. This also applies when HQ runs in an ordinary
account or the operator declines to create a dedicated HQ account.

**Dated amendment.** [PDR-0093](PDR-0093-standalone-hq-secure-enclave-signing.md) records the narrowly approved standalone signing exception. This earlier record is preserved.

## Authority and execution

1. HQ owns the enrollment workflow and its application-level decisions.
   It requests each privileged operation over the authenticated, signed local
   Machine channel. Caller identity alone does not authorize the operation.
   Each request names a fixed, strongly typed operation. Machine checks its
   expected fields, requested purpose and authority. Signing, encryption and
   decryption with protected host keys run under the admin credentials. Machine
   constructs or validates the operation-specific input and returns only the
   permitted result. A paired caller cannot select an arbitrary key or use a
   general sign, encrypt or decrypt interface. Raw private
   keys and unrestricted signing capability remain inside the admin boundary.
2. For device enrollment and token proofs, HQ handles the identity-service
   HTTPS exchange. Machine and keyd can perform local signing offline.
   Signature verification uses public data. Signing a message to establish
   the caller on the paired channel gives that caller no authority to sign
   as the enrolled device.
3. Direct hardware access, local software keys, transient keys used for
   privileged credential operations, helper binaries, migration and recovery
   are subject to the same rule. An unavailable secure provider makes the
   operation unavailable. Installation, testing with real credentials, or a
   cooperative profile cannot move the operation into a nonsecure account.
4. Protected qualification requires observations of the actual calling and
   executing accounts, an authenticated HQ request, Machine authorization,
   successful verification of the returned result, and persistence across
   restart. A signature alone cannot establish where the key was used.
   Test fixtures using disposable identities establish component behavior only.

## Change control

Agents are forbidden to rewrite, weaken, bypass or add an exception to this
boundary in code, tests, configuration, documentation, deployment or recovery
without **prior explicit product-owner approval and recorded justification
for the exact change**. Before changing the boundary, present the proposed
difference, why it is necessary, which accounts and resources it affects
and the security consequences. Record the owner's decision and justification
in a successor platform decision. Preserve the historical record and link
the successor. An ordinary PR approval, green CI or a component decision
cannot grant an implicit exception.

## Evidence and adoption

The original agent-bot-hq D4 change explicitly attached administrative custody to the HQ
signer entry. Later component text associated private-key use with HQ.
PDR-0027 assigned enrollment authority to HQ when deciding the identity
plugin boundary. This clarification retains that responsibility and locates
privileged execution in Machine. The current implementation gaps remain
open until verified on the relevant platform and account layout.
[Original custody wording](https://github.com/true-line/agent-bot-hq/blob/6480b35d9b881393553e2f0ef6e3e02e55285a6f/docs/daemon-plugin-split.md#L244)
· [agent-bot-hq D4 decision](https://github.com/true-line/agent-bot-hq/blob/6480b35d9b881393553e2f0ef6e3e02e55285a6f/docs/daemon-plugin-split.md#L879-L907)
· [Owner-directed correction](https://github.com/true-line/agent-bot-platform/discussions/91).
