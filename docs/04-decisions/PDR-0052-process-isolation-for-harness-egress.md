---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-21
Date: 2026-11-12
Accepted: 2026-11-21
Discussion: https://github.com/true-line/agent-bot-platform/discussions/52
Affects-Repos: [agent-bot-machine, agent-bot-hq, agent-bot-souls, soul-conformance]
Affects: [R3, trust-model]
---

# PDR-0052 Isolate network access at harness launch

The owner selected process isolation in [Discussion #52](https://github.com/true-line/agent-bot-platform/discussions/52), approved the [relay assignment](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793), and approved this [per-installation bridge credential amendment](https://github.com/true-line/agent-bot-platform/pull/114#issuecomment-7069861743) on 2026-11-21. [PDR-0085](PDR-0085-macos-first-protected-pilot.md) sets macOS first.

## Context

The SDK obtains its runtime binding from Souls over the member socket, then authenticates to the broker. Souls owns the member token and revocation. Direct network access could bypass broker policy and audit. Per-account firewall rules could conflict with host firewalls. [Member bootstrap contract](https://github.com/true-line/agent-bot-hq/blob/main/docs/hq-member-bootstrap-client.md) · [Platform #68](https://github.com/true-line/agent-bot-platform/issues/68)

## Decision

1. On macOS, the launched harness may connect to two exact Unix socket paths from its launch assignment. One is its assigned broker. The other is the Souls member socket for that individual launch. Deny other socket destinations, including another launch's member socket in the same directory. Deny direct IP connections and carry network requests through the broker. Expanding these permissions requires explicit product-owner approval and recorded justification. Selection of a supported launcher and verification on each supported OS version remain implementation work. [Owner decision on the Souls socket](https://github.com/true-line/agent-bot-platform/discussions/52#discussioncomment-19773186)
2. On Linux, launch the harness in an empty network namespace. The selected design uses a Machine-installed, root-owned launcher restricted to provisioned accounts. It enters the namespace and permanently drops privileges to the selected account before running the harness. The authorization covers that launcher only.
3. Verify T03 through normal harness launch. A direct request to a reachable provider or service must fail, and the same operation through the broker must reach the service. On the declared macOS host, verify member authentication and broker binding through the assigned sockets and verify refusal on a different launch's socket. [Conformance catalog](../07-verification/conformance-catalog.md)

## Stage 2a bridge credential assignment

HQ starts managed Souls through Soul runner. Each installation has a separate
untrusted runner account; existing per-harness credential accounts remain.
IDE, CLI and web agents not started by HQ are unmanaged. [Runner account decision](https://github.com/true-line/agent-bot-machine/issues/630#issuecomment-7068469234)

For a stock vendor client that cannot speak HQ-hosted Comms, retain two
confined processes but change the [approved sidecar principal](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793):

- The vendor client runs as that Soul installation's runner UID. Its only
  outbound Unix paths are its per-start Souls member socket and one assigned
  local broker-relay HTTP socket.
- A bridge sidecar runs as dedicated UID **B**, one per Soul installation,
  distinct from runner **R**, shared harness credential **C**, HQ and Machine.
  B has private `0700` state. It may connect only to its HQ Comms broker and
  member socket and bind only R's exact HTTP listener. B holds broad broker
  authority; R gets start-bound authority. C remains for direct broker clients.

Machine provisions three exact endpoints; HQ verifies its signed assignment
and kernel peer identity:

| Endpoint | Parent and socket | Permitted peer and authority |
| --- | --- | --- |
| HQ Comms broker | HQ-owned parent `2750`, socket `0660`, B-private group | Peer UID B and HMAC bound to Machine-authenticated installation/start/plan/runtime; refuse C, R, other B and old starts. C's broker is unchanged. |
| Per-start Souls member | R-owned parent `2750`, socket `0660`, B-private group | Assigned R/B peers with start-scoped authentication. R cannot obtain B's broker binding or broad token. |
| Local HTTP relay | B-owned parent `2750`, socket `0660`, R-private group | Peer UID R with installation/start/plan binding. Headers grant no authority. Only B binds or replaces it. |

Refuse owner, group, mode, inode or peer mismatch; retire endpoints on stop.
R, C and other B identities cannot read B's proof or state, replace its
listener or use its endpoints. Mode checks do not replace kernel peer checks.

Each macOS process retains two outbound paths: R to member and HTTP; B to
member and dedicated HQ broker. B has one exact HTTP bind. Both deny direct
IPv4/IPv6 and sibling Unix paths. A separate HQ control process needs its own
reviewed policy; it cannot add an R/B outbound path.

HQ starts the Soul through the reviewed Machine-installed rule. Initial HQ
admission and `launch.attach` must use the signed runner-specific admission
endpoint, never an implicit `hqHome/admission.sock`. A member bearer or
`launch.attach` result visible to R must not disclose B's broad broker
material; B receives that material through a separate B-only authenticated
handoff. Before HQ starts the vendor client, B must complete an actual HQ
Comms HMAC bind for the assigned start. An HTTP listener, HQ hello, or member
socket alone is insufficient readiness; failed binding stops launch and
cleans up endpoints. Existing direct broker clients retain Decision 1.

The [prior approval](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793)
covered C, not B or its broker delegation. In a [same-C probe](https://github.com/true-line/agent-bot-hq/issues/231#issuecomment-7069283897),
another C process read a `0600` token and unlinked a live `0660` listener.
Network sandboxing cannot stop same-UID file operations, so C cannot hold
protected broad sidecar authority. [Distinct-R fixture evidence](https://github.com/true-line/soul-adapters/issues/4#issuecomment-7069253198)
does not prove production B custody or physical T03. The owner approved
this exact B assignment on 2026-11-21 because shared C permits same-UID
token access and listener removal. That approval does not enable a protected
launcher or satisfy T03.

Migration is fail closed. Existing C direct broker clients and the accepted
two-path rule remain unchanged. C/R sidecar fixtures may provide cooperative
evidence only. Machine provisions B and all three assigned endpoints from an
owner-reviewed plan; HQ and Souls refuse a protected start until B custody,
the runner/member handoff, and the pre-ACP HMAC bind are implemented. There is
no protected fallback to C or a generic HQ socket when B is unavailable.
On stop, revoke the start-bound tokens and endpoint assignments, remove its
listener and member endpoint, and leave other installations and C accounts
intact.

Acceptance must show C and R cannot read B's token or replace its listener;
other B identities cannot use its endpoints; wrong kernel peer UID is refused
even when group access permits a connection; stale, replayed, and mismatched
start/plan/broker proofs are refused across HQ restart. The installed profiles
must deny sibling sockets and direct IPv4/IPv6 for each process, and a failed
HMAC bind must prevent ACP startup and clean up. A physical host run still
must establish T01–T03 and T21 before any protected claim.

## Consequences

HQ starts Soul runner under R and a confined sidecar under B; Machine/keyd
stay out of their runtime process tree. Machine installs fixed rules through
owner-reviewed provisioning. [Socket fixture #583](https://github.com/true-line/agent-bot-machine/pull/583)
does not prove B custody. T03 needs installed dual-process profiles, kernel
identities, token custody and stop behavior. [HQ launch decision](https://github.com/true-line/agent-bot-hq/blob/adf3de1ef1f819712d54bfd53aff382c408684da/docs/daemon-plugin-split.md#stage-2a-member-isolation-wp2)

Each implementation must identify which processes it actually confines. Existing installations with per-account firewall rules need a separate migration that preserves isolation during transition. [DRIFT-024](../00-governance/drift-register.md#drift-024-harness-egress-isolation)

## Alternatives considered

Per-account firewall rules can interfere with other firewall managers. Leaving direct IP access available would let a harness bypass its broker. Discussion #52 also considered a per-harness systemd unit on Linux, which would change how HQ hands input and output to the launched process.
