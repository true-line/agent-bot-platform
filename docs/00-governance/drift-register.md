---
Status: Proposed
Doc-Type: governance
Owner: platform-maintainer
Last-Reviewed: 2026-11-11
---

# Drift register

Known places where two sources of truth disagree. An agent that meets one of these does not pick a side: it follows the resolution path or raises a Decisions discussion. Entries are never deleted. A resolved entry keeps its heading here, and its full record, with what removed the conflict, moves to [resolved drift](drift-register-resolved.md). DRIFT-001 to DRIFT-015 were found by the 2026-11-07 survey.

## DRIFT-001 R9 has two wordings

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-001-r9-has-two-wordings).

## DRIFT-002 Which repository is HQ

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-002-which-repository-is-hq).

## DRIFT-003 Which account the daemon runs in

- **Resolved 2026-11-08.** [Full record](drift-register-resolved.md#drift-003-which-account-the-daemon-runs-in).

## DRIFT-004 Wire and task contracts exist twice

- **Open.** agent-comms ships NDJSON wire v1 (`lib/wire.mjs`) and a task state table (its `tasks.md` doc) that do not reference soul-contracts. S6 sections 6 and 7 specify `wire/v1` and `task/v1` with nine HQ-authoritative states and comms as a mirror.
- **Resolution.** [PDR-0024](../04-decisions/PDR-0024-comms-mirrors-task-v1-and-frames-wire-v1.md): the schemas are in soul-contracts `wire/v1` and `task/v1`. agent-comms mirrors HQ's `task/v1` records through a codec, frames routed messages in `wire/v1` at its broker layer, and runs every fixture of both against them. Its v0.5.5 task workflow and local client protocol stay, documented as outside the seams. Resolved when that agent-comms PR merges.

## DRIFT-005 Two products called headquarters

- **Open.** agent-watchtower calls itself "agent coordination headquarters" with its own control plane and approvals (agent-watchtower ADR-0012). S6 defines HQ as the single local authority; S7 scopes the watcher to observability.
- **Decided 2026-11-07, open until the repository changes.** The owner made agent-watchtower a standalone security product on top of the platform (PDR-0002). It consumes `hq-v1` read-only and holds no control authority.
- **Resolution.** agent-watchtower drops the "headquarters" claim, its own control plane and its approvals, superseding agent-watchtower ADR-0012.

## DRIFT-006 GeniusBar or DudlesBar

- **Open.** S6, S7 and these docs say GeniusBar. The geniusbar repository renamed the product DudlesBar (geniusbar ADR-0417).
- **Decided 2026-11-07, name still open.** GeniusBar is the code name; DudlesBar is not adopted. A product name is chosen before any public release, because "Genius Bar" is an Apple service name (RISK-010).
- **Resolution.** The owner picks the product name; the glossary records it with GeniusBar as the former code name, and the geniusbar repository supersedes geniusbar ADR-0417.

## DRIFT-007 Two Soul package layouts

- **Open.** agent-bot-identity's `soul-package.md` doc defines formats 1 and 2 (`soul.json`, `AGENTS.md`, `skills/`). S6 section 11 and agent-bot-daemon plan section 5 define the `Contents/` layout with `SoulInfo.json` and `SoulLock.json`.
- **Resolution.** The `soul-package-format` seam in soul-package is the single home; identity documents formats 1 and 2 as legacy import paths only.

## DRIFT-008 More than one engineering process source

- **Open.** Process guidance exists in qwts/qwts-agent-sop (22 SDLC guides), true-line/engineering-relay (23 guides) and qwts/qwts-agent-sdlc. agent-watchtower's governed block points to qwts/playbook-engineering; agent-bot-identity's AGENTS.md links both qwts/agent-sop and qwts/qwts-agent-sop.
- **Resolution.** The platform links one process source through its governed block. Choosing between the others is an org decision, outside this repository.

## DRIFT-009 "Soul" and "principal" mean different things

- **Open.** S6 section 3 defines a Soul as a persistent multi-member agent and a principal as a human or organization; the platform [glossary](../glossary.md) carries those definitions since soul-contracts moved its glossary there ([soul-contracts#26](https://github.com/true-line/soul-contracts/pull/26)). agent-comms ADR-0003 defines a soul as one agent conversation (`agent_<uuid>`) and a principal as a human or transport account; agent-bot's README uses the agent-comms meaning.
- **Resolution.** The platform [glossary](../glossary.md) is the single home after PDR-0001; agent-comms records the older meaning as superseded.

## DRIFT-010 Short labels collide

- **Open.** S6 labels its external references `R1` to `R8`, beside its requirements R1 to R12. agent-bot-daemon's plan labels its decisions `D1` to `D4` and its risks `R1` to `R10`, colliding with the north star's decisions (S1 D1 to S1 D4) and with the requirements.
- **Resolution.** Platform side resolved by [identifiers](identifiers.md) (X-series, qualified labels, RISK-series). agent-bot-daemon renames its risks when its plan moves here.

## DRIFT-011 The split decisions are recorded three times

- **Open.** The daemon, identity, comms and soul-runtime split appears in agent-bot-identity ADR-1183, agent-bot-daemon plan section 10.1 and ENG-0111.
- **Resolution.** The cross-repo part becomes one PDR; the other records cite it.

## DRIFT-012 The identity service has two addresses

- **Open.** S6 and the architecture name `agents.true-line.ai`. agent-bot's README and code comments, agent-bot-daemon's plan and agent-bot-identity's server-mode documentation and tests also use `agent-bot-gold.vercel.app`.
- **Decided 2026-11-07, open until the repositories change.** The owner made `agents.true-line.ai` the canonical address. `agent-bot-gold.vercel.app` is a deployment alias: it keeps serving existing clients, and agent-bot already treats it as a legacy host. Documents name only the canonical address.
- **Resolution.** agent-bot records the alias, and agent-bot, agent-bot-daemon and agent-bot-identity replace it in their documents. Their adoption issues carry the item: true-line/agent-bot#154, true-line/agent-bot-daemon#79 and qwts/agent-bot-identity#1378.

## DRIFT-013 Planned repository names do not exist

- **Open.** agent-bot-daemon's plan names `agent-bot-soul`, `agent-bot-soul-runtime` and `agent-bot-comms`; the repositories are agent-bot-souls (empty) and agent-comms. Its README links `qwts/agent-bot-daemon#1` although the repository is in true-line.
- **Resolution.** PDR-0002 fixes the names in `registry/repos.yaml`; agent-bot-daemon's plan links there.

## DRIFT-014 Diagram provenance was swapped

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-014-diagram-provenance-was-swapped).

## DRIFT-015 Draft 0.4.1 is cited but does not exist

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-015-draft-041-is-cited-but-does-not-exist).

## DRIFT-016 The daemon plan gave HQ authority to other repositories

- **Resolved 2026-11-08.** [Full record](drift-register-resolved.md#drift-016-the-daemon-plan-gave-hq-authority-to-other-repositories).

## DRIFT-017 Control authority when a machine links to Harbor

- **Conflict.** On 2026-11-11 the owner directed that HQ alone is a complete, supported deployment that may never link to Harbor, and that when a machine does link, Harbor becomes its control plane: a more secure control plane plus agent federation. The controlled records say remote tiers never hold control:
  - **R2** (Approved): "Only local HQ controls lifecycle and protected operations on its host", and the owner's administrative channel terminates at local HQ.
  - **S6 §4**: remote administration never crosses a relay; the owner reaches `hq/v1` only through a tunnel the owner opens. The [decision log](../04-decisions/decision-log.md) carries the same baseline for the open "Owner authentication" decision.
  - **[PDR-0023](../04-decisions/PDR-0023-hq-observation-uplink-for-presence-bindings-and-events.md)** and the `observation-v1` seam: Harbor keeps a read-only projection, and the uplink carries no control or execution path.
  - The **agent-bot charter** in `registry/repos.yaml`: Harbor is trusted for credential custody and issuance only, and must not own lifecycle or any control path to a host.
  - The [architecture overview](../03-architecture/overview.md) and [federation](../03-architecture/federation.md) pages: remote tiers hold no control authority. The overview's diagram already labels agent-bot "control plane" beside HQ's "local control plane", so the page disagrees with itself.
- **Open.** No side is chosen here. R2 and PDR-0023 stay in force until a PDR is accepted. [Discussion #47](https://github.com/true-line/agent-bot-platform/discussions/47) asks the question, and [PDR-0047](../04-decisions/PDR-0047-harbor-is-the-control-plane-of-a-linked-machine.md) is Proposed.

## DRIFT-018 Two UI repositories have no charter

- **Conflict.** true-line/agent-bot-hq-ui (the on-machine HQ interface) and true-line/agent-bot-harbor-ui (Harbor console designs, a remote view of one machine's settings in `daemon-ui/`, and MCP app resources in `mcp-apps/`) exist. Neither has an entry in `registry/repos.yaml`. [PDR-0002](../04-decisions/PDR-0002-repository-topology-and-admission.md) admits no repository without a charter, keeps the web console in agent-bot and says the planned agent-bot-ui is not created. agent-bot-harbor-ui's README still calls the product "Agent Command Center", not Harbor, and names agent-bot-ui as its destination.
- **Open.** Discussion #47 and PDR-0047 also ask which plane each interface belongs to and whether these two repositories get charters or merge into agent-bot-hq and agent-bot.
