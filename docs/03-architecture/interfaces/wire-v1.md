---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-16
Normative-Source: true-line/soul-contracts (wire/v1 frame schema + fixtures)
---

# Protocol reference: wire/v1

The broker's outer routing frame carries destination, expiry, capability and
optional sealing metadata. It is distinct from the local client's NDJSON
request protocol.

> **Normative source:** the released [wire/v1 frame schema](https://github.com/true-line/soul-contracts/blob/b96239cc47571237f7064ddbcbd0edec8e365c6b/schemas/wire/v1/wire-frame.schema.json)
> and [fixtures](https://github.com/true-line/soul-contracts/tree/b96239cc47571237f7064ddbcbd0edec8e365c6b/fixtures).
> [PDR-0024](../../04-decisions/PDR-0024-comms-mirrors-task-v1-and-frames-wire-v1.md)
> places this frame at broker delivery and relay boundaries. The production
> [wire/v1 codec](https://github.com/true-line/agent-bot-comms/blob/972fcbed06c8ff79bf60bd9129f5da54e22f5772/lib/contracts/wire-v1.mjs)
> validates that contract; `lib/wire.mjs` is the separate local client layer.

## Outer frame fields

| Field | Purpose |
|---|---|
| `wire_version` | released major version; this schema requires 1 |
| `destination_soul` | routing target |
| `destination_epoch` | sender's last-known epoch, a routing hint; commits are fenced, not inbound delivery |
| `message_id` | deduplication key |
| `expires_at` | expiry timestamp checked with runtime context |
| `payload_size` | declared payload size, bounded by the schema |
| `wake_class` | declared wake category; acceptance does not grant lifecycle authority |
| `required_capabilities` | capabilities the receiver must have negotiated |
| `sealed` | optional sealing metadata; relayed content protection needs its reviewed cryptographic profile |

Fixtures exist for: oversized frame, duplicate key, unknown required
capability and stale expiry. Schema validity and contextual expiry/capability
enforcement are separate verdicts. The [T14 evidence](../../10-program/stage-0-evidence.md#stage-0-evidence-and-remaining-work)
exercises production codecs; it does not qualify live transport or federation.

## Relay visibility

Relays see **only the outer frame** — content is sealed; timing and size
remain observable (§6). This is the disclosure contract for relayed
delivery ([data flow](../../05-security-privacy/data-flow-and-retention.md#outbound-flows)).

## Mailbox semantics

- **Durable mailbox** with deduplication keyed by message ID (agent-bot-comms ADR-0004)
- **Wake classes** and the external-untrusted cold-start rule (§6)
- **Send reservations** with retry reuse (§8)
- **Poison quarantine**, expiry, backpressure (§6 defaults)
- Outbox behind a store interface implemented by HQ's protected database;
  clients keep a mirror only (§6, §11)

## Gateways

A2A and MCP gateways preserve provenance and apply admission policy (§12).
A2A sits at the edge (agent-bot-comms ADR-0005); host apps embed agent-bot-comms (agent-bot-comms ADR-0059).

## Stage 4 additions (planned)

Relay mode: same binary, routing only — outer-frame inspection, **no
execution channel** (§13). Sealing profile and enrollment per the reviewed
cryptographic contract. Federation crypto profile is an open decision
([open decisions](../../04-decisions/decision-log.md#open-platform-decisions)).
