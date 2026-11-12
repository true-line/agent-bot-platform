---
Status: Proposed
Doc-Type: governance
Owner: platform-maintainer
Last-Reviewed: 2026-11-11
---

# Resolved drift

Full records of the [drift register](drift-register.md) entries that are resolved: the conflict and what removed it. The register keeps each heading, so every DRIFT ID still resolves there. An entry moves here in the PR that resolves it; open entries stay in the register.

## DRIFT-001 R9 has two wordings

- **Conflict.** soul-contracts `traceability/REQUIREMENTS.md` carried R9 from draft 0.3. Draft 0.4 (S6) adds: "During an identity-service outage, only protected external effects that need a newly minted credential wait."
- **Resolved 2026-11-07.** [soul-contracts#26](https://github.com/true-line/soul-contracts/pull/26) replaced `traceability/`, `glossary/` and `papers/` with links to the platform at baseline/3 (PDR-0001). The platform registry's 0.4 wording is the only R9.

## DRIFT-002 Which repository is HQ

- **Conflict.** S1 D2, S6 section 3 and S7 make managed-machine (now agent-bot-machine) the HQ daemon. agent-bot-daemon's README and plan, and the current [architecture diagram](../03-architecture/overview.md), put HQ in agent-bot-daemon with agent-bot-machine as a secure executor that is never root.
- **Resolved 2026-11-07.** PDR-0002, accepted in its discussion, makes agent-bot-daemon HQ, and the [decision log](../04-decisions/decision-log.md) records S1 D2 as superseded. agent-bot-machine ADR-0001 already keeps HQ in agent-bot-daemon. S1, S6 and S7 stay frozen and are read with PDR-0002.

## DRIFT-003 Which account the daemon runs in

- **Conflict.** agent-bot-identity ADR-0332 ran one daemon per OS user in the Souls' account. S6 section 4 and agent-bot-daemon D1 run HQ in a separate account.
- **Resolved 2026-11-08.** agent-bot-daemon D6 puts HQ in its own OS account. agent-bot-identity ADR-1381 ([qwts/agent-bot-identity#1382](https://github.com/qwts/agent-bot-identity/pull/1382)) supersedes agent-bot-identity ADR-0332 decision 2 and cites agent-bot-daemon D6.

## DRIFT-014 Diagram provenance was swapped

- **Resolved 2026-11-07.** The soul-docs portal labeled the current diagram as the old privileged-daemon sketch and the reverse. The migration renamed them: `assets/architecture.mmd` is current and `assets/architecture-superseded-privileged-machine.mmd` is the older sketch.

## DRIFT-015 Draft 0.4.1 is cited but does not exist

- **Resolved 2026-11-07.** agent-bot-daemon's plan (section 10.1) and the soul-contracts glossary say a draft 0.4.1 changed S6's component table and Appendix C to name agent-bot-daemon as HQ instead of managed-machine. No 0.4.1 file exists: every copy of the whitepaper found is byte-identical to the S6 draft 0.4 pin. The one change it was meant to carry is recorded in PDR-0002 (decision 3) and the repository catalog.
- **Follow-up.** S6 stays draft 0.4. soul-contracts dropped the claim when its glossary moved to the platform ([soul-contracts#26](https://github.com/true-line/soul-contracts/pull/26)). When agent-bot-daemon adopts the platform block, it cites PDR-0002 instead of draft 0.4.1.

## DRIFT-016 The daemon plan gave HQ authority to other repositories

- **Conflict.** Before its platform adoption ([agent-bot-daemon#79](https://github.com/true-line/agent-bot-daemon/issues/79)), agent-bot-daemon's plan (sections 3.1 and 9) assigned work against the catalog's charters:
  - **agent-bot-identity** as HQ's identity plugin, holding the device signer, grants, grant handles, approvals and credential references. The catalog puts agent-bot-identity inside the Soul and gives these to agent-bot-daemon.
  - **agent-comms** holding the task service, budgets and the action ledger. The catalog gives these to agent-bot-daemon, and PDR-0024 makes it the `task-v1` provider.
  - **One soul-runtime repository** holding the package format, validator, render and adapter manifests. The catalog gives these to soul-package and soul-adapters.
  - **An SDK `wire/` folder** in agent-bot-daemon, which does not own wire framing. The folder holds shared codecs (binding proof, presence verifier, canonical JSON), not framing.
- **Resolved 2026-11-08.** [agent-bot-daemon#83](https://github.com/true-line/agent-bot-daemon/pull/83) made the plan follow the catalog and named the codecs non-framing. [PDR-0027](../04-decisions/PDR-0027-hq-identity-authority-lives-in-agent-bot-daemon.md) answered discussion #27: HQ identity authority is built into agent-bot-daemon; agent-bot-identity's plugin registers member surfaces only.
