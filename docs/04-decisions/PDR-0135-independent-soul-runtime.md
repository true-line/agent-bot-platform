---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-26
Date: 2026-11-26
Discussion: https://github.com/true-line/agent-bot-platform/discussions/135
Affects-Repos: [agent-bot-platform, agent-bot, agent-bot-hq, agent-bot-souls, agent-bot-comms, agent-bot-machine, soul-adapters, soul-conformance]
Affects: [R11, hq-plugin-contract, hq-v1, wire-v1, acp-front-door, trust-model, scope]
---

# PDR-0135 Keep Souls independent of HQ and defer IDE integration

The owner directed that Souls run independently, that HQ be able to start a Soul across an account boundary, and that terminal chat suffice for the MVP. This proposal records that direction for cross-repository adoption. [Decision discussion and owner clarifications](https://github.com/true-line/agent-bot-platform/discussions/135#discussioncomment-19939806)

## Component boundary

1. A user can start a Soul without HQ or Harbor. Souls supervises its harnesses, applies the package's policies and manages sessions, configuration and recovery. Each harness owns its provider configuration and model calls. Harness adapters connect Souls to a harness’s session and lifecycle interfaces.
2. HQ can also start the Soul through its runner. The runtime and its agents execute outside the HQ service account. Clients in standard and service accounts call HQ through its authenticated API. HQ's code and private state are inaccessible to those agents, and HQ has no access to users' private account data.
3. HQ admits the managed runtime, verifies grants and handles lifecycle requests. HQ relays cross-machine Comms frames to and from Harbor. Harbor routes them between linked machines and Comms delivers them to agents. Agent network management, communications restrictions and model inference remain outside HQ’s remit. Registering a component's control interface with HQ conveys only the authority specified by that interface.
4. HQ handles its own Harbor control traffic and the network exchanges required on Machine's behalf. The signed local channel, Machine's independent checks, administrative custody and the explicit standalone signing exception continue to follow PDR-0047, PDR-0091 and PDR-0093.
5. R11's pilot rubric is a bounded task completed through one terminal conversation. The user can inspect which harness did the work without having to configure or switch individual sessions. IDE-facing ACP is a possible later integration. Per-harness ACP adapters have a separate role inside Souls.

## Consequences

PDR-0037 described a comms broker plugin hosted in HQ. PDR-0052 and PDR-0102 and the Stage 2a interface record specify evidence for that layout. The cross-machine relay is part of HQ. Its forwarding role alone does not determine the protected broker placement or endpoint contract. DRIFT-028 tracks reconciliation. A diagram or an existing result for the earlier layout cannot qualify a changed path.

HQ and Souls must demonstrate both independent start and an HQ start across the account boundary. Comms, HQ, Machine and conformance must reconcile the affected broker bindings and qualify the exact released path before claiming a protected profile. The host isolation, custody and evidence requirements still apply. The scope, R11 rubric and seam catalog distinguish IDE integration from harness adapters.

## Alternatives considered

Hosting the runtime in HQ would couple agent execution to the service account. Cross-machine delivery requires forwarding a frame, which HQ can do while the Soul runs independently. Requiring an ACP editor client in the pilot would make editor integration a prerequisite for demonstrating the single-Soul user experience.
