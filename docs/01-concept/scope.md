---
Status: Draft
Doc-Type: concept
Owner: product-owner
Last-Reviewed: 2026-11-07
Sources: S6 §1, §2, §15
---

# Product scope

The first release serves individual technical operators and small engineering teams doing bounded development and research work through one persistent Soul. This page fixes what that release includes and excludes, so a component does not build toward something the product has not committed to.

## Users and roles

The data model keeps three roles distinct even when one person fills all of them in the first release (S6 section 1):

| Role | Does |
|---|---|
| Owner | Configures a Soul's authority: grants, data destinations, roles, budgets |
| Requester | Assigns work within that authority |
| Operator | Maintains machines and integrations |

The initial customer hypothesis is an operator who already uses more than one agent harness and needs dependable work across a few repositories or research workspaces.

## In scope for the MVP

From S6 section 2:

- One owner on one supported host; one Soul with two harness roles (lead and specialist).
- Terminal chat and an ACP front door; an HQ administration CLI; a minimal owner console.
- Brokered access to one model destination (remote or local) and one external service.
- Durable tasks and action receipts, interruption and recovery.
- Release profile: managed protected on the Linux reference host. The same build runs managed cooperative on macOS and says so.

## Out of scope for the MVP

- Cross-owner tenancy, public federation, a marketplace, exposed specialist endpoints.
- Unattended cross-machine migration and concurrent active replicas of a Soul.
- Nested Soul execution and self-accepting policy changes.
- Any promise that arbitrary harnesses work under strong enforcement; adapters qualify one at a time.

A standalone mode may exist for development, but it cannot satisfy the protected release criteria by changing its label (R8).

## The release test

An owner can assign a bounded task, inspect its authority and evidence, interrupt it, and recover it without silently widening permission or duplicating a consequential action (S6, executive overview). The [conformance catalog](../07-verification/conformance-catalog.md) breaks this into stage gates.

## Before a hosted or broader release

S6 section 15 lists what must exist before either step. Before a public hosted service: tenant isolation, account recovery, abuse handling, quotas, incident response, retention controls and clear service ownership. Before a broader local release: installation diagnostics, supported-platform documentation, credential revocation and rotation, safe update and rollback, backup recovery, and an inspectable export.
