---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-13
Date: 2026-11-13
Discussion: https://github.com/true-line/agent-bot-platform/discussions/62
Affects-Repos: [soul-contracts, agent-bot-hq, agent-bot-comms, agent-bot-identity]
Affects: [hq-plugin-contract, identity-cli, identity-service-api, R3, R6, R7]
---

# PDR-0062 HQ binds notice scope; the legacy alias consumes one

The proposed HQ-backed notice contract preserves the legacy `take_inbox`
consume-one handoff using HQ's durable local mailbox, with a separate read-only
`notices.peek` for new clients. HQ binds each caller's allowed notice scope;
agent-facing requests never select a remote queue or bypass HQ to consume it.

This record is **Proposed**. The owner selected Option A in the
[originating issue comment](https://github.com/true-line/agent-bot-platform/issues/60#issuecomment-6860006254).
That preference is the basis for this proposal, not a claim that an answer has
been marked in [Discussion #62](https://github.com/true-line/agent-bot-platform/discussions/62)
or that an Accepted PDR has merged.

## Context

- [PDR-0027](PDR-0027-hq-identity-authority-lives-in-agent-bot-daemon.md)
  keeps identity authority in HQ. Identity's agent-facing plugin surfaces
  resolve to broker queries and hold no HQ authority.
- The [HQ migration plan](https://github.com/true-line/agent-bot-hq/blob/main/docs/daemon-plugin-split.md#82-deprecated)
  names `notices.peek` as a replacement for the legacy inbox surfaces, while
  row 11 calls `take_inbox` an alias. Local handoff semantics and the binding
  from a live runtime to a remote harness and repository remain unspecified.
- [Comms #314](https://github.com/true-line/agent-bot-comms/pull/314) and
  [HQ #124](https://github.com/true-line/agent-bot-hq/pull/124) delivered durable
  ingestion before upstream acknowledgement. The legacy identity consumer
  still takes and acknowledges upstream directly, so it can consume a notice
  before HQ takes custody. [HQ #125](https://github.com/true-line/agent-bot-hq/pull/125)
  records why ingestion alone does not prove alias parity.
- Legacy `takeOne` omits `lease` and `lease_expires_at` and adds `pulled: true`.
  Durable custody intentionally omits `attempts` and unknown fields. Full raw
  payload equality is therefore not a valid compatibility claim.
- [PDR-0053](PDR-0053-soul-life-and-agent-replace-member.md) defines Soul, Life,
  agent and the harness account unit. An adapter ID or OS account does not
  establish the remote enrolled harness or repository. Sharing a harness does
  not imply separate private notice queues for every agent.

## Decision

The following is the proposed cross-repository contract, pending acceptance:

1. **Separate custody from caller handoff.** Ingestion remains upstream take,
   durable HQ transaction, then upstream acknowledgement, with notice-ID
   deduplication. The legacy alias consumes one eligible local notice
   transactionally before returning it. A lost response after local consumption
   can lose that caller handoff; this is not end-to-end at-least-once delivery to
   the caller. A future acknowledged local delivery protocol is separate work.
2. **Keep peek read-only.** New clients may inspect eligible local notices
   without consumption through `notices.peek`. The legacy alias preserves its
   consume-one behavior rather than silently becoming peek. Neither operation
   takes or acknowledges upstream directly; local consumption preserves the
   ingestion deduplication tombstone.
3. **Freeze caller scope in HQ.** HQ binds an admitted live runtime and its
   accepted agent assignment to an explicitly authorized enrolled remote
   harness and repository scope. Every query checks the current runtime, lease
   and epoch. Absent scope, expired or superseded callers and forged queue or
   repository selectors are refused. Scope changes require a new validated
   binding, never an override in an agent request. The contract must specify
   the binding fields and persistence/restart behavior before implementation.
   Policy authorization continues to follow R2 and
   [PDR-0047](PDR-0047-harbor-is-the-control-plane-of-a-linked-machine.md);
   this record gives no agent a way to grant itself scope.
4. **Withhold notices outside explicit scope.** A stored notice with missing,
   invalid or out-of-scope repository metadata is neither returned nor consumed
   by a scoped query. Its repository is never inferred from the requesting
   caller. Define retained/operator-handling behavior before rollout rather
   than silently assigning or discarding it.
5. **Specify payload compatibility.** The contract and deprecation docs must
   enumerate the preserved legacy envelope/content fields, filtering and
   oldest-first ordering, including the treatment of `pulled`, and intentional
   transport/unknown-field differences. Do not restore unknown or secret-bearing
   fields merely to match raw legacy output. Responses contain only bounded,
   sanitized notice content and stable IDs, with `external-untrusted`
   provenance and wake class `none` or `notify`; no upstream leases, credentials,
   DPoP material, owner directive or cold-start authority reaches an agent.
6. **Use the broker exclusively for the HQ-backed path.** Identity's surface is
   a broker client. HQ refusal or unavailability never triggers direct upstream
   fallback. Any explicitly retained standalone legacy mode must not compete
   for a migrated queue. The rollout must prevent or detect old competing
   consumers and state mixed-version limits; updating the new shim alone does
   not prove old consumers are disabled.
7. **Keep each fact in its home.** This PDR is the proposed home of the shared
   scope and handoff choice. Shared request/reply/error records and fixtures
   belong in `soul-contracts` before consumers depend on them (R7). HQ owns
   scope and lifecycle enforcement; comms owns mailbox mechanics; identity owns
   the compatibility surface. No schema or released field changes are made by
   this proposal, and no new error code is allocated here.

## Consequences

- **Platform:** acceptance records the chosen answer and an Accepted PDR under
  [change control](../00-governance/change-control.md). Subsequent seam or
  compatibility registry changes cite it and regenerate their pages. This
  Proposed record changes no registry behavior, resolves no drift entry and
  declares no Stage 0 exit. It does not change managed/unmanaged terminology
  or profiles ([PDR-0055](PDR-0055-a-soul-is-managed-when-hq-starts-it.md)).
- **soul-contracts:** specify any required shared messages, scope fields and
  errors with positive and negative fixtures before component implementation.
  Define the payload compatibility table in the contract home rather than
  copying it across component specifications.
- **agent-bot-hq:** validate and freeze scope, reject stale or unauthorized
  callers, expose scoped host access and define binding restart behavior.
- **agent-bot-comms:** implement scoped peek and transactional local
  consumption while preserving upstream custody and deduplication guarantees.
  Define handling of notices whose repository cannot be established.
- **agent-bot-identity:** implement only the broker-query compatibility shim,
  with the documented response shape and no direct-upstream fallback. Document
  the explicit legacy transition and mixed-version restrictions.

[HQ #13](https://github.com/true-line/agent-bot-hq/issues/13) remains the alias
acceptance tracker. After acceptance, each affected repository tracks its own
implementation slice. Before row 11 is called complete, component evidence must
show:

- the field-level compatibility table, filtering, order and consume-one result;
  peek leaves the notice available;
- refusal of forged cross-harness/repository selectors, missing or invalid
  notice repository metadata and expired or superseded callers;
- no direct upstream request from an agent-facing query, no credential/lease
  leakage and no promotion of external content to authority or lifecycle control;
- the chosen lost-response limitation, restart behavior and one durable custody
  transition under redelivery, with upstream acknowledgement after commit;
- the enforceable competing-consumer migration path and mixed-version limits.

## Alternatives considered

- **Make the legacy alias read-only peek (Option B).** A notice survives a lost
  response, but unchanged legacy callers have no separate acknowledgement and
  can repeatedly process it. That changes the destructive handoff and cannot be
  described as parity without a controlled client transition.
- **Keep direct upstream consumption beside HQ (Option C).** It avoids an
  immediate compatibility surface change, but an old consumer can acknowledge
  before HQ custody. Row 11 remains incomplete.
- **Treat the harness account as queue authority.** It neither proves the
  remote enrolled harness/repository nor separates agents sharing that account.
  HQ's explicit runtime scope is required instead.
