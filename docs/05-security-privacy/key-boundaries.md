---
Status: Draft
Doc-Type: security
Owner: security-reviewer
Last-Reviewed: 2026-11-11
Scope: key material and credential flow
---

# Key boundaries

One rule with no exceptions: **credentials live in HQ and travel as
references — never as secrets.**

## The boundary

- HQ owns the key store (§4); `Equip` returns **references** (§5)
- Credentials **never enter the package** (§11) — not in `opt/`, not in
  templates, not in transfer records (§11: no secrets or reusable grants)
- The broker mediates credential *use*: inference, service calls,
  messages/wake, lifecycle all produce receipts with the adapter route
  (§4, §7)
- A shared GitHub App can serve several Souls because **the broker keeps
  scope and attribution separate**; apps held by HQ's broker, never by a
  harness (identity paper, direction 3)

## Exceptions and how they are labeled

| Exception | Risk | Mitigation |
|---|---|---|
| Short-lived-token route (§4) | token exists inside a harness for its TTL | labeled in **every receipt**; prefer brokered route |
| Harness sign-ins (per machine) | harness-level sessions outside the broker | "portable" does not remove them (§11); audit as host requirements |

## Key lifecycle

- **Add:** `hq credential add <id>` (proposed verb) → HQ store
- **Rotate:** re-equips at next lease renewal (§5, §15 release prereq)
- **Revoke:** effective at next protected operation (§4)
- **Verification:** T02 on your host + `hq audit secrets` fingerprint
  scan ([credentials how-to](../user-guide/how-to/credentials.md))

## Relay and enrollment keys

Per-relay keys, pinned peers, owner-verified out-of-band challenge
(direction 5, agent-bot-comms ADR-0028). Relays never hold Soul credentials; they route
sealed outer frames ([federation](../03-architecture/federation.md)).

## Catalog signing

The admin catalog is **signed on admin publish**; the installer accepts
catalog items only, runs as brew admin, never root (architecture,
[components diagram](../03-architecture/overview.md#components-today)).

## Control signing

On a machine the owner has linked, Harbor signs policy and lifecycle
records with a control key of its own, separate from the catalog and
credential-minting keys. HQ pins it at link time, and rotation and
revocation need the owner's device presence. Its custody, rotation and
revocation are decided in
[PDR-0047](../04-decisions/PDR-0047-harbor-is-the-control-plane-of-a-linked-machine.md).

## What a reviewer should ask for

1. T02 result for the specific host build (key boundary)
2. A receipts sample showing `labeled` short-lived-token routes
3. The T16 package-attack report (proves secrets absent from packages)
4. The signed qualification manifest chain for adapters in use
   ([release conformance](../08-release/release-conformance-report.md))
