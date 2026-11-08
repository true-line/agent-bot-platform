---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-07
Date: 2026-11-07
Accepted: 2026-11-07
Discussion: https://github.com/true-line/agent-bot-platform/discussions/24
Affects-Repos: [agent-bot-comms, agent-bot-hq, agent-bot-souls, soul-conformance, soul-contracts]
Affects: [wire-v1, task-v1]
---

# PDR-0024 agent-comms mirrors task-v1 and frames wire-v1

agent-comms meets the two seams as the registry already assigns them. It validates and mirrors HQ's `task/v1` records unchanged, and it wraps each routed message in a `wire/v1` frame at its broker delivery and relay layer. Its shipped v0.5.5 task workflow and local client protocol stay as they are, documented as outside the seams. This closes DRIFT-004 without a schema change or a breaking release.

## Context

- soul-contracts v0.4.1 publishes `wire/v1` and `task/v1` schemas with positive and negative fixtures. qwts/agent-comms#297 asked agent-comms to load them in its tests, which is part of the Stage 0 exit in the [roadmap](../10-program/roadmap.md).
- agent-comms v0.5.5 describes different things (DRIFT-004):
  - Its task states are offered, accepted, working, input-required, completed, failed, rejected and canceled. `task/v1` has offered, accepted, running, waiting with a reason, reconciling, completed, failed, canceled and expired. `rejected` has no `task/v1` equivalent.
  - Its parties are `offerer` and `assignee`; `task/v1` names `requester` and `accountable_soul`. `task/v1` transitions also need `installation_epoch`, `lease_generation` and `operation_id`, which comms does not have.
  - Its wire is op-based NDJSON request lines on a local socket ([its local wire module](https://github.com/qwts/agent-comms/blob/main/lib/wire.mjs)). `wire/v1` is an outer routing frame with `destination_soul`, `destination_epoch`, `expires_at` and `wake_class`.
- The [seam registry](../03-architecture/seams.md) already assigns ownership: agent-bot-daemon (HQ) provides `task-v1` and agent-comms consumes it; agent-comms provides `wire-v1`.

## Decision

1. **comms mirrors `task-v1`.** agent-comms adds a codec that validates and mirrors HQ task records and commitment requests unchanged. Its tests run every `task/v1` fixture in soul-contracts through that codec: the positives are accepted, and the negatives are refused with the error code each one names.
2. **The native task workflow is not `task-v1`.** The v0.5.5 task workflow stays as a local peer-offer feature, and agent-comms documents it as outside the seam. Whether to retire it once HQ tasks exist is a later decision.
3. **comms frames `wire-v1` at the broker layer.** agent-comms wraps each routed message in a `wire/v1` frame at its broker delivery and relay layer, and its tests run every `wire/v1` fixture there. The local client request protocol stays as it is, documented as a layer under the seam.
4. **No contract changes.** This work changes neither `wire/v1` nor `sealed-inner-v1`. The federation candidate remains input only, not baseline. Meeting the published `wire/v1` frame is not authorization to enable public federation, or to accept an unreviewed sealing profile. Public federation and agent-comms step 6 stay gated.
5. **The identity mapping stays unspecified.** Which platform term an `agent_<uuid>` conversation identity maps to (Soul, member, runtime or session) is not decided here (agent-comms ADR-0297).
6. **Implementation details stay in agent-comms.** The validator choice and other comms-side details are decided in agent-comms and recorded in its ADR.

## Acceptance

The owner accepted option 1 on 2026-11-07, in the marked answer to [discussion #24](https://github.com/true-line/agent-bot-platform/discussions/24). The answer added decisions 4 and 5 from standing decisions, and asked that this be recorded as PDR-0024.

## Consequences

- **agent-comms:** one PR adds the `task/v1` codec, the `wire/v1` frame and the fixture tests, makes [its task page](https://github.com/qwts/agent-comms/blob/main/docs/tasks.md) and [its local wire module](https://github.com/qwts/agent-comms/blob/main/lib/wire.mjs) cite the seams, and records an ADR. Two task models coexist in agent-comms for a while. Nothing installed breaks (PDR-0002).
- **Platform:** the `wire-v1` and `task-v1` seam notes cite this record, and DRIFT-004's resolution follows it. DRIFT-004 is resolved when the agent-comms PR merges.
- **soul-contracts:** no change.
- **agent-bot-daemon, agent-bot-souls, soul-conformance:** no change now. They consume the same fixtures, so a frame or record agent-comms emits must pass them.

## Alternatives considered

- **Project the native model onto `task/v1`.** A lossy projection cannot produce the HQ-only fields, has no clean home for `rejected` without a schema change, and blurs who is authoritative.
- **Migrate agent-comms natively to `task/v1`.** It would break installed v0.5.5 clients and host apps, which PDR-0002 forbids during adoption, and agent-comms cannot be authoritative for a seam HQ provides.
