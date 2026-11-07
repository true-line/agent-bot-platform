---
Status: Draft
Doc-Type: reference
Owner: protocol-maintainer
Last-Reviewed: 2026-11-07
Sources: S6; S1; S5; S8
---

# Glossary

This page is the single home for platform vocabulary (PDR-0001, proposed). A component repository links here instead of defining a term again; a schema field name in soul-contracts takes its meaning from this page. The Where column cites the source a definition came from.

Two terms are in conflict and stay marked until the owner decides: **Soul** and **principal** (DRIFT-009), and **GeniusBar**, which is a code name until the owner picks a product name (DRIFT-006).

## Identity

| Term | Definition | Where |
|---|---|---|
| **Soul** | The smallest unit the network addresses; one stable ID across revisions, hosts, harnesses | S6 §1; S1 |
| **Member** | A harness brain-region inside a Soul, with a Soul-qualified ID | S5 |
| **Installation** | One admitted placement of a Soul on a host; fenced by installation epoch | S6 §5, §7 |
| **Runtime** | A launched process executing a member; fresh credentials on replacement | S5 |
| **Session** | A bounded interaction context, one per context/conversation | S8 |
| **Definition revision** | An immutable revision of the Soul's definition; sleep/upgrade produce new ones; ID never changes | S1 D3, S1 D4 |

## Authority and enforcement

| Term | Definition | Where |
|---|---|---|
| **HQ** | The machine's headquarters: trusted supervisor + broker; the enforcement point outside the agent shell's trust domain | S6 §3, §4 |
| **Protected** | Routed through the broker with a receipt: inference, service calls, task commits, messages/wake, credential use, lifecycle | S6 §4, §6, §7 |
| **Cooperative** | Inside a member's own trust domain: workspace edits, local shell, harness-internal tools — reported, not enforced | S6 §4 |
| **Managed machine** | Enrolled with the owner's identity service; two-way connection | S8 |
| **Unmanaged machine** | Agent runs with only MCP/limited tooling, no enrolled local server | S8 |
| **Managed Soul** | Harnesses launched and run by its soul package | S8 |
| **Unmanaged Soul** | Harness owned by an app the platform doesn't run (IDE, web chat) | S8 |
| **Grant** | Standing authority: action/resource selectors, destinations, data restrictions, expiry, ceiling | S6 App. A |
| **Approval** | Owner confirmation bound to a record digest; single-action or bounded class | S6 §8, T24 |
| **Dream grant** | Time, cost share, cell cap, destinations, executor for a dream run | S6 App. A |

## Tasks and coordination

| Term | Definition | Where |
|---|---|---|
| **Task** | A unit of work with resource scope + exclusive write scope; nine-state machine | S6 §7 |
| **Receipt** | Broker-issued record: task, caller (member+runtime), destination, adapter route, settled cost | S6 §7 |
| **Outcome unknown** | Terminal ambiguity; reconcile via broker lookup, never blind replay | S6 §7, T06 |
| **Wake class** | Delivery scheduling class on the wire frame | S6 §6 |
| **Send reservation** | Outbox reservation; settles on retry or cancel | S6 §8 |

## Memory and improvement

| Term | Definition | Where |
|---|---|---|
| **Notes** | Typed, self-reported memory — **not evidence** | S6 §10 |
| **Dream run** | Idle-time admitted workflow under a dream grant; no administrative authority | S6 §10 |
| **Candidate (revision)** | Proposed definition/primitive change with per-cell eval matrix; partial acceptance disallowed | S6 §10, T28 |
| **Guardrail** | A check whose failure must never be accepted; violation disables a route | S6 §9 |
| **Primitive** | A reusable skill/behavior improvement rendered per adapter | S6 §10 |
