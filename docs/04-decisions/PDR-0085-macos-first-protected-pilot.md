---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-17
Date: 2026-11-17
Discussion: https://github.com/true-line/agent-bot-platform/discussions/85
Affects-Repos: [agent-bot-platform, agent-bot-hq, agent-bot-machine, soul-conformance]
Affects: [R8, scope, quality-bar, trust-model]
---

# PDR-0085 Qualify protected macOS first for the operator pilot

The owner chose macOS for the first protected operator pilot on 2026-11-17.
This proposal records that choice for review. The owner-approved record on
platform main governs rollout. [Discussion #85](https://github.com/true-line/agent-bot-platform/discussions/85)

## Context

S6 put protected Linux first and protected macOS in Stage 4. That order
would require separate hardware before the owner could qualify the system
on its primary operating platform. Existing Linux results are valuable for
their declared cohorts. They cannot establish macOS host behavior.

## Decision

1. Qualify a declared macOS host in Stage 2a. Record its hardware and OS
   build, relevant dependency and adapter versions, definition revision,
   policy digest and observed profile. T01, T02 and T03 must pass under
   protected enforcement. T21 must demonstrate cooperative labeling and
   refusal of a protected claim on the cooperative configuration.
2. Run the Stage 3 operator pilot on qualified protected macOS with real
   approved adapters, measured pilot targets and the usual stage sign-off.
   Report cooperative for configurations providing only cooperative guarantees.
3. Shared contracts describe required behavior across operating systems.
   HQ and Machine select host-specific implementations. Cloud Linux
   development can proceed in parallel throughout delivery.
4. Linux and Windows are secondary targets. Preserve existing Linux tests
   and evidence with their host and scope. Each secondary host needs its
   own qualification before advertising protected support. Their availability
   and qualification are independent of the macOS pilot.
5. [PDR-0053](PDR-0053-soul-life-and-agent-replace-member.md) governs
   OS accounts per harness credential. A shared account alone establishes
   neither separation between agents nor protected status. Qualification
   must prove the required observations on the actual configuration.

## Consequences

HQ and Machine implement and verify the macOS service account, caller
binding, state isolation, egress and key custody. Conformance publishes
independent results, including the T02 key boundary on the declared host.
The [roadmap](../10-program/roadmap.md) owns stage order and the
[support matrix](../09-operations/support.md#host-support-matrix) owns
status by host. Existing operator, adapter, portability and relay gates
keep their evidence requirements. [DRIFT-022](../00-governance/drift-register.md#drift-022-pilot-host-order)
tracks component adoption.

## Alternatives considered

Linux-first would carry forward the original schedule but delay validation
on the pilot platform. A cooperative-only macOS pilot would omit the host
enforcement the owner requires. Requiring all operating systems to qualify
together would tie macOS delivery to independent ports.
