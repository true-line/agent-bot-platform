---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-20
Date: 2026-11-12
Discussion: https://github.com/true-line/agent-bot-platform/discussions/52
Affects-Repos: [agent-bot-machine, agent-bot-hq, soul-conformance]
Affects: [R3, trust-model]
---

# PDR-0052 Isolate network access at harness launch

The owner selected the process-isolation answer in [Discussion #52](https://github.com/true-line/agent-bot-platform/discussions/52). This proposed record reconciles that answer with Stage 2a. [PDR-0085](PDR-0085-macos-first-protected-pilot.md) sets macOS first.

## Context

A launched harness needs its Unix broker socket. A direct network connection lets it reach a provider outside the broker's policy and audit. The owner raised a second concern with per-account firewall rules. They would have to coexist with every other firewall managing the host.

## Decision

1. On macOS, apply a sandbox profile to the launched harness process that denies direct IP networking and permits the Unix socket used for its broker. The owner-selected answer specifies the mechanism at the profile level. Selection of a supported launcher and verification on each supported OS version remain implementation work.
2. On Linux, launch the harness in an empty network namespace. The selected design uses a Machine-installed, root-owned launcher restricted to provisioned accounts. It enters the namespace and permanently drops privileges to the selected account before running the harness. The authorization covers that launcher only.
3. Verify T03 through normal harness launch. A direct request to a reachable provider or service must fail, and the same operation through the broker must reach the service. The macOS pilot needs that evidence on its declared host and configuration. [Conformance catalog](../07-verification/conformance-catalog.md)

## Consequences

Machine and HQ must agree on how a provisioned harness account, its launch policy and its assigned broker endpoint fit together. Each implementation must identify which processes it actually confines. Existing installations with per-account firewall rules need a separate migration that preserves isolation during transition. [DRIFT-024](../00-governance/drift-register.md#drift-024-harness-egress-isolation)

## Alternatives considered

Per-account firewall rules can interfere with other firewall managers. Leaving direct IP access available would let a harness bypass its broker. Discussion #52 also considered a per-harness systemd unit on Linux, which would change how HQ hands input and output to the launched process.
