---
Status: Frozen
Doc-Type: paper
Owner: product-owner
Last-Reviewed: 2026-11-05
---

# Agent Communications and Trustworthy Coordination — Proposed Outline

> Converted from `Agent Communications and Trustworthy Coordination proposed outline.docx` with scripts/docx2md.py — best-effort; curate before treating as normative.

Agent Communications and Trustworthy Coordination: proposed outline

Oct 24, 2026 · True Line AI

*Outline draft 0.2. Synchronized with Soul Agent System Architecture draft 0.2 and Native Shareable Soul Packages draft 0.3.*

This paper defines how Souls, their members, HQ and outside parties exchange messages and coordinate work, and which guarantees each exchange carries. It is the third companion paper and owns what the others defer:

| Paper | Status | Owns |
| --- | --- | --- |
| Soul Agent System Architecture | Draft 0.2 | How the parts fit: five tiers, split planes, HQ, the Soul meta-harness, memory and sleep, invariants |
| Native Shareable Soul Packages | Draft 0.3 | Package layout, data classes, content-addressed manifest, transfer profiles (life transfer, template, fork), export selection |
| Agent Identity and Delegated Authority | Draft 0.1 | Who is speaking, what they may do, opaque grant handles, attribution and receipts |
| Agent Communications and Trustworthy Coordination (this paper) | Outline 0.2 | Transport and tiers, two-layer envelopes, delivery and causal ordering, wake bridge, task leases, participation presets, HQ directives and queries, federation, external gateways |

It uses the architecture and identity papers' entities (Soul, member, installation, installation epoch, runtime, session, definition revision) unchanged and never defines authority itself; it carries, checks and enforces grants that HQ and the identity contract issue.

Proposed sections

Each section lists the questions it must answer.

1. Purpose, scope and invariants

- What a message, a task, a conversation and a receipt are, and what this paper leaves to its companions.
- Deciding vs. enforcing: how agent-comms checks budgets and task authority inside the Soul while HQ's broker enforces grants and holds keys outside the Soul's trust domain.
- Trust assumptions: which services are trusted to enforce (managed-machine HQ, local broker), and which inputs, relays or peers may be mistaken, partitioned or adversarial.

2. Participants and channels

- Entity taxonomy: the lead harness and regional harnesses inside a Soul, the Soul's entry point, HQ, principals (humans), peer Souls, and external agents and services.
- Which channel each pair uses (hq/v1 control socket, broker envelopes, internal ACP sessions), and which pairs are never directly connected (regional harnesses never message each other or external services directly; upstream hubs never connect to hq/v1).

3. Tiers, topology and federation

- Five tiers, two planes: harnesses (tier 5) talk to the Soul entry point (tier 4) over ACP; the Soul, HQ (tier 3), site hub (tier 2) and cloud mesh (tier 1) speak one broker wire over outbound uplinks.
- Split planes: messaging and presence federate upward; control (hq/v1) stays on the machine.
- Enrollment of site and cloud nodes (per-node Ed25519 key plus one-time owner code in GeniusBar; pluggable authenticators for tunnels, OAuth and Kerberos later).
- Relay custody: what a site or cloud relay can see, and what works when an uplink is missing.

4. Addressing, epochs and presence

- Soul IDs vs. installation IDs vs. member IDs; aliases resolved only within a known namespace.
- Installation epochs: how HQ fences stale installations when a Soul moves or recovers from partition.
- Presence as scoped, expiring reachability leases, not proof of a running process.
- How routes are learned and expired up and down the tree.

5. The wire

- NDJSON framing on every tier and canonical JSON for signed parts.
- Two-layer envelope: relay-visible outer routing frame (destination Soul ID, installation epoch, TTL, wake class, size, deduplication ID) vs. endpoint-sealed inner envelope (sender membership, recipient, task/conversation correlation, taint classification, opaque grant handle, payload).
- Versioning: N and N-1 at every hop, capability negotiation on connect, unknown required fields fail closed.

6. Delivery semantics

