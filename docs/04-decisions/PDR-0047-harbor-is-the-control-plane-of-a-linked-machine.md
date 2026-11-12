---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-11
Date: 2026-11-11
Accepted: 2026-11-11
Discussion: https://github.com/true-line/agent-bot-platform/discussions/47
Affects-Repos: [agent-bot-hq, agent-bot, agent-bot-machine, soul-contracts, agent-bot-comms]
Affects: [R2, R9, QA-A11Y-01, hq-v1, control-v1, identity-service-api, catalog-signing, daemon-machine-channel, mcp-tools, trust-model, topology]
---

# PDR-0047 Harbor is the control plane of a linked machine; HQ alone stays a complete deployment

HQ with no Harbor link is a complete, supported deployment. When the owner links a machine, Harbor becomes its control plane: Harbor decides policy and lifecycle, and HQ remains the only place anything is enforced or executed. The most important consequence: a compromised Harbor can stop work on a linked machine but cannot add authority to it, because every action that adds authority carries the owner's device presence signature and is verified on the host.

## Context

- R2 said only local HQ controls lifecycle and protected operations, and S6 §4 allows remote administration only through a tunnel the owner opens. PDR-0023 gave Harbor a read-only projection with no control path.
- On 2026-11-11 the owner set a different direction (DRIFT-019): the local piece is open source and may never link to Harbor; Harbor is parity with local plus the wider machine network; once a machine links, Harbor is the control plane. Harbor and the local piece share one implementation, with Harbor's features added on top.
- Two interface repositories existed without charters (DRIFT-020), and soul-contracts has no record for an owner session, device enrolment, a machine plan, or anything Harbor sends to HQ.

## Decision

1. **Two deployment modes.** *Local-only*: HQ, agent-bot-machine and the Souls, with no Harbor account. *Linked*: the same, plus Harbor. Local-only is a supported product, not a degraded profile.
2. **One core, Harbor as an add-on.** agent-bot-hq, its `hq/v1` owner API and the HQ interface are the only implementation of a machine. Harbor consumes the same contracts. No core component requires Harbor to build, install, run or pass conformance, and Harbor's view of one machine renders the same `hq/v1` records as the local interface.
3. **When linked, Harbor decides and HQ enforces.** Harbor is the authority for the machine's policy and lifecycle decisions. HQ is the only enforcement and execution point; no remote tier gets a shell or an execution channel. Harbor reaches HQ only with signed records that HQ validates against its current signed policy.
4. **Three classes of action.**
   - *Reduce* (stop, deny, revoke, quarantine): a Harbor signature is enough.
   - *Operate inside policy* (start, restart or drain an admitted Soul; offer a task): a Harbor signature under the owner's link grant; HQ refuses anything the signed policy does not already allow.
   - *Widen* (a policy write that adds authority, harness account creation, key or credential provisioning, installs, machine plans, link changes): the record carries the owner's device presence signature. Harbor relays it and cannot originate it. HQ and agent-bot-machine each verify it, whatever path it arrived on (agent-bot-hq D4).
5. **Local override is deny-only while linked.** At the machine the owner can stop, deny, revoke and unlink. Granting beyond Harbor's policy needs an unlink first.
6. **Link loss fails closed.** HQ keeps enforcing the last signed policy, accepts only reduce actions and never widens. Work that needs no new credential continues (R9). Whether a signed policy expires while the link is down is unspecified here and is settled in the `control/v1` contract.
7. **Link and unlink happen at the machine.** Only the owner, with device presence, links or unlinks. Harbor cannot enrol a machine on its own or prevent an unlink. After an unlink the machine is local-only and holds its own policy and credentials.
8. **Control gets its own seam.** `control-v1` (provider agent-bot, consumers agent-bot-hq and agent-bot-machine, contract home soul-contracts `schemas/control/v1`) carries the signed policy bundle and the relayed owner request. `observation-v1` stays read-only as PDR-0023 decided, and message relays still carry no control, so T12 holds as written.
9. **R2 is reworded** in `registry/requirements.yaml`: "Only local HQ executes lifecycle and protected operations on its host. In a local-only deployment HQ also decides them. On a machine the owner has linked, Harbor decides and HQ enforces; an action that adds authority carries the owner's device presence signature, verified on the host. Relays deliver messages and presence; no remote tier obtains an execution channel."
10. **Interfaces per plane.**
    - *Local machine*: the HQ interface (agent-bot-hq-ui), the `agent-bot-hq` CLI and GeniusBar, all over `hq/v1` on the local socket. agent-bot-machine shows only the presence prompt.
    - *Fleet*: the Harbor console, shipped from agent-bot, designed in agent-bot-harbor-ui.
    - *One linked machine, opened from Harbor*: the remote machine view. It reuses the HQ interface's screens over `control-v1`; approving a machine plan there is a widen action.
    - *MCP apps*: HQ's MCP server locally, Harbor's owner-authenticated server when hosted.
