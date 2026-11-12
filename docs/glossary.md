---
Status: Draft
Doc-Type: reference
Owner: protocol-maintainer
Last-Reviewed: 2026-11-12
Sources: S6; S1; S5; S8
---

# Glossary

This page is the single home for platform vocabulary (PDR-0001). A component repository links here instead of defining a term again; a schema field name in soul-contracts takes its meaning from this page. The Where column cites the source a definition came from.

Two terms are in conflict and stay marked until the owner decides: **Soul** and **principal** (DRIFT-009), and **GeniusBar**, which is a code name until the owner picks a product name (DRIFT-006).

## Identity

| Term | Definition | Where |
|---|---|---|
| **Soul** | A package: a definition plus what its Life has captured. One stable ID. It runs by itself or, preferably, managed by HQ. A Soul is not an agent | PDR-0053; S6 §1; S1 |
| **Member** | Retired by PDR-0053; write **agent**. It meant a harness brain-region inside a Soul, with a Soul-qualified ID. Contract field names keep it: `member_id` identifies an agent of a Soul | S5; PDR-0053 |
| **Installation** | One admitted placement of a Soul on a host; fenced by installation epoch | S6 §5, §7 |
| **Runtime** | A launched process executing an agent; fresh credentials on replacement | S5 |
| **Session** | A bounded interaction context, one per context/conversation | S8 |
| **Binding** | HQ's association of one session with one worktree, for the Soul the session acts for; ends on unbind, session end or revocation; not a grant | PDR-0023 |
| **Presence** | HQ's observation that a session is live, from a named evidence source; distinct from daemon health, binding and model activity | PDR-0023 |
| **Definition revision** | An immutable revision of the Soul's definition; sleep/upgrade produce new ones; ID never changes | S1 D3, S1 D4 |
| **Principal** | A human or organization that can own or delegate authority, independent of any agent | S6 §3; in conflict, DRIFT-009 |
| **Owner** | The principal whose host account installed HQ and who configures a Soul's authority | S6 §3 |
| **Life** | A Soul running over time. It captures memories, experiences and new abilities. Its captured state is stored in the package and moves with the Soul | PDR-0053 |
| **Lead** | The Life's brain: the one harness that orchestrates, routes work and finalizes decisions | PDR-0053 |
| **Agent** | What runs in a harness inside a Life: a motor function, talent or trait of the Life. Not the equivalent of a person; the Life is. One Life has several | PDR-0053 |
| **Harness** | The program an agent runs in. One credential and one OS account per harness credential | PDR-0053 |
| **Specialist** | An agent that returns proposals and evidence to the lead | S6 §3 |
| **Enrollment** | One-time registration of a Soul, node or relay with an owner-confirmed challenge; lasts until revoked | S6 §3 |
| **Admission (clock-in)** | Per-start verification of a Soul and its runtimes by local HQ | S6 §3 |

## Authority and enforcement

| Term | Definition | Where |
|---|---|---|
| **HQ** | The machine's headquarters: trusted supervisor + broker; the enforcement point outside the agent shell's trust domain | S6 §3, §4 |
| **Harbor** | The hosted service at `agents.true-line.ai`: the owner's identity service and its web console, from the agent-bot repository. Full name Agent Bot Harbor. Distinct from HQ, which runs on the machine. For a machine the owner has linked, Harbor decides policy and lifecycle and HQ enforces; Harbor never executes on a host | Owner decision 2026-11-10; PDR-0047 |
| **Protected** | Routed through the broker with a receipt: inference, service calls, task commits, messages/wake, credential use, lifecycle | S6 §4, §6, §7 |
| **Cooperative** | Inside an agent's own trust domain: workspace edits, local shell, harness-internal tools — reported, not enforced | S6 §4 |
| **Managed machine** | Enrolled with the owner's identity service; two-way connection | S8 |
| **Unmanaged machine** | Agent runs with only MCP/limited tooling, no enrolled local server | S8 |
| **Managed Soul** | Harnesses launched and run by its soul package | S8 |
| **Unmanaged Soul** | Harness owned by an app the platform doesn't run (IDE, web chat) | S8 |
| **Grant** | Standing authority: action/resource selectors, destinations, data restrictions, expiry, ceiling | S6 App. A |
| **Grant handle** | A broker-generated opaque reference to a grant, bound to the admitted caller and never chosen by the caller; lasts one runtime admission | S6 §3 |
| **Credential reference** | An opaque pointer to a short-lived credential HQ obtains from the identity service, never the secret itself | S6 §3 |
| **Approval** | Owner confirmation bound to a record digest; single-action or bounded class | S6 §8, T24 |
| **Dream grant** | Time, cost share, cell cap, destinations, executor for a dream run | S6 App. A |

## Tasks and coordination

| Term | Definition | Where |
|---|---|---|
| **Task** | A unit of work with resource scope + exclusive write scope; nine-state machine | S6 §7 |
| **Receipt** | Broker-issued record: task, caller (agent+runtime), destination, adapter route, settled cost | S6 §7 |
| **Outcome unknown** | Terminal ambiguity; reconcile via broker lookup, never blind replay | S6 §7, T06 |
| **Wake class** | Delivery scheduling class on the wire frame | S6 §6 |
| **Directive** | A task offer from HQ backed by authenticated local authority; peer text cannot acquire the kind | S6 §3, T04 |
| **Query** | An agent's question to HQ, answered with a decision record | S6 §3 |
| **Send reservation** | Outbox reservation; settles on retry or cancel | S6 §8 |

## Memory and improvement

| Term | Definition | Where |
|---|---|---|
| **Notes** | Typed, self-reported memory — **not evidence** | S6 §10 |
| **Dream run** | Idle-time admitted workflow under a dream grant; no administrative authority | S6 §10 |
| **Candidate (revision)** | Proposed definition/primitive change with per-cell eval matrix; partial acceptance disallowed | S6 §10, T28 |
| **Guardrail** | A check whose failure must never be accepted; violation disables a route | S6 §9 |
| **Primitive** | A reusable skill/behavior improvement rendered per adapter | S6 §10 |
| **Render** | The deterministic build step that turns primitives into each adapter's native configuration, per revision and adapter version | S6 §3 |
| **Eval cell** | One role on one harness version and one provider within an evaluation plan | S6 §3 |