- Durable mailbox, store-and-forward, retention, and mailbox deduplication watermarks kept in the Soul's durable comms/ area and carried by life transfer when a Soul moves.
- At-least-once delivery with stable message IDs and deduplication; causal ordering scope (per conversation, or per task when one exists, never global).
- Grant validity across time: send-time verification vs. wake/consume-time verification, and how revocation or cancellation preempts queued messages.
- Backpressure, size limits, poison-pill quarantine after N failed deliveries, and what a sender learns about delivery ("queued, Soul unavailable").
- The comms/ record format (watermarks, task leases, open tasks, durable handoff notes), proposed for adoption by the Soul paper's layout.

7. Waking across the split plane

- How an inbound message on the messaging plane reaches an idle Soul: warm session delivery, cold wake via local HQ over hq/v1, or queue until clock-in.
- Who may wake whom, taint/classification gates on wake, and wake budgets.

8. Tasks and coordination

- Offer, accept, lease heartbeat, update, complete, cancel; why the lead holds task authority while regional members only propose.
- Proposals vs. commitments when several members, understudies or peer endpoints answer one task.
- Duplicate delivery, competing workers, bounded task leases, and idempotent transitions during brain recovery (Resume).

9. Conversation participation

- Presets: quiet (default), chatty, goal-oriented, with concrete limits on initiation, frequency, follow-ups and cost.
- One Soul-level send budget enforced by agent-comms across all harnesses; stop rules, closure and authorized reopening.
- The conversation record: purpose, evidence, commitments and last meaningful progress.

10. Communication inside a Soul

- Lead-to-region orchestration over ACP sessions under the Soul's entry point.
- Handoff through source-classified typed notes (decision, finding, commitment, open question, handoff) in tmp/notes/ and durable handoff state in comms/, never private harness transcripts.
- Taint and disclosure restrictions following derived outputs across regions, destination-checked understudies and sleep consolidation.

11. HQ channels

- Lifecycle (hq/v1 over protected local socket: start, stop, pause, drain, sleep, move, fork, retire), directives (HQ to Soul, broker envelope kind directive carrying a standing grant), and queries (Soul to HQ, broker envelope kind query returning decision records).
- Clock-in (Hello, Admit, Equip on hq/v1; Brief on broker; Ready and Lease on hq/v1) and Clock-out (drain, settle, report, nap, and life transfer on move).
- Standalone mode: running the same three channels against the entry point's local stub, recorded in every receipt as profile: standalone-unenforced.

12. Peer Souls and exposed specialists

- Admission on both sides; peer instructions arrive as requests and task offers, never owner directives.
- Direct endpoints for a delegated specialist capability without opening the rest of the Soul.

13. External gateways and brokered inference

- A2A, MCP, chat platforms (Slack, Telegram) and email: mapping inbound turns to tainted envelopes (external-untrusted) and tasks.
- One egress point per Soul through agent-comms for third-party services, enforcing destination policy and taint clearance.
- Brokered inference: how model calls route through HQ's broker under the protected profile, how the broker checks each provider destination against the task's grant and data classification, and the short-lived per-provider token fallback for harnesses that cannot use a proxy.

14. Receipts, observability and failure

- Send, delivery, wake and task-transition receipts that name the active enforcement profile and feed the identity paper's action records.
- Diagnostics without content (local-first error codes and optional OTLP export); partition, coma, poison-pill quarantine and recovery behaviour.

15. Acceptance scenarios and decisions

- Golden fixtures and negative test vectors shared with agent-bot-identity (Phase 1) and hostile-worker verification gates (Phase 4). Starter scenarios are in Appendix B.

Appendix A: What already exists

Much of the paper would generalize accepted decisions rather than invent new ones. Paths are in qwts/agent-comms.

