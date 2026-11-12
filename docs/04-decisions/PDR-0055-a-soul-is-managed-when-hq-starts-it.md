---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-12
Date: 2026-11-12
Accepted: 2026-11-12
Discussion: https://github.com/true-line/agent-bot-platform/discussions/55
Affects-Repos: [soul-contracts, agent-bot-hq, agent-bot-souls]
Affects: [trust-model]
---

# PDR-0055 A Soul is managed when HQ starts it

A Soul that HQ starts is a managed Soul. A Soul that HQ does not start is an unmanaged Soul. HQ does not start Souls yet, so every Soul today is unmanaged.

## Context

- The [glossary](../glossary.md) took both terms from S8: a managed Soul had its "harnesses launched and run by its soul package", and an unmanaged Soul had its harness "owned by an app the platform doesn't run (IDE, web chat)". Neither line mentioned HQ.
- PDR-0053 says a Soul "runs by itself or, preferably, managed by HQ". The entry point in agent-bot-souls cannot run a Soul without HQ, and nothing said what such a run is called ([agent-bot-souls#4](https://github.com/true-line/agent-bot-souls/issues/4)).
- In a working session the owner said:
  - If HQ is there, use the HQ flow. If it is not, the person running the Soul has to specify what happens. "HQ is there" means on the system and running.
  - "soul without an official HQ is unmanaged soul"; "by definition its unmanaged because it's not started by hq".
  - "hq start (managed) hq doesnt start (unmanaged)".
  - A Soul started from the command line with HQ running and a Soul run with no HQ are the same thing: unmanaged.
  - The project is large, and some things will have gaps until they are filled.

## Decision

1. **Managed Soul:** a Soul that HQ starts.
2. **Unmanaged Soul:** a Soul that HQ does not start, however else it is started: from the command line, or by an app the platform doesn't run.
3. **There are two cases, not three.** A Soul started from the command line is unmanaged whether or not HQ is running.
4. **Not decided here.** The enforcement profile values `managed-protected` and `managed-cooperative`, and when HQ starts Souls, stay as they are until a later decision.

## Acceptance

The owner stated the decision in a working session on 2026-11-12. It is recorded in the marked answer to [discussion #55](https://github.com/true-line/agent-bot-platform/discussions/55), which the agent posted quoting the owner.

## Consequences

- **Platform:** the glossary and the lifecycle page follow this record.
- **soul-contracts:** the profile values `managed-protected` and `managed-cooperative` are reported for Souls that this record calls unmanaged. DRIFT-018 tracks it. No schema changes with this record.
- **agent-bot-hq:** HQ starting a Soul has no row in its migration plan.
- **agent-bot-souls:** a Soul run without HQ is an unmanaged Soul ([agent-bot-souls#4](https://github.com/true-line/agent-bot-souls/issues/4)).

## Alternatives considered

- **Option A: managed means under HQ**, admitted by it and with its agents started by it, whoever started the Soul. It keeps the profile values true and is not the owner's definition.
- **Option C: keep the S8 meanings** and pick a new word for a Soul run without HQ. It conflicts with what the owner said.
