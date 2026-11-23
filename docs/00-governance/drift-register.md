---
Status: Proposed
Doc-Type: governance
Owner: platform-maintainer
Last-Reviewed: 2026-11-17
---

# Drift register

Follow each resolution or raise a Decisions discussion. Retain every heading;
move completed entries to [resolved drift](drift-register-resolved.md).

## DRIFT-001 R9 has two wordings

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-001-r9-has-two-wordings).

## DRIFT-002 Which repository is HQ

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-002-which-repository-is-hq).

## DRIFT-003 Which account the daemon runs in

- **Resolved 2026-11-08.** [Full record](drift-register-resolved.md#drift-003-which-account-the-daemon-runs-in).

## DRIFT-004 Wire and task contracts exist twice

- **Open.** agent-comms' NDJSON wire and task table diverge from the soul-contracts `wire/v1` and nine-state, HQ-authoritative `task/v1` seams (S6 §§6–7).
- **Resolution.** [PDR-0024](../04-decisions/PDR-0024-comms-mirrors-task-v1-and-frames-wire-v1.md): comms mirrors HQ tasks and frames routed messages against both contract fixture sets. Its local protocol and v0.5.5 workflow remain outside those seams until the adoption PR merges.

## DRIFT-005 Two products called headquarters

- **Open.** agent-watchtower ADR-0012 claims a second headquarters and approvals; S6 gives HQ sole local authority and S7 gives the watcher observability.
- **Decided 2026-11-07.** [PDR-0002](../04-decisions/PDR-0002-repository-topology-and-admission.md) keeps watchtower a separate read-only security product.
- **Resolution.** Watchtower removes its control claims and supersedes its ADR.

## DRIFT-006 GeniusBar or DudlesBar

- **Open.** S6/S7 use GeniusBar; geniusbar ADR-0417 says DudlesBar.
- **Decided 2026-11-07.** GeniusBar remains a code name; DudlesBar is not adopted. A public name is required before release (RISK-010).
- **Resolution.** The owner selects the name; the glossary and geniusbar ADR follow.

## DRIFT-007 Two Soul package layouts

- **Open.** agent-bot-identity's `soul-package.md` doc defines formats 1 and 2 (`soul.json`, `AGENTS.md`, `skills/`). S6 section 11 and agent-bot-daemon plan section 5 define the `Contents/` layout with `SoulInfo.json` and `SoulLock.json`.
- **Resolution.** The `soul-package-format` seam in soul-package is the single home; identity documents formats 1 and 2 as legacy import paths only.

## DRIFT-008 More than one engineering process source

- **Open.** Process guidance exists in qwts/qwts-agent-sop (22 SDLC guides), true-line/engineering-relay (23 guides) and qwts/qwts-agent-sdlc. agent-watchtower's governed block points to qwts/playbook-engineering; agent-bot-identity's AGENTS.md links both qwts/agent-sop and qwts/qwts-agent-sop.
- **Resolution.** The platform links one process source through its governed block. Choosing between the others is an org decision, outside this repository.

## DRIFT-009 "Soul" and "principal" mean different things

- **Open.** S6, agent-comms ADR-0003 and agent-bot README use incompatible Soul/principal meanings. [PDR-0053](../04-decisions/PDR-0053-soul-life-and-agent-replace-member.md) and the [glossary](../glossary.md) define Soul as a package.
- **Resolution.** Components adopt the glossary; comms marks its older meaning superseded.

## DRIFT-010 Short labels collide

- **Open.** S6 reference R1–R8 and daemon risk R1–R10 collide with requirements; daemon decision labels collide with S1 decisions.
- **Resolution.** [Identifiers](identifiers.md) use X, qualified D and RISK labels; daemon renames its risks.

## DRIFT-011 The split decisions are recorded three times

- **Open.** The daemon, identity, comms and soul-runtime split appears in agent-bot-identity ADR-1183, agent-bot-daemon plan section 10.1 and ENG-0111.
- **Resolution.** The cross-repo part becomes one PDR; the other records cite it.

## DRIFT-012 The identity service has two addresses

- **Open.** Agent Bot, daemon and identity docs name `agent-bot-gold.vercel.app` while S6 uses `agents.true-line.ai`.
- **Decided 2026-11-07.** The latter is canonical; the former remains a deployment alias.
- **Resolution.** Components document the alias and canonical host in true-line/agent-bot#154, true-line/agent-bot-daemon#79 and qwts/agent-bot-identity#1378.

## DRIFT-013 Planned repository names do not exist

- **Open.** agent-bot-daemon's plan names `agent-bot-soul`, `agent-bot-soul-runtime` and `agent-bot-comms`; the repositories are agent-bot-souls (empty) and agent-comms. Its README links `qwts/agent-bot-daemon#1` although the repository is in true-line.
- **Resolution.** PDR-0002 fixes the names in `registry/repos.yaml`; agent-bot-daemon's plan links there.

## DRIFT-014 Diagram provenance was swapped

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-014-diagram-provenance-was-swapped).

