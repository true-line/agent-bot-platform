---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-08
Date: 2026-11-08
Accepted: 2026-11-08
Discussion: https://github.com/true-line/agent-bot-platform/discussions/23
Affects-Repos: [agent-bot-daemon, agent-bot, soul-contracts, agent-comms, agent-bot-identity]
Affects: [observation-v1, R1, R2, R9, QA-A11Y-01]
---

# PDR-0023 HQ observation uplink for presence, bindings and events

Local HQ observes agent sessions and pushes allowlisted observations over the enrolled device's authenticated outbound HTTPS to the identity service at `agents.true-line.ai`, which keeps a read-only projection for the web console. The projection is never an authority: HQ stays authoritative for bindings and lifecycle, and the uplink carries no control or execution path (R2). Communications reuse agent-comms' existing workstreams, and the discussion board comes last.

## Context

- The console cannot tell a live agent session from a running daemon or a stale binding. Daemon health work (agent-bot-identity#1356) shows that HQ is up, not that any session is.
- Discussion #23 proposed presence, binding visibility, lifecycle events, communications and a board, in that order, with companion issues in agent-bot-daemon (#80 to #82), agent-bot and agent-comms.
- R1 keeps Soul, member, installation, runtime and session separately attributable. R9 keeps local work going without the uplink.

## Decision

1. **Option 1.** HQ collects evidence and pushes it outbound. agent-bot stores an observational projection that the console reads. Live browser updates (SSE) are a later proposal, not a dependency of the first slice.
2. **Seam.** The uplink is the `observation-v1` seam: agent-bot-daemon provides it and agent-bot consumes it. Its records, fixtures and error codes live in soul-contracts `schemas/observation/v1` and the error registry, published before any implementation emits them. No repository keeps a local copy of the contract.
3. **Subjects.** Observations name owner account, then enrolled device, then Soul, then member, then session. A binding links one session to one worktree. The Soul ID is the stable public ID (R1). Session, binding and worktree IDs are opaque and minted by HQ, never derived from a path or a harness transcript ID. Sibling sessions of one Soul never overwrite each other.
4. **Evidence.** Every presence observation names its evidence source. observation/v1 lists the sources and which adapters support each. The first slice uses session bind, unbind and end, and authenticated requests HQ receives from a bound session. A source an adapter does not support reports `unknown`. Presence never implies thinking, busy or model activity.
5. **States.** `active`: evidence observed within the freshness window, measured from observation time, not receipt time. `stale`: the latest evidence is older than the window. `offline`: the service has not heard from the device within the uplink expiry; last observations show with their age. `unknown`: no supported source. `ended`: HQ saw the session end, unbind or revoke. `ended` is terminal; a new session gets a new ID. A daemon heartbeat refreshes the device's uplink, never a session.
6. **Freshness.** Each observation carries HQ's source epoch, which increases on every HQ start, a per-epoch sequence, observation time and an event ID. The service keeps the highest epoch and sequence per subject, ignores duplicates and older records, and refuses observations for an ended session. Buffered observations keep their original time, so replay never looks fresh. A new epoch starts with a snapshot. Only a complete, accepted snapshot can mark a subject ended; a partial or missing upload changes nothing.
7. **Cadence and limits.** HQ sends on change plus a jittered periodic refresh. The HQ outbox, replay window and projection are bounded. On overflow HQ drops the oldest entries and sends an explicit gap marker. The numbers (refresh interval, jitter, freshness window, uplink expiry, bounds and retention) are unspecified. The owner sets them before #80 ships, and soul-contracts publishes them with observation/v1.
8. **Allowlist.** By default an observation may carry only the opaque IDs, Soul and member IDs, adapter name, state, evidence source, epoch, sequence, times, event kind and gap markers. It never carries credentials, binding secrets or proofs, prompts, transcript contents, IDs or URLs, raw diagnostics or exceptions, or absolute local paths. Repository or worktree metadata is sent only after observation/v1 states its fields and destination and the owner approves them.
9. **Failure.** An uplink outage never blocks permitted local work (R9). Expiry never revokes a binding. Device revocation stops ingestion. The service scopes every record to the device's owner account.
10. **Communications and board.** Communications reuse agent-comms ADR-0028 and its open workstreams, not a new transport. Board threads are durable conversation, never grants, directives or commands (R6). Readership, attribution, retention and whether the service may read content are decided before board storage is chosen. An end-to-end encrypted comms envelope is never reused as server-readable board content.
11. **Address and accessibility.** Telemetry goes only to `agents.true-line.ai`, never `agents.true-line.com`. Console surfaces meet QA-A11Y-01.

## Acceptance

The owner accepted option 1 on 2026-11-08, in the marked answer to [discussion #23](https://github.com/true-line/agent-bot-platform/discussions/23), and asked that it be recorded as PDR-0023. Points 3 to 8 record the contract decisions the answer asked this record to make.

## Consequences

- **Platform:** the seam registry adds `observation-v1`, and the catalog adds it to agent-bot-daemon and agent-bot.
- **soul-contracts:** publishes observation/v1 schemas, fixtures and error codes, including the numbers in point 7. That unblocks agent-bot-daemon#80 to #82.
- **agent-bot-daemon:** #80 presence, #81 binding visibility and #82 events, in that order, after the contract. Their tests prove that daemon-only liveness never yields `active`, that a reconnect never resurrects an ended session, and that two sessions of one Soul stay distinct.
- **agent-bot:** ingestion, projection and console. Tests prove tenant isolation and that board content never grants execution authority.
- **agent-bot-identity:** existing binding and health instrumentation feeds HQ through a narrow child issue there. It does not start a second binding registry.
- **agent-comms:** no new transport; the board follows its own issue.

## Alternatives considered

- **One bidirectional channel for everything.** It couples heartbeat delivery to tunnel readiness and mixes monitoring with control.
- **WebRTC or direct browser-to-host.** It adds signaling and NAT traversal and exposes the host, with no requirement for peer transport.
