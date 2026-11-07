---
Status: Draft
Doc-Type: concept
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Sources: S1
---

# Vision

The north star, condensed. Full text with tables and decision logs:
[north star source](../papers/agent-bot-north-star.md).

## One network, five tiers

You attach to one cloud node and reach every agent through it. The same
pattern repeats at each tier. **The Soul is the smallest unit the network
addresses.**

- Messaging and presence run **up** from the Soul to hubs.
- Supervision runs **down** only, from the machine manager to harnesses.
- Remote tiers never hold control authority.

## Build on what exists

The plan extends specified, working pieces rather than replacing them:
soul packages (`.soul` format 1/2 implemented), sleep/dream scheduler and
journal (implemented), federation policy (agent-comms ADR-0028 accepted), the
agent-comms wire and durable mailbox, and the HQ direction from the
whitepapers. State of each piece:
[north star → Existing foundations](../papers/agent-bot-north-star.md#existing-foundations).

## Alignment commitments

The architecture commits to the Soul paper (v0.3 overview) and the
identity paper (draft 0.1) row by row — stable Soul ID with separate
definition revisions; credentials in external stores referenced, never
carried; host-enforced access because trust domains may overlap; one
clock-in flow for start, report-in, and migration; no synchronized
writers; template/fork produce new IDs; dreams powerless without grants;
participation presets enforced Soul-level (one send budget, not four);
unenforceable profiles declared, never silent. The full mapping tables:
[north star → Alignment](../papers/agent-bot-north-star.md#alignment-with-the-soul-paper-v03-overview).

## Invariants

The short list the architecture must uphold is maintained in the north
star: [Invariants](../papers/agent-bot-north-star.md#invariants).

## Suggested first steps (from the north star)

Glossary + fixtures for **Soul, member, installation, runtime, session**;
then multi-harness admission with caller-bound grants and a
hostile-worker test. This is exactly Stage 0/2a of the
[repository plan](../papers/repository-plan-2026-10-24.md#2-cross-repository-sequence).
