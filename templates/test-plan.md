---
Status: Draft
Doc-Type: plan
Owner: verification-lead
Last-Reviewed: YYYY-MM-DD
Stage: <Stage 0 | 1 | 2a | 2b | 3 | 4>
Baseline: baseline/<N>
---

# Test plan: Stage <N> <name>

<One paragraph: what this stage must prove, on which host profile, and the exit evidence from the roadmap.>

## Scope

| T-series test | Verifies | Implemented in | Level |
|---|---|---|---|
| T<NN> | R<N> | soul-conformance | <unit, contract, integration, system, hostile> |

Tests out of scope for this stage, with the stage that picks each up.

## Entry criteria

Contract versions, fixtures and component commits that must exist before the run. Pin each to a commit.

## Environment

Host, OS and enforcement profile (protected or cooperative), harness and adapter versions, providers. Anything that differs from the declared profile is a deviation.

## Exit criteria

The pass condition for each test and for the stage. A stage exits on evidence, never on its date.

## Evidence

Where the run's report is published and what it must contain: commands, versions, results, deviations, unresolved failures.
