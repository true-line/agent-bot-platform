---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-11
Date: 2026-11-11
Discussion: https://github.com/true-line/agent-bot-platform/discussions/47
Affects-Repos: [agent-bot-hq, agent-bot, agent-bot-machine, soul-contracts, agent-bot-comms]
Affects: [R2, R9, hq-v1, identity-service-api, catalog-signing, daemon-machine-channel, mcp-tools, trust-model, topology]
---

# PDR-0047 Harbor is the control plane of a linked machine; HQ alone stays a complete deployment

HQ with no Harbor link is a complete, supported deployment. When the owner links a machine, Harbor becomes its control plane: Harbor decides policy and lifecycle, and HQ remains the only place anything is enforced or executed. The most important consequence: a compromised Harbor can stop work on a linked machine but cannot add authority to it, because every action that adds authority carries the owner's device presence signature and is verified on the host.

## Context

- R2 (Approved) says only local HQ controls lifecycle and protected operations, and S6 §4 allows remote administration only through a tunnel the owner opens. PDR-0023 gave Harbor a read-only projection with no control path.
- On 2026-11-11 the owner set a different direction (DRIFT-017): the local piece is open source and may never link to Harbor; local holds everything needed to make local work; Harbor is parity with local plus the wider machine network; and once a machine links, Harbor is the control plane, described as a more secure control plane plus agent federation.
- The owner also directed that Harbor and the local piece share one implementation: build the local core once and add Harbor's features on top, not two builds of the same thing.
- Two interface repositories exist without charters (DRIFT-018), and nothing records which plane each interface belongs to.
- soul-contracts has no records for an owner session, device enrollment, a machine plan, or anything Harbor sends to HQ, so every one of these would otherwise be invented per repository.

## Decision

1. **Two deployment modes.** *Local-only*: HQ, agent-bot-machine and the Souls, with no Harbor account. *Linked*: the same, plus Harbor. Local-only is a supported product, not a degraded profile. The test: with Harbor unreachable or never configured, no rule becomes unenforced.
2. **One core, Harbor as an add-on.** agent-bot-hq, its `hq/v1` owner API and the HQ interface are the only implementation of a machine. Harbor's features are an add-on that consumes the same contracts. Dependencies point one way: no core component requires Harbor to build, install, run or pass conformance. Harbor's view of one machine renders the same `hq/v1` records as the local interface; there is no second implementation of machine settings.
3. **When linked, Harbor decides and HQ enforces.** Harbor is the authority for the linked machine's policy and lifecycle decisions. HQ is still the only enforcement and execution point, and no remote tier gets a shell or an execution channel. Harbor reaches HQ only with signed records that HQ validates against its current signed policy.
4. **Three classes of action.**
   - *Reduce* (stop, deny, revoke, quarantine): a Harbor signature is enough.
   - *Operate inside policy* (start, restart or drain an admitted Soul; offer a task): a Harbor signature under the owner's link grant; HQ refuses anything the current signed policy does not already allow.
   - *Widen* (a policy write that adds authority, member or account creation, key or credential provisioning, installs, machine plans, link changes): the record carries the owner's device presence signature. Harbor relays it and cannot originate it. HQ and agent-bot-machine each verify it (agent-bot-hq D4).
