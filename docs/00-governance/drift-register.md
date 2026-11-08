---
Status: Proposed
Doc-Type: governance
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
---

# Drift register

Known places where two sources of truth disagree. An agent that meets one of these does not pick a side: it follows the resolution path or raises a Decisions discussion. Entries are never deleted; a resolved entry records what removed the conflict. DRIFT-001 to DRIFT-015 were found by the 2026-11-07 survey.

## DRIFT-001 R9 has two wordings

- **Conflict.** soul-contracts `traceability/REQUIREMENTS.md` carried R9 from draft 0.3. Draft 0.4 (S6) adds: "During an identity-service outage, only protected external effects that need a newly minted credential wait."
- **Resolved 2026-11-07.** [soul-contracts#26](https://github.com/true-line/soul-contracts/pull/26) replaced `traceability/`, `glossary/` and `papers/` with links to the platform at baseline/3 (PDR-0001). The platform registry's 0.4 wording is the only R9.

## DRIFT-002 Which repository is HQ

- **Conflict.** S1 D2, S6 section 3 and S7 make managed-machine (now agent-bot-machine) the HQ daemon. agent-bot-daemon's README and plan, and the current [architecture diagram](../03-architecture/overview.md), put HQ in agent-bot-daemon with agent-bot-machine as a secure executor that is never root.
- **Resolved 2026-11-07.** PDR-0002, accepted in its discussion, makes agent-bot-daemon HQ, and the [decision log](../04-decisions/decision-log.md) records S1 D2 as superseded. agent-bot-machine ADR-0001 already keeps HQ in agent-bot-daemon. S1, S6 and S7 stay frozen and are read with PDR-0002.

## DRIFT-003 Which account the daemon runs in

- **Open.** agent-bot-identity ADR-0332 (Accepted) runs one daemon per OS user in the Souls' own account. S6 section 4 and agent-bot-daemon D1 run HQ in a separate account. agent-bot-identity ADR-1183 does not supersede agent-bot-identity ADR-0332.
- **Decided 2026-11-07, open until the repository changes.** agent-bot-daemon D6 runs HQ in its own OS account, separate from the members and from agent-bot-machine's admin sandbox. That is the platform position.
- **Resolution.** A new agent-bot-identity ADR supersedes agent-bot-identity ADR-0332 and cites agent-bot-daemon D6.

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

- **Resolved 2026-11-07.** The soul-docs portal labeled the current diagram as the old privileged-daemon sketch and the reverse. The migration renamed them: `assets/architecture.mmd` is current and `assets/architecture-superseded-privileged-machine.mmd` is the older sketch.

## DRIFT-015 Draft 0.4.1 is cited but does not exist

- **Resolved 2026-11-07.** agent-bot-daemon's plan (section 10.1) and the soul-contracts glossary say a draft 0.4.1 changed S6's component table and Appendix C to name agent-bot-daemon as HQ instead of managed-machine. No 0.4.1 file exists: every copy of the whitepaper found is byte-identical to the S6 draft 0.4 pin. The one change it was meant to carry is recorded in PDR-0002 (decision 3) and the repository catalog.
- **Follow-up.** S6 stays draft 0.4. soul-contracts dropped the claim when its glossary moved to the platform ([soul-contracts#26](https://github.com/true-line/soul-contracts/pull/26)). When agent-bot-daemon adopts the platform block, it cites PDR-0002 instead of draft 0.4.1.

## DRIFT-016 The daemon plan gave HQ authority to other repositories

- **Open.** Before its platform adoption ([agent-bot-daemon#79](https://github.com/true-line/agent-bot-daemon/issues/79)), agent-bot-daemon's plan (sections 3.1 and 9) assigned work against the catalog's charters:
  - **agent-bot-identity** as HQ's identity plugin, holding the device signer, grants, grant handles, approvals and credential references. The catalog puts agent-bot-identity inside the Soul and gives these to agent-bot-daemon.
  - **agent-comms** holding the task service, budgets and the action ledger. The catalog gives these to agent-bot-daemon, and PDR-0024 makes it the `task-v1` provider.
  - **One soul-runtime repository** holding the package format, validator, render and adapter manifests. The catalog gives these to soul-package and soul-adapters.
  - **An SDK `wire/` folder** in agent-bot-daemon, which does not own wire framing. The folder holds shared codecs (binding proof, presence verifier, canonical JSON), not framing.
- **Not settled by the catalog.** Whether agent-bot-identity, which consumes `hq-plugin-contract` from inside the Soul, ships HQ-side plugin code or only member surfaces: [discussion #27](https://github.com/true-line/agent-bot-platform/discussions/27).
- **Resolution.** agent-bot-daemon's adoption PR makes its plan follow the catalog for the first three items and names its codecs as non-framing. The entry closes when that PR merges and discussion #27 is decided.
