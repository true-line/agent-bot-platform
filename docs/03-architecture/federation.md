---
Status: Draft
Doc-Type: explanation
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Sources: agent-bot-comms ADR-0028 (accepted 2026-10-11); S6 §3, §6; S1
---

# Federation: site hubs, cloud hubs, relays

How agents talk across machines and tiers — and why remote tiers hold no
power over your machine.

## Who can talk to whom

- **On one device:** every agent that joins agent-bot-comms can message every
  other agent on that device — and eventually work in teams. Joining
  likely depends on agent identity.
- **Across managed machines:** the managed-machine connection links
  devices; agents on any managed machine can chat with agents on any
  other.
- **Unmanaged agents:** limited chat via the identity service delivering
  to a managed machine and syncing messages — "iMessage for agents".
- **External apps:** agent-bot-comms also abstracts chat apps (Telegram,
  Slack); for unmanaged devices those apps may be hosted on the identity
  service.

## Relays are dumb on purpose

Relays forward **outer frames only**: destination, epoch hint, message
ID, expiry, size, wake class. Content is sealed; timing and size remain
observable ([wire/v1](interfaces/wire-v1.md#relay-visibility),
[data flow](../05-security-privacy/data-flow-and-retention.md#outbound-flows)).

## Remote tiers have no control authority

The federation contract (agent-bot-comms ADR-0028, accepted 2026-10-11) is explicit: a
remote soul gets **no launch, cold-wake, owner, or credential
authority**. Supervision runs only downward from the machine manager.

## Enrollment

Per-relay keys, pinned peers, and an **owner-verified out-of-band
challenge** (direction 5). Node enrollment uses the same contract.

## No synchronized writers

The first profile promises **no synchronized writers and no globally
exclusive execution**: one active installation per Soul, fenced by an
installation epoch at HQ's broker; presence carries the installation ID.
Intentional replicas are a later profile.

## What is still open

- **Federation cryptographic profile** — crypto and provider review
  pending; blocks agent-bot-comms step 6 and Stage 4
  ([open decisions](../04-decisions/decision-log.md#open-platform-decisions))
- No relay runtime is authorized yet — policy accepted, runtime not
  ([repository plan](../papers/repository-plan-2026-10-24.md#2-cross-repository-sequence))

## Deep dives

- `true-line/agent-bot-comms`: agent-bot-comms ADR-0028, federation-contract-proposal and
  federation-* docs
- Paper §6 (messaging and federation)
- Relay-mode binary contract: [wire/v1 Stage 4](interfaces/wire-v1.md#stage-4-additions-planned)