## DRIFT-015 Draft 0.4.1 is cited but does not exist

- **Resolved 2026-11-07.** [Full record](drift-register-resolved.md#drift-015-draft-041-is-cited-but-does-not-exist).

## DRIFT-016 The daemon plan gave HQ authority to other repositories

- **Resolved 2026-11-08.** [Full record](drift-register-resolved.md#drift-016-the-daemon-plan-gave-hq-authority-to-other-repositories).

## DRIFT-017 Component records still say "member"

- **Open.** PDR-0053 retires "member" for what runs in a harness and makes the account unit one OS account per harness credential. soul-contracts prose and field descriptions, and agent-bot-comms, agent-bot-souls and agent-bot-machine prose, still say "member". agent-bot-hq D7 and its plan rows 16a to 16d give each member its own OS account and keep state in the member's home.
- **Resolution.** Each repository corrects its prose to the [glossary](../glossary.md); contract field names such as `member_id` stay. agent-bot-hq replaces the account unit in agent-bot-hq D7 with PDR-0053's.

## DRIFT-018 Profile values say "managed" for Souls HQ does not start

- **Open.** PDR-0055 requires HQ to start managed Souls, but CLI-started
  Souls report `managed-protected` or `managed-cooperative` and HQ lacks a
  Soul start plan.
- **Resolution.** Only HQ-started Souls may report a managed profile. Direct
  IDE, CLI and web sessions remain unmanaged. Open until the Soul runner,
  contract claim rules and conformance checks enforce this.

## DRIFT-019 Control authority when a machine links to Harbor

- **Resolved 2026-11-11.** [Full record](drift-register-resolved.md#drift-019-control-authority-when-a-machine-links-to-harbor).

## DRIFT-020 Two UI repositories have no charter

- **Conflict.** agent-bot-hq-ui and agent-bot-harbor-ui exist without `registry/repos.yaml` charters, contrary to [PDR-0002](../04-decisions/PDR-0002-repository-topology-and-admission.md). Harbor UI still names an old product and destination.
- **Decided 2026-11-11.** [PDR-0047](../04-decisions/PDR-0047-harbor-is-the-control-plane-of-a-linked-machine.md) keeps both as HQ/Harbor design sources.
- **Resolution.** Add charters before implementation; Harbor UI uses Harbor and drops the agent-bot-ui destination.

## DRIFT-021 T14 previous-major and profile evidence

- **Resolved.** The conformance overview correction merged before the Stage 0 closeout. [Full record](drift-register-resolved.md#drift-021-t14-previous-major-and-profile-evidence).

## DRIFT-022 Pilot host order

- **Open.** S6 and HQ scheduled protected Linux first. [PDR-0085](../04-decisions/PDR-0085-macos-first-protected-pilot.md) moved protected macOS ahead of the pilot. Align HQ, Machine and conformance plans and trackers. Each host needs its own evidence.

## DRIFT-023 Privileged host key custody

- **Open.** HQ-local signing must satisfy [PDR-0093](../04-decisions/PDR-0093-standalone-hq-secure-enclave-signing.md). Close when all affected paths enforce [PDR-0091](../04-decisions/PDR-0091-host-privileged-custody.md) and have qualifying evidence.

## DRIFT-024 Harness egress isolation

- **Open.** HQ's plan and Machine's Linux firewall differ from [PDR-0052](../04-decisions/PDR-0052-process-isolation-for-harness-egress.md). Reconcile both and verify T03.

## DRIFT-025 Stage 2a snapshot custody

- **Conflict.** The owner rejected a root helper and selected Machine-admin
  custody for Agent Bot managed inputs, frozen snapshots and spent claims.
  Current root-owned text, Contracts UID-0 records and Machine/HQ drafts
  disagree. [PDR-0121](../04-decisions/PDR-0121-machine-admin-custody-for-stage-2a-snapshots.md)
  records the proposed successor.
- **Resolution.** Version Contracts and Machine/HQ together; require
  matching installed bytes and physical T01–T03/T21 evidence before use.

## DRIFT-026 Machine admin network providers

- **Conflict.** Machine admin providers/downloads and keyd GitHub requests
  perform direct network I/O despite
  [PDR-0091](../04-decisions/PDR-0091-host-privileged-custody.md)
  and the owner's longstanding HQ-mediated boundary.
- **Resolution.** HQ performs network exchange over authenticated local
  requests; Machine admin/root paths and children are denied direct IPv4,
  IPv6 and DNS. Refuse unavailable routes and prove denial on the host.
