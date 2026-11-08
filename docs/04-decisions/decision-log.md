---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-07
---

# Decision log

Platform-level decisions the owner made in other records, before or outside the PDR process, and the platform-level decisions still open. Decisions the owner already made stay in force as recorded; a PDR is needed only to change one or to settle a conflict. Component-only decisions are left in their repositories and are not listed. A new platform-level decision is raised in [Decisions](https://github.com/true-line/agent-bot-platform/discussions/categories/decisions), not in a component repository.

## Decisions in force or superseded

| Label | Recorded in | Decision | Platform status |
|---|---|---|---|
| S1 D1 | North star, owner 2026-10-24 | Split planes: messaging and presence federate upward; supervision stays machine-local. | In force; carried by R2 and R9 |
| S1 D2 | North star, owner 2026-10-24 | The manager is the managed-machine daemon and GeniusBar's backend. | Superseded by agent-bot-daemon D1 and PDR-0002 (DRIFT-002) |
| S1 D3 | North star, owner 2026-10-24 | The identity CLI is the toolset inside each Soul. | In force; agent-bot-identity charter |
| S1 D4 | North star, owner 2026-10-24 | A lead harness orchestrates; agent-comms carries and enforces that orchestration. | Partly superseded: S6 section 3 moves enforcement to the broker in HQ's trust domain; comms client checks are advisory |
| S1 A2 | North star, assumption | Tiers 1 to 3 run the agent-comms broker in local, site or cloud mode. | Working assumption; matches S6 relay mode |
| S1 A3 | North star, assumption | Agents are addressed by `agent_<uuid>`. | Working assumption; see DRIFT-009 |
| S1 A4 | North star, assumption | Strangler migration: managed-machine first supervises the agent-bot daemon. | Superseded by agent-bot-daemon D1; strangler approach itself stands |
| agent-bot-daemon D1 | daemon plan section 10.1, owner 2026-10-27 | agent-bot-daemon is HQ; agent-bot-machine stays the provisioner. | In force; PDR-0002 records it in the catalog |
| agent-bot-daemon D2 | daemon plan section 10.1, owner 2026-10-27 | Provider keys that cannot be short-lived: resolved from the identity service at HQ start, memory only, named on receipts (pilot); per-task credentials or an inference gateway (target). | In force |
| agent-bot-daemon D3 | daemon plan section 10.1, owner 2026-10-27 | Hosted Souls stay possible: the soul-runtime core stays pure; no server-runtime work before the pilot gates. | In force |
| agent-bot-daemon D4 | daemon plan section 10.1, owner 2026-10-31 | Host-side credentials and policy live in agent-bot-machine's admin sandbox; owner presence is a Secure Enclave signature verified there. | In force; changes the trust-domain table, see [trust domains](../03-architecture/trust-domains-and-profiles.md) |
| agent-bot-daemon D5 | daemon plan section 10.1, owner 2026-11-07 | The WP1 contracts (schemas, fixtures, error registry) live in soul-contracts; agent-bot-daemon pins a release by digest and keeps no copies. | In force; PDR-0001 decision 3 gives soul-contracts the same scope |
| agent-bot-daemon D6 | daemon plan section 10.1, owner 2026-11-07 | HQ runs in its own OS account (`_agent-bot-hq` on macOS, `agent-bot-hq` on Linux), created by agent-bot-machine and separate from its admin sandbox. Members and the owner's account cannot read HQ's store. | In force; DRIFT-003 resolved by agent-bot-identity ADR-1381 |
| agent-bot-daemon D7 | daemon plan section 10.1, owner 2026-11-07 | On macOS each Soul member gets its own OS account, so two members on the same harness never share state (S6 section 4; T01 to T03). Agents the owner runs in their own account as delegates stay there. The SOP's per-harness account record is amended to per-member. | In force; settles the macOS principal for member isolation, which stays open for Linux |
| agent-bot-identity ADR-1183 | identity repository | Split agent-bot into daemon, identity, comms and soul-runtime repositories. | In force; duplicated in two other places (DRIFT-011) |
| agent-bot-identity ADR-0274 | identity repository | The product is mechanism; add-ons and SOP packs carry policy. | In force; candidate product principle |
| agent-comms ADR-0028 | comms repository, accepted 2026-10-11 | Federation policy for relays. | In force; constrains seam `wire-v1` |

## Open platform decisions

From whitepaper draft 0.4 section 16 (S6) and the repository plan's blocking decisions (S7 section 6). Each becomes a Decisions discussion when its stage needs it.

| Decision | Proposed baseline in S6 | Needed by |
|---|---|---|
| Owner authentication | Installing host account over the access-controlled socket; remote only through an owner-opened tunnel | Stage 1 |
| Authoritative task state | Task revisions, deduplication and action records in HQ's store; comms is a mirror | Stage 1 |
| Member isolation | Separate protected runtime principals with private state per member; Linux first | Stage 2a |
| Epoch semantics | Commit fence at the broker; routing hint in the frame; stale-epoch mail delivered | Stage 2b |
| Budget shape | One ceiling with working and maintenance sub-allocations | Stage 2b |
| Primitive rendering | Canonical primitives with per-adapter overrides; digests in `SoulLock.json` | Stage 3 |
| Candidate acceptance | Whole-candidate accept or reject per cell matrix; no partial acceptance in the MVP | Stage 3 |
| Sleep acceptance | Owner reviews control-affecting candidates in the MVP | Stage 3 |
| Notes durability | Durable batched dream inputs; scratch in tmp; no shutdown nap | Stage 3 |
| Definition naming | `SoulInfo.json` and `SoulLock.json` | Stage 3 |
| Federation cryptographic profile | Reviewed endpoint sealing and enrollment profile | Stage 4 |
| Installation authority placement | Owner-operated installation authority before partitioned takeover | Stage 4 |
| First protected platform | One Linux reference profile; macOS per-member accounts second | Stage 2a |