5. **Local override is deny-only while linked.** At the machine the owner can stop, deny, revoke and unlink. Granting beyond Harbor's policy needs an unlink first.
6. **Link loss fails safe.** HQ keeps enforcing the last signed policy and issues nothing beyond it. Work that needs no new credential continues (R9). Policy carries an expiry; after it, HQ refuses widening actions until the link returns or the owner unlinks.
7. **Link and unlink happen at the machine.** Only the owner, with device presence, links or unlinks. Harbor cannot enrol a machine on its own or prevent an unlink. After an unlink the machine is local-only and holds its own policy and credentials (agent-bot-hq D4).
8. **Control gets its own seam.** A new seam `control-v1` (provider agent-bot, consumers agent-bot-hq and agent-bot-machine, contract home soul-contracts `schemas/control/v1`) carries the signed policy bundle and the relayed owner request. `observation-v1` stays read-only as PDR-0023 decided, and message relays still carry no control, so T12 holds as written.
9. **R2 is reworded.** New statement, recorded in `registry/requirements.yaml`: "Only local HQ executes lifecycle and protected operations on its host. In a local-only deployment HQ also decides them. On a machine the owner has linked, Harbor decides and HQ enforces; an action that adds authority carries the owner's device presence signature, verified on the host. Relays deliver messages and presence; no remote tier obtains an execution channel."
10. **Interfaces per plane.**

    | Interface | Plane | Talks to | Home |
    |---|---|---|---|
    | HQ interface | Local machine | `hq/v1` owner API over the local socket | agent-bot-hq-ui |
    | `agent-bot-hq` CLI and GeniusBar | Local machine | `hq/v1` | agent-bot-hq, geniusbar |
    | Presence prompt | Local machine | Secure Enclave | agent-bot-machine (no other interface) |
    | Harbor console | Fleet | Harbor API | agent-bot, designs in agent-bot-harbor-ui |
    | Remote machine view | One linked machine, opened from Harbor | `hq/v1` records through `control-v1` | Reuses the HQ interface's screens |
    | MCP apps | Either | HQ's MCP server locally, Harbor's owner-authenticated server when hosted | agent-bot-harbor-ui `mcp-apps/` |

    Machine plans are approved in the HQ interface, or from the remote machine view as a *widen* action under point 4.
11. **The two interface repositories get charters.** agent-bot-hq-ui and agent-bot-harbor-ui are added to `registry/repos.yaml` as design sources for agent-bot-hq and agent-bot. This amends PDR-0002's count; the web console still ships from agent-bot.
12. **Contracts first.** soul-contracts gains, with negative fixtures, before any implementation: owner session open and exchange; status and receipt listing; device enrolment and the link and unlink record; the `control/v1` policy bundle and relayed owner request; a machine-plan record; a local-issuer variant of the credential issuance record; MCP app payloads.

## Consequences

- **agent-bot-platform.** Reword R2; add `control-v1` to `registry/seams.yaml`; add tests to `registry/tests.yaml` for: a Harbor-originated widening request without owner presence is refused by HQ and by agent-bot-machine; link loss keeps the last signed policy; the core passes conformance with Harbor unreachable; local override cannot grant while linked. Update the agent-bot charter (it may hold decision authority for linked machines, never execution) and add the two interface charters. Update the overview, federation and trust-domain pages. Close the "Owner authentication" open decision: the socket for local, `control-v1` for linked, the tunnel as the fallback. Resolves DRIFT-017 and DRIFT-018.
- **agent-bot-hq.** Verify and enforce `control/v1` records; classify every owner API call as reduce, operate or widen; persist the last signed policy with its expiry; implement link and unlink behind owner presence; expose nothing that executes on a Harbor signature alone beyond the reduce and operate classes.
- **agent-bot (Harbor).** Author and sign policy; relay owner-signed requests unmodified; hold no code path that creates a widening record. Protect the control signing key as it protects the catalog key. Build fleet and federation features over `hq/v1` records.
- **agent-bot-machine.** Verify owner presence itself for every widening action regardless of the path it arrived on; store the linked policy and its expiry; on unlink, return to holding local policy and credentials.
- **soul-contracts.** Add the records in point 12 and error codes for a missing presence signature, an expired policy and an action outside policy.
- **agent-bot-comms.** No change to `wire/v1`. Relays keep carrying messages and presence only.
- **agent-bot-hq-ui, agent-bot-harbor-ui.** Adopt the platform block. agent-bot-harbor-ui renames to Harbor in its README and stops targeting agent-bot-ui. Its `daemon-ui/` becomes the remote machine view built from the HQ interface's screens.

## Alternatives considered

- **Keep R2 as written.** Smallest attack surface, but no fleet control and it contradicts the owner's direction.
- **Give Harbor an execution channel.** Simplest fleet operations; one Harbor compromise owns every linked machine.
- **Two separate products.** No trust-model change locally, but two implementations drift and parity cannot be tested.
- **Carry control on the observation uplink.** One channel to build. PDR-0023 already rejected mixing monitoring with control, and a separate seam keeps the read-only projection provably read-only.
