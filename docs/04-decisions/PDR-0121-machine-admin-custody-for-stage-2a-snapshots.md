---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-22
Last-Reviewed: 2026-11-22
Discussion: https://github.com/true-line/agent-bot-platform/discussions/121
Amends: PDR-0102
Affects-Repos: [agent-bot-platform, soul-contracts, agent-bot-machine, agent-bot-hq, agent-bot-souls, soul-conformance]
Affects: [R3, R8, trust-model]
---

# PDR-0121 Keep Stage 2a snapshots in Machine admin custody

The product owner rejected a root helper for Stage 2a snapshot and one-use
claim mechanics. The secure Machine administrative account is trusted to
manage files on its host; adding a root helper would expand privileged
execution without serving that trust model. This decision changes the
qualification-only Agent Bot managed source, frozen snapshot and claim custody specified by
[PDR-0102](PDR-0102-protected-adapter-qualification.md). It does not grant a
protected launch or a physical test result. [Decision discussion and recorded
owner direction](https://github.com/true-line/agent-bot-platform/discussions/121#discussioncomment-19815746).

## Context

The controlled Stage 2a measurement interface currently requires root-owned
host projection, executable inputs, staging and snapshots. The Contracts
draft fixes snapshot `owner_uid` at zero, while Machine's draft publisher
and reservation path require root. The paired daemon runs as secure admin.
No reviewed offline installer supplies arbitrary exact root-owned launch
inputs for this path. The owner rejected a new root helper. This is
[DRIFT-025](../00-governance/drift-register.md#drift-025-stage-2a-snapshot-custody).

## Decision

1. The reviewed Machine installation identifies one secure administrator
   account A. Machine stages and publishes the exact approved Definition and
   launch-input snapshots, and durably spends each one-use start claim, under
   A. The owner-approved plan and authenticated installation pin A's account
   identity and numerical UID. HQ and incoming signed records cannot choose
   A. No root helper is installed or invoked for snapshot or claim mechanics
   at installation, before launch or during a start.
2. A must be distinct from HQ, runner R, bridge B and credential account C.
   The owner may choose a single-account machine, but a host unable to
   provide the separate accounts required by a protected profile refuses
   that profile. The required distinction is a property of the selected
   profile, not a limit on the owner's control of their machine.
3. A-owned snapshot and claim directories have verified private ancestry.
   Agent Bot managed host projection, executable, module, configuration and
   policy inputs are also A-owned and measured separately from the frozen
   Soul Definition. OS images retain OS custody and are bound by the
   recorded macOS build and signing requirements.
   Machine copies through no-follow descriptors, validates the approved
   inventory and each file's owner, group, mode, link count, ACL, identity
   and hash, syncs staged files and directories, and atomically publishes
   the read-only snapshot. R receives only the read and traversal access
   needed for its own start. HQ, R, B, C and sibling installations cannot
   write, replace, rename or delete inputs, snapshots or claims. Machine
   checks exact descriptors and bytes before authorization. HQ initiates
   the fixed reviewed R/B launcher using Machine's signed one-use binding;
   the launcher rechecks the pinned identities and bytes immediately before
   its own exec and proves the selected runtime closure. Machine observes
   the actual child before finalization. No unguarded reopen or late
   unreviewed load qualifies. A and root are trusted to manage these files;
   an A-owned file is not immutable against another A process. This decision
   does not authorize a new root helper for account transition. The
   existing fixed sudo rule and launcher require separate review and
   physical enforcement; any privileged transition has no direct network.
4. Machine serializes and durably records each exact one-use claim before
   returning a reservation. Failed and uncertain attempts remain spent.
   A and root are trusted not to remove or roll back claim state. Suspected
   rollback or uncertain durability refuses until a fresh owner-approved
   recovery; moving the claim directory cannot reset old spent names.
5. The existing [PDR-0091](PDR-0091-host-privileged-custody.md) boundary
   forbids direct network from Agent Bot secure-admin or root processes in
   every profile and path, including setup, migration and recovery.
   Existing Machine admin download providers violate it
   ([DRIFT-026](../00-governance/drift-register.md#drift-026-machine-admin-network-providers))
   and must use HQ's authenticated local exchange or refuse. Installed
   confinement must deny direct IPv4 and IPv6
   traffic and DNS/provider access on the designated host; permitted local
   IPC is explicit and cannot act as a general network proxy. HQ handles
   network exchange in its unprivileged account through purpose-limited,
   authenticated local Machine requests. An unverified deny or an
   unavailable local channel refuses protected qualification.
6. Independent host projection and executable source measurements remain
   in force under A custody for Agent Bot managed bytes. This changes their
   ownership as well as frozen copies and one-use claims. The approved
   measurements, selected command and arguments, account
   assignment, Machine signature, HQ finalization, completed-run evidence
   and physical T01–T03/T21 gates still apply.

## Consequences

- The [controlled measurement interface](../03-architecture/interfaces/stage2a-measurement.md)
  states the replacement custody rule. No protected positive path may mix
  old root-owned and new A-owned records.
- soul-contracts must version snapshot identity, launch-input custody,
  canonical vectors and signed reservation/host-report references. A verifier compares the
  snapshot UID to authenticated installation and plan state; it does not
  accept an arbitrary nonzero UID from a signed record.
- agent-bot-machine must update snapshot publisher/observer, measurement
  binding, host projection and code-input custody, one-use claim, offline
  host-report verifier and tests together.
  It must preserve no-follow, durability, replay and spent-name checks and
  add a callable, purpose-limited admin authorization and signing path.
- agent-bot-hq and agent-bot-souls must pin the compatible contract and
  installation identity, refuse mixed versions, and prove that the exact
  measured inputs are executed under assigned accounts. The final launcher
  handoff remains an open implementation gate.
- soul-conformance and physical acceptance must test wrong/shared A,
  R/B/HQ/C and sibling write denial, byte and inode replacement, replay
  and restart, direct IPv4/IPv6 denial for privileged processes, the
  permitted local channel, and the actual selected code closure. Source
  fixtures and synthetic signatures do not count as host proof.
- DRIFT-025 remains open until the published contract, implementation,
  installed release and physical evidence agree with this decision.

## Alternatives considered

- A per-launch root helper could create root-owned snapshots and switch
  target UIDs. The owner rejected its added privileged surface.
- A root-owned snapshot without a helper leaves the existing nonroot
  Machine producer unable to construct the specified artifact.