11. **The two interface repositories get charters** in `registry/repos.yaml` as design sources for agent-bot-hq and agent-bot, before any work lands there. Every interface meets QA-A11Y-01. This amends PDR-0002's repository count; the web console still ships from agent-bot.
12. **Contracts first.** No implementation PR merges in any repository before the `control-v1` seam and these soul-contracts records exist with negative fixtures: the `control/v1` policy bundle and relayed owner request, owner session open and exchange, device enrolment and the link and unlink record, a machine-plan record, and a local-issuer variant of the credential issuance record. Status and receipt listing and MCP app payloads follow.
13. **Harbor's control signing key** is its own key, separate from the catalog and credential-minting keys, held under agent-bot's existing key custody and never in a repository or on a host. HQ pins its public key at link time under owner presence, and every `control/v1` record names the key.
    - *Rotation*: a record signed by the current key that also carries the owner's presence signature. HQ accepts no other change to the pinned key.
    - *Revocation*: the owner revokes at the machine, or with a record that carries owner presence. HQ then refuses every record from that key and acts as in point 6 until the owner links again.
    - No paid key service, hardware module or new provider account is approved here. If existing custody cannot meet this, that is a separate decision for the owner.
14. **Parity is a test.** soul-conformance shows that local-only HQ passes the full supported suite with Harbor unreachable.
15. **Federation stays off.** Fleet features are in scope. Federation waits for its cryptographic profile review (agent-bot-hq Q8, and "Federation cryptographic profile" in the [decision log](decision-log.md)).

## Acceptance

Option B was accepted on the owner's behalf on 2026-11-11 in the marked answer to [discussion #47](https://github.com/true-line/agent-bot-platform/discussions/47), with seven conditions. An agent posted that answer for the owner; the owner confirms it by merging this record. Points 4, 6, 9, 11, 12, 14 and 15 carry them, and point 13 records the key handling the answer asked this record to write down.

## Consequences

- **agent-bot-platform.** Done with this record: R2 reworded, `control-v1` added, the agent-bot charter changed and the architecture pages updated, which resolves DRIFT-019. Still to do: the two interface charters, which close DRIFT-020 with agent-bot-harbor-ui's README change, and tests in `registry/tests.yaml` for points 4, 5, 6, 13 and 14.
- **agent-bot-hq.** Verify and enforce `control/v1` records; classify every owner API call as reduce, operate or widen; keep the last signed policy; link, unlink, key pinning and revocation behind owner presence.
- **agent-bot (Harbor).** Author and sign policy; relay owner-signed requests unmodified; hold no code path that creates a widening record. Record the control key's custody and rotation schedule in its own ADR. Build fleet features over `hq/v1` records.
- **agent-bot-machine.** Verify owner presence itself for every widening action; store the linked policy; on unlink, hold local policy and credentials again.
- **soul-contracts.** Add the records in point 12, with error codes for a missing presence signature, a revoked key and an action outside policy.
- **agent-bot-comms.** No change to `wire/v1`.
- **agent-bot-hq-ui, agent-bot-harbor-ui.** Adopt the platform block. agent-bot-harbor-ui names the product Harbor and stops targeting agent-bot-ui; its `daemon-ui/` becomes the remote machine view.

## Alternatives considered

- **Keep R2 as written.** Smallest attack surface, but no fleet control, and DRIFT-019 stays open.
- **Give Harbor an execution channel.** One Harbor compromise owns every linked machine.
- **Two separate products.** Two implementations drift, and parity cannot be tested.
- **Carry control on the observation uplink.** PDR-0023 rejected mixing monitoring with control; a separate seam keeps the projection provably read-only.
