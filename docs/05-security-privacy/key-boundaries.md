---
Status: Draft
Doc-Type: security
Owner: security-reviewer
Last-Reviewed: 2026-11-11
Scope: key material and credential flow
---

# Key boundaries

HQ brokers credential references. Agent Machine authorizes privileged host operations and uses the protected resource under the secure administrative account. The identity service retains its own server-side keys. See [administrative custody and change control](../04-decisions/PDR-0091-host-privileged-custody.md).

## The boundary

Equip returns references. Packages, templates and transfer records must exclude secrets and reusable grants. A short-lived result can be returned only as permitted for the operation. Cooperative labeling and harness sign-ins confer no exception to administrative custody. Addition, rotation and revocation of protected host credentials use the same boundary.

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
