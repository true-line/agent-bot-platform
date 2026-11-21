---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-21
Date: 2026-11-12
Discussion: https://github.com/true-line/agent-bot-platform/discussions/52
Affects-Repos: [agent-bot-machine, agent-bot-hq, agent-bot-souls, soul-conformance]
Affects: [R3, trust-model]
---

# PDR-0052 Isolate network access at harness launch

The owner selected the process-isolation answer in [Discussion #52](https://github.com/true-line/agent-bot-platform/discussions/52). The current main-branch record and its [Stage 2a relay amendment](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793) are accepted. This draft [tracks a further change](https://github.com/true-line/agent-bot-platform/issues/113) to the relay credential principal; the accepted main-branch rule remains in force until the owner approves and this amendment merges. [PDR-0085](PDR-0085-macos-first-protected-pilot.md) sets macOS first.

## Context

Before the broker can identify a member's runtime, the SDK presents its launch token to Souls on the member socket and obtains its runtime binding. It then authenticates to the broker. Souls owns the token, its lifetime and its revocation. [Member bootstrap contract](https://github.com/true-line/agent-bot-hq/blob/main/docs/hq-member-bootstrap-client.md)

A launched harness needs its Unix broker socket. A direct network connection lets it reach a provider outside the broker's policy and audit. The owner raised a second concern with per-account firewall rules. They would have to coexist with every other firewall managing the host.

The [HQ migration plan, row 16c](https://github.com/true-line/agent-bot-hq/blob/a1e847cb36d7b0e825f810c8c3d4f16fdff6543d/docs/daemon-plugin-split.md#stage-2a-member-isolation-wp2) still recommends a per-account firewall. [Machine #497](https://github.com/true-line/agent-bot-machine/pull/497) installed Linux IPv4 and IPv6 rules. [Platform #68](https://github.com/true-line/agent-bot-platform/issues/68) tracks macOS qualification.

## Decision

1. On macOS, the launched harness may connect to two exact Unix socket paths from its launch assignment. One is its assigned broker. The other is the Souls member socket for that individual launch. Deny other socket destinations, including another launch's member socket in the same directory. Deny direct IP connections and carry network requests through the broker. Expanding these permissions requires explicit product-owner approval and recorded justification. Selection of a supported launcher and verification on each supported OS version remain implementation work. [Owner decision on the Souls socket](https://github.com/true-line/agent-bot-platform/discussions/52#discussioncomment-19773186)
2. On Linux, launch the harness in an empty network namespace. The selected design uses a Machine-installed, root-owned launcher restricted to provisioned accounts. It enters the namespace and permanently drops privileges to the selected account before running the harness. The authorization covers that launcher only.
3. Verify T03 through normal harness launch. A direct request to a reachable provider or service must fail, and the same operation through the broker must reach the service. On the declared macOS host, verify member authentication and broker binding through the assigned sockets and verify refusal on a different launch's socket. [Conformance catalog](../07-verification/conformance-catalog.md)

## Proposed Stage 2a bridge credential amendment

The owner clarified that a managed Soul is started by HQ through Soul runner. Each
installed Soul gets one separate untrusted runner OS account; existing
per-harness credential accounts remain distinct. Independently started IDE,
CLI, and web agents are unmanaged. [Runner account decision](https://github.com/true-line/agent-bot-machine/issues/630#issuecomment-7068469234)

For a stock vendor client that cannot speak the HQ-hosted Comms protocol,
retain two separately confined processes. This proposal changes only the
credential-sidecar principal in the [previously approved relay assignment](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793):

- The vendor client runs as that Soul installation's runner UID. Its only
  outbound Unix paths are its per-start Souls member socket and one assigned
  local broker-relay HTTP socket.
- A bridge sidecar runs as a dedicated bridge credential UID **B**, one per
  Soul installation. B is distinct from the installation's runner UID **R**,
  every shared per-harness credential UID **C**, HQ, and Machine. B has a
  private account and `0700` state directory and is never reused for another Soul
  installation. Its only outbound Unix paths are its assigned HQ-hosted Comms
  broker and the same per-start member socket. It may bind only the exact
  local Unix listener assigned for R. B holds broad broker authority; R gets
  only start-bound authority. Existing C accounts remain for direct broker
  clients and must not receive this sidecar's broad token.

The three endpoints have independent, exact assignments. Machine provisions
their parent directories and checks ownership, group, modes, and identity
before launch; HQ verifies the signed assignment and kernel peer identity:

| Endpoint | Parent and socket | Permitted peer and authority |
| --- | --- | --- |
| HQ Comms broker for this installation | HQ-owned parent, B-private group, mode `2750`; HQ-owned socket, B-private group, mode `0660` | Only kernel peer UID B, with keyed HMAC proof bound by HQ to the Machine-authenticated installation, start, plan, and runtime. C, R, other B identities, and old starts are refused. The existing C broker endpoint is not widened. |
| Per-start Souls member | R-owned parent, B-private group, mode `2750`; R-owned socket, B-private group, mode `0660` | Only the assigned R and B kernel peer UIDs with start-scoped member authentication. R may obtain its own start binding but cannot obtain B's broker proof, channel binding secret, or broad token. |
| Local broker-relay HTTP | B-owned parent, R-private group, mode `2750`; B-owned socket, R-private group, mode `0660` | Only the assigned R kernel peer UID, authenticated to this installation/start/plan. HTTP headers, including vendor API placeholders, confer no authority. B alone may bind and replace this listener. |

Mode and group checks are necessary but do not replace kernel peer checks or
start binding. The protected launch refuses ownership, mode, socket inode,
group, or peer mismatch and retires the endpoints after the start stops. B's
broker proof and state remain inaccessible to R, C, and other B identities.
The shared C account cannot own or read B's private state or unlink B's
listener. B cannot use another installation's endpoints.

The exact macOS sandbox assignments retain two outbound Unix paths per
confined process: R may connect only to its member and HTTP relay; B may
connect only to that member and its dedicated HQ broker. B alone has one
literal HTTP listener bind. Both deny direct IPv4/IPv6 and sibling Unix
destinations. A separate control process, if used for HQ admission, needs
its own reviewed policy and cannot add an outbound path to R or B.

HQ starts the Soul through the reviewed Machine-installed rule. Initial HQ
admission and `launch.attach` must use the signed runner-specific admission
endpoint, never an implicit `hqHome/admission.sock`. A member bearer or
`launch.attach` result visible to R must not disclose B's broad broker
material; B receives that material through a separate B-only authenticated
handoff. Before HQ starts the vendor client, B must complete an actual HQ
Comms HMAC bind for the assigned start. An HTTP listener, HQ hello, or member
socket alone is insufficient readiness; failed binding stops launch and
cleans up endpoints. Existing direct broker clients retain Decision 1.

The [prior owner approval](https://github.com/true-line/agent-bot-platform/pull/111#issuecomment-7069182793)
covered a sidecar under C. It does not authorize this B account, HQ broker
peer delegation, B-only token handoff, or replacement listener custody.
The justification for asking approval is a [same-C negative probe](https://github.com/true-line/agent-bot-hq/issues/231#issuecomment-7069283897):
another process under the shared credential UID read a `0600` sidecar token
and unlinked its live `0660` socket in a UID-owned `0750` parent. The network
sandbox cannot stop those file operations. Thus C cannot hold protected broad
sidecar authority. [Distinct-R fixture evidence](https://github.com/true-line/soul-adapters/issues/4#issuecomment-7069253198)
shows the proposed group-visible socket path works, but it does not prove
production B handoff, installed launch, or physical T03. This proposed
principal change requires a separate explicit owner approval and recorded
justification before the protected profile can use it.

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

The owner assigned runtime launch to HQ in row 16b. Machine must install the fixed rules through owner-reviewed provisioning. For a direct broker client, HQ starts the adapter as the harness credential account selected at admission. Under this proposed managed stock-vendor assignment, HQ starts Soul runner under R and a separately confined broker sidecar under B. Machine and keyd stay out of the runtime process tree. The [macOS socket policy fixture](https://github.com/true-line/agent-bot-machine/pull/583) verified two assigned sockets and refusal of sibling sockets and direct IP traffic, but not this B endpoint custody. T03 requires the production HQ launcher to apply the exact profile to each process before starting the adapter and demonstrate both kernel identities, socket assignments, token custody and stop behavior. [HQ launch decision](https://github.com/true-line/agent-bot-hq/blob/adf3de1ef1f819712d54bfd53aff382c408684da/docs/daemon-plugin-split.md#stage-2a-member-isolation-wp2) · [Darwin provisioning work](https://github.com/true-line/agent-bot-machine/issues/585)

Each implementation must identify which processes it actually confines. Existing installations with per-account firewall rules need a separate migration that preserves isolation during transition. [DRIFT-024](../00-governance/drift-register.md#drift-024-harness-egress-isolation)

## Alternatives considered

Per-account firewall rules can interfere with other firewall managers. Leaving direct IP access available would let a harness bypass its broker. Discussion #52 also considered a per-harness systemd unit on Linux, which would change how HQ hands input and output to the launched process.
