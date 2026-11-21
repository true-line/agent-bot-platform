---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-21
Date: 2026-11-12
Discussion: https://github.com/true-line/agent-bot-platform/discussions/52
Affects-Repos: [agent-bot-machine, agent-bot-hq, agent-bot-souls, soul-conformance]
Affects: [R3, trust-model]
---

# PDR-0052 Isolate network access at harness launch

The owner selected the process-isolation answer in [Discussion #52](https://github.com/true-line/agent-bot-platform/discussions/52). This accepted record reconciles that answer with Stage 2a. [PDR-0085](PDR-0085-macos-first-protected-pilot.md) sets macOS first.

## Context

Before the broker can identify a member's runtime, the SDK presents its launch token to Souls on the member socket and obtains its runtime binding. It then authenticates to the broker. Souls owns the token, its lifetime and its revocation. [Member bootstrap contract](https://github.com/true-line/agent-bot-hq/blob/main/docs/hq-member-bootstrap-client.md)

A launched harness needs its Unix broker socket. A direct network connection lets it reach a provider outside the broker's policy and audit. The owner raised a second concern with per-account firewall rules. They would have to coexist with every other firewall managing the host.

The [HQ migration plan, row 16c](https://github.com/true-line/agent-bot-hq/blob/a1e847cb36d7b0e825f810c8c3d4f16fdff6543d/docs/daemon-plugin-split.md#stage-2a-member-isolation-wp2) still recommends a per-account firewall. [Machine #497](https://github.com/true-line/agent-bot-machine/pull/497) installed Linux IPv4 and IPv6 rules. [Platform #68](https://github.com/true-line/agent-bot-platform/issues/68) tracks macOS qualification.

## Decision

1. On macOS, the launched harness may connect to two exact Unix socket paths from its launch assignment. One is its assigned broker. The other is the Souls member socket for that individual launch. Deny other socket destinations, including another launch's member socket in the same directory. Deny direct IP connections and carry network requests through the broker. Expanding these permissions requires explicit product-owner approval and recorded justification. Selection of a supported launcher and verification on each supported OS version remain implementation work. [Owner decision on the Souls socket](https://github.com/true-line/agent-bot-platform/discussions/52#discussioncomment-19773186)
2. On Linux, launch the harness in an empty network namespace. The selected design uses a Machine-installed, root-owned launcher restricted to provisioned accounts. It enters the namespace and permanently drops privileges to the selected account before running the harness. The authorization covers that launcher only.
3. Verify T03 through normal harness launch. A direct request to a reachable provider or service must fail, and the same operation through the broker must reach the service. On the declared macOS host, verify member authentication and broker binding through the assigned sockets and verify refusal on a different launch's socket. [Conformance catalog](../07-verification/conformance-catalog.md)

## Stage 2a managed account and broker assignment

The owner clarified that a managed Soul is started by HQ through Soul runner. Each
installed Soul gets one separate untrusted runner OS account; existing
per-harness credential accounts remain distinct. Independently started IDE,
CLI, and web agents are unmanaged. [Runner account decision](https://github.com/true-line/agent-bot-machine/issues/630#issuecomment-7068469234)

For a stock vendor client that cannot speak the HQ-hosted Comms protocol,
the proposed macOS assignment uses two separately confined processes:

- The vendor client runs as that Soul installation's runner UID. Its only
  outbound Unix paths are its per-start Souls member socket and one assigned
  local broker-relay HTTP socket.
- A credential-sidecar process runs as the distinct harness credential UID.
  Its only outbound Unix paths are the assigned HQ-hosted Comms broker and
  the same per-start member socket. It may bind only the exact local Unix
  listener assigned for the vendor client. It holds broad broker authority
  outside the runner UID; the runner receives only start-bound authority.

HQ starts the Soul through the reviewed Machine-installed rule. Any
runner-specific HQ admission occurs before vendor confinement or in a
separately reviewed control process; it is not a third outbound path for
the vendor client. The per-start member endpoint and local listener need
reviewed UID, group, mode, kernel peer identity, token lifetime, restart and
retirement checks. Existing direct broker clients retain the two-path
assignment in Decision 1.

This assignment changes the vendor client's assigned broker destination and
adds one exact sidecar listener bind. The owner explicitly approved this
PDR-0052 permission change on 2026-11-21 with the [recorded justification](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793):
stock vendor ACP cannot speak the HQ broker protocol while managed Souls
require HQ-hosted Comms and a separate runner UID. This approval grants no
third outbound path and does not authorize an installed production launcher.
The [fixture proof](https://github.com/true-line/soul-adapters/issues/4#issuecomment-7069138758)
and [Machine sidecar profile](https://github.com/true-line/agent-bot-machine/pull/638)
show socket feasibility, but use a shared test UID and do not qualify
production launch or physical T03. [Souls endpoint work](https://github.com/true-line/agent-bot-souls/issues/29)
remains open.

## Consequences

The owner assigned runtime launch to HQ in row 16b. Under that decision, Machine must install the rule through owner-reviewed provisioning. HQ must use the rule to start the adapter as the harness account selected at admission. Machine and keyd stay out of the runtime process tree. The [macOS socket policy fixture](https://github.com/true-line/agent-bot-machine/pull/583) verified both assigned sockets and refusal of sibling sockets and direct IP traffic. T03 still requires the production HQ launcher to apply the profile before starting the adapter and demonstrate the kernel identity, socket assignments and stop behavior. [HQ launch decision](https://github.com/true-line/agent-bot-hq/blob/adf3de1ef1f819712d54bfd53aff382c408684da/docs/daemon-plugin-split.md#stage-2a-member-isolation-wp2) · [Darwin provisioning work](https://github.com/true-line/agent-bot-machine/issues/585)

Each implementation must identify which processes it actually confines. Existing installations with per-account firewall rules need a separate migration that preserves isolation during transition. [DRIFT-024](../00-governance/drift-register.md#drift-024-harness-egress-isolation)

## Alternatives considered

Per-account firewall rules can interfere with other firewall managers. Leaving direct IP access available would let a harness bypass its broker. Discussion #52 also considered a per-harness systemd unit on Linux, which would change how HQ hands input and output to the launched process.
