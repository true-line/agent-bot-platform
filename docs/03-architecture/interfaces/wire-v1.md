---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-05
Normative-Source: true-line/soul-contracts (wire/v1 frame schema + fixtures)
---

# Protocol reference: wire/v1

The inter-agent wire protocol: NDJSON outer frames carrying sealed
envelopes, plus the mailbox semantics around them.

> **Normative source:** `true-line/soul-contracts` wire/v1 outer frame and
> sealed envelope schemas (§6, Appendix A) with fixtures; existing
> implementation in `qwts/agent-comms` (`lib/wire.mjs`,
> `canonical-json.mjs`, durable mailbox per agent-comms ADR-0004).

## Outer frame fields

| Field | Purpose |
|---|---|
| destination Soul | routing target |
| epoch hint | fencing/staleness signal |
| message ID | dedup key |
| expiry | stale frame refusal |
| payload size | limit enforcement |
| wake class | scheduling priority of the wake |
| required capabilities | receiver must declare all; unknown → refuse |
| sealed block | content, sealed; relays cannot read it |

Fixtures exist for: oversized frame, duplicate key, unknown required
capability, stale expiry (Stage 0 contract baseline).

## Relay visibility

Relays see **only the outer frame** — content is sealed; timing and size
remain observable (§6). This is the disclosure contract for relayed
delivery ([data flow](../../05-security-privacy/data-flow-and-retention.md#outbound-flows)).

## Mailbox semantics

- **Durable mailbox** with deduplication keyed by message ID (agent-comms ADR-0004)
- **Wake classes** and the external-untrusted cold-start rule (§6)
- **Send reservations** with retry reuse (§8)
- **Poison quarantine**, expiry, backpressure (§6 defaults)
- Outbox behind a store interface implemented by HQ's protected database;
  clients keep a mirror only (§6, §11)

## Gateways

A2A and MCP gateways preserve provenance and apply admission policy (§12).
A2A sits at the edge (agent-comms ADR-0005); host apps embed agent-comms (agent-comms ADR-0059).

## Stage 4 additions (planned)

Relay mode: same binary, routing only — outer-frame inspection, **no
execution channel** (§13). Sealing profile and enrollment per the reviewed
cryptographic contract. Federation crypto profile is an open decision
([open decisions](../../04-decisions/decision-log.md#open-platform-decisions)).