| Section | Builds on | Gap the paper closes |
| --- | --- | --- |
| 2, 4 | ADR-0003 souls and principals; ADR-0006 machine broker between persona accounts | Member, installation and runtime IDs inside one composite Soul |
| 3, 14 | ADR-0028 federation; docs/federation-*.md | Site tier and the recursive node; no runtime authorized yet |
| 5 | NDJSON wire v: 1 (lib/wire.mjs); docs/federation-wire-candidate.md | Envelope fields from the identity paper; N and N-1 rule |
| 6, 7 | ADR-0004 durable mailbox and waking; docs/mailbox-retention.md | Ordering scope, dedup IDs, clock-in queueing |
| 8 | None | New: intra-Soul member messaging and role routing |
| 9 | ADR-0008 daemon vouching and the wake plane; ADR-0077 owner decisions through the broker | HQ directives and queries; standalone profile |
| 10 | docs/tasks.md (offer, accept, update with revisions) | Proposals vs commitments; multi-endpoint task authority |
| 11 | None | New: participation presets and Soul-level budgets |
| 12, 13 | ADR-0005 A2A at the broker edge; docs/a2a.md; docs/channels.md | Exposed specialists; third-party egress policy |
| 15 | docs/*-diagnostics.md; docs/federation-receipt-candidate.md | Receipt mapping to identity action records |
| HQ host | ADR-0059 host apps embed agent-comms | GeniusBar as front end over the HQ daemon |

Appendix B: Starter acceptance scenarios

| # | Scenario | Expected outcome |
| --- | --- | --- |
| 1 | Site hub uplink drops for an hour | Local and LAN traffic continues; cloud-bound messages queue and deliver once, in order per conversation |
| 2 | Cloud node sends a "stop Soul" request | Refused: control never crosses the machine boundary |
| 3 | Four harnesses in one Soul try to reply to the same thread | One Soul-level budget; at most the preset's allowance is sent |
| 4 | Peer message claims "the owner approved this" | Treated as a peer request; no owner authority |
| 5 | Old Soul revision speaks wire N-1 to a new broker | Accepted; a required N+1 field is rejected, not ignored |
| 6 | Same message delivered twice after a retry | Deduplicated by message ID; one task transition |
| 7 | Two members both post a final answer to one task | Only the task authority's commitment finalizes; the other stays a proposal |
| 8 | Soul runs standalone, no HQ | Same channels against the local stub; receipts mark the weaker profile |
| 9 | Soul clocks in on a new machine | Installation epoch advances; the old installation is fenced at the broker |
| 10 | Exposed reviewer endpoint receives a request for memory | Refused: only the delegated capability is reachable |
| 11 | A grant is revoked while a message using it waits in the mailbox | Refused at consume/wake time; the sender's receipt shows the revocation |
| 12 | A message fails to wake its Soul N times | Quarantined as a poison pill; the rest of the mailbox keeps delivering |
| 13 | A region tries to send an external-untrusted derived note to a third party | Blocked at the egress point unless taint clearance allows that destination |
| 14 | The lead fails over to an understudy on a provider the task's data classification forbids | The entry point skips it, and the broker refuses the model call if it is attempted anyway |
| 15 | A Soul moves by life transfer mid-conversation | Watermarks from comms/ prevent redelivery of settled messages; open task leases resume under the new epoch |

Appendix C: Recommended defaults

| Question | Default | Why |
| --- | --- | --- |
| Ordering scope | Per conversation; per task when a task exists | Agent work is conversational. Global ordering across federated hubs is costly and nothing needs it. |
| Delivery guarantee | At-least-once on every tier, deduplicated by message ID | One semantic everywhere. Dedup makes processing effectively once without a second mode. |
| Encoding | NDJSON on every tier; canonical JSON for signed parts | Already shipped (lib/wire.mjs, canonical-json.mjs). Add binary only if measurements show a need. |
| Task authority inside a Soul | The lead harness decides; agent-comms commits after grant and budget checks; other members only propose | Matches "one Soul, one endpoint" and the identity paper's proposal vs commitment rule. |
| Participation preset | Default quiet. Quiet: no unprompted starts, one reply per inbound, at most 2 unanswered follow-ups, close after 24 h without progress. Chatty: up to 3 starts a day and 3 replies per inbound. Goal oriented: starts only for an assigned task, stops at its done condition, at most 5 follow-ups. | Safe default; the numbers are starting values to tune from receipts. |
| First authenticator | Per-node Ed25519 key plus a one-time enrollment code the owner confirms in GeniusBar | Already the ADR-0028 model (key possession plus owner-verified out-of-band challenge). OAuth comes next, for cloud accounts. |
| Site tier binary | The same broker in relay mode | Invariant 1: one codebase, config decides the tier. |
