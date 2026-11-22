---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-21
Last-Reviewed: 2026-11-21
Discussion: https://github.com/true-line/agent-bot-platform/discussions/102
Affects-Repos: [agent-bot-platform, agent-bot-machine, agent-bot-hq, agent-bot-souls, agent-bot-comms, soul-adapters, soul-contracts, soul-conformance]
Affects: [R8, trust-model]
---

# PDR-0102 Verify protected adapter qualification offline

The owner approved this trust model for protected adapter launches. A package
build identifies what was produced. Qualification also requires independent
evidence of how the exact package and harness behaved on the declared host.
[Owner decision](https://github.com/true-line/agent-bot-platform/discussions/102#discussioncomment-19798348).

## Evidence and certification

Only a designated qualification host may sign test evidence. Ordinary device
enrollment grants no such authority. On macOS, the independent conformance
runner supplies a fixed report. Machine/keyd signs that report under the
administrator account. HQ cannot request signatures over arbitrary input.
The physical Mac gate requires T01, T02 and T03 under protected enforcement
and T21 under cooperative enforcement. [macOS pilot decision](PDR-0085-macos-first-protected-pilot.md).

To collect evidence before an adapter's first certification, the owner may
approve a single qualification run on a designated test Mac. The approval
identifies the exact candidate adapter and test plan and is consumed once.
The independent runner exercises the real controls with disposable member
state and a test provider. A protected result requires observed enforcement.
When a report claims a managed profile, HQ must have started the Soul through
the Soul runner. A direct vendor, IDE or web session remains unmanaged even if
Harbor policy or local hooks constrain it
([PDR-0055](PDR-0055-a-soul-is-managed-when-hq-starts-it.md)).
The run produces evidence for review. Its approval grants no authority for
ordinary HQ work, a reusable launch rule or release certification.
[Owner decision on first qualification](https://github.com/true-line/agent-bot-platform/discussions/102#discussioncomment-19798697).

One designated release workflow in `true-line/soul-adapters` may certify a
qualification after verifying the host-signed passing results. The owner pins
the release source, workflow identity and authorized evidence signers in signed
policy. The qualification attestation has its own type. Its subject is the digest
of the exact bytes of `qualification.json`. The record binds the package and
native harness digests, executable, ordered arguments, code inputs, host,
enforcement profile, suite revision and results. The adapter manifest references
the signed attestation. Build provenance alone cannot authorize a protected launch.

The fixed purpose, canonical report bytes, host and owner signature envelopes,
and offline verification sequence live in the [qualification signature
contract draft](https://github.com/true-line/soul-contracts/pull/49).
Machine may ask keyd to sign only after the one-use attempt has an immutable
completed-run record and Machine has independently observed the actual
HQ-started Soul process, runner, account identities and enforcement profile.
An HQ launch receipt or a `started` attempt alone cannot establish those facts.
The report signer must be explicitly designated for that host in owner policy;
device enrollment does not designate it. A release workflow must verify the
host signatures before issuing its separate qualification attestation.

## Controlled Stage 2a Soul measurement

The product owner approved this qualification-only byte rule in the Stage 2a
working session on 2026-11-21. It permits one owner-approved attempt on the
designated Mac with the existing `soul-conformance` `hello.soul` lineage. It
does not authorize ordinary HQ work, a reusable protected launch, or a general
Stage 3 `.soul` import verifier. The exact owner-approved attempt names the
candidate, suite and template revisions, installed plan, frozen file inventory,
and expected measurements. A changed path, byte, mode or launch input needs a
new plan and one-use approval.
The approval covers one exact suite plan. Each actual Soul start in that plan,
including the cooperative T21 replay or a restart, needs its own distinct
durably spent Machine reservation; a protected reservation cannot be replayed
for a cooperative start.

Machine independently measures a closed, frozen `Contents/` definition and
reconstructible tree. It includes `SoulInfo.json`, `SoulLock.json`, every file
and directory under `primitives/` (Definition), and every file and directory
under `opt/` (Reconstructible). For the current `hello.soul` template this is
four files: SoulInfo, SoulLock, `primitives/quickstart-task.json`, and
`opt/quickstart-adapter.mjs`. The measured inventory must exactly equal the
owner-approved inventory. Unknown top-level paths or extra files in the
frozen source refuse. No file may be omitted by a wildcard. This is an exact
installation and launch byte closure; it does not establish the semantic
validity or portability of a package.

Life (`workspaces/`, `home/`, `memorial/`, `dreams/`, `comms/`), Rebuilt
(`cache/`), Recreated (`host/`) and Dropped (`tmp/`) state lives in separate
runner-owned writable paths, outside the frozen source. It cannot supply
unreviewed executable, module, configuration, policy or checker bytes for the
qualified run. The current template executes `workspaces/scratch/check.mjs`
from writable Life. Before a protected qualification, move that checker into
the frozen `opt/` closure or an independently measured root-owned launch-input
projection and invoke it from there. `answer.txt` remains writable evidence;
record the seeded issue/answer and final answer as test input and outcome.

Machine separately measures the root-owned host projection (including exact
`adapters.json` and `installation.json` values), runner, Machine, HQ, broker,
adapter, native harness and test-provider binaries/configuration, sandbox
policy, all executable code inputs, and the selected command and ordered
arguments. No `PATH` search, shell expansion, network fetch, late generated
executable, unenumerated non-system image or unsigned code module may supply
launch bytes. System images are bound by the recorded macOS build and code
signing requirement. An undeclared dynamic load or a late import from Life or
host state refuses protected qualification. An observed import inventory must
show the exact selected Node, HQ and comms code closure; counting the whole
release archive is not proof that the selected closure is complete or within
the limit below.

Each frozen directory and regular file has one canonical record: root-relative
ASCII path, `kind` (`directory` or `regular`), four-digit octal POSIX permission
mode, and for a file unsigned byte size and lowercase SHA-256 of its exact
descriptor-read bytes. Records sort by unsigned UTF-8 path bytes and serialize
as RFC 8785 JCS UTF-8 without BOM or newline. Duplicate, non-ASCII,
case-folding or Unicode-normalization aliases, empty or `..` path components,
symlinks, hard links, devices, sockets, writable ancestors and ACL allow
entries refuse. Machine computes
`sha256:` plus lowercase hex of
`SHA256(ASCII("agent-bot/stage2a-definition-opt-closure/v1") || 0x00 ||
JCS(definition_records))`. The separately canonicalized launch-input records
use the distinct prefix `agent-bot/stage2a-launch-inputs/v1` with the same
NUL and JCS rule. Owner, group, device, inode and timestamps are custody
checks, not portable digest members.

This constrained path permits at most 512 frozen entries, 256 MiB per regular
file and 1 GiB total frozen bytes; at most 64 external launch-input files have
the same per-file and aggregate limits. Exceeding a limit refuses before
hashing. A larger or different Soul requires an explicit reviewed rule, not
an implicit limit bypass. If the observed selected runtime needs more than 64
external files, this qualification path refuses even when the archive itself
is a valid release. `SoulLock.json.definition_digest` is a claimed
accepted revision, not a measurement of its own containing file. The exact
one-use owner-approved plan maps `(soul_id, claimed_definition_digest,
definition_measurement)`; Machine and HQ refuse a matching self-claim without
that accepted mapping or if authenticated Hello disagrees.

Machine copies approved source and code through no-follow directory
descriptors into a private root-owned staging tree. It verifies one-link
regular files and protected ancestors, hashes the bytes actually opened,
syncs every staged file and directory, then atomically publishes a read-only
root-owned snapshot and syncs its parent. It launches only that snapshot,
retaining or reopening descriptors and comparing identities and hashes
immediately before exec. The sandbox denies runner writes to source and host
projection from the first instruction. An unguarded path check followed by a
later open is insufficient. Machine must also prove that the running process
selected those exact executable and code inputs; changed identity or late
unreviewed load stops the run. The current Souls reader's runner-owned package
and writable `Contents/host` layout must be changed before positive launch.

Both measurements, snapshot identity and exact installed-plan digest must
match through the Machine-signed one-use pre-Hello reservation, authenticated
post-Hello finalization, immutable completed-run record and signed host
report. Machine independently observes the HQ-started runner, separate bridge,
peer accounts, confinement profile and HQ-hosted comms bind. HQ keeps admitted
runtime IDs provisional and unusable until it verifies the distinct Machine
finalization against the actual Hello and complete runtime set. A failed or
uncertain step refuses and contains. T01–T03 run under the observed protected
profile; T21 replays the same frozen measured Soul and qualified one-use runner
under a separately declared cooperative profile, and every receipt names that
profile. A `started` claim, HQ receipt, finalization or stop-containment record
is not a completed physical test and cannot authorize host-report signing.

Refusal tests must cover missing, extra, reordered or changed `primitives/` or
`opt/` entries; writable checker execution; changed bytes, path, mode or
launch inputs; links, special files, aliases, writable ancestry and limits;
snapshot mutation or inode swap before exec; self-claimed revision without an
accepted measurement mapping; unlisted module, provider or host projection;
replay on restart or another installation, host or HQ epoch; and any attempt
to substitute a started/finalized/stopped run for the completed physical
T01–T03/T21 evidence. The one-use start remains spent on ambiguous failure.
The exact byte schema and negative fixtures belong in `soul-contracts`, and
Machine, Souls, HQ and independent conformance must implement this rule before
any protected claim.

## Offline verification and local approval

Machine ships with an initial signed policy covering trust and revocation. HQ
may deliver a newer signed revision. Machine verifies it locally, rejects a
rollback to an older revision and enforces expiry. Only the owner authorizes
changes to trusted identities. HQ can withhold an update. It cannot extend
expiry, add a signer or override a revocation. Machine needs no internet access.

The initial owner-signed policy and owner public root must ship together in a
reviewed Machine release. Policy updates must preserve the greatest accepted
revision across restart. The signed policy pins the release workflow identity,
source and trust root and the designated physical host keys. Offline release
verification also requires an authenticated signing-time proof; a claimed
workflow name or a certificate without a verified trust chain is insufficient.

Refuse a protected launch when qualification has expired, revocation information
is stale, the evidence or signer is unknown or revoked, the installed inputs
have changed, or the required Machine pairing is unavailable. Cooperative
execution requires an explicit choice. The operator still approves each exact
local launch-rule installation.

## Revocation-information freshness

The owner selected a maximum age of one hour (3,600 seconds) for revocation
information in the Stage 2a working session on 2026-11-21. The owner-signed
policy binds the timestamp of the revocation snapshot to its exact set.
At every protected launch, Machine rejects a missing or future-dated snapshot
and refuses when its age exceeds 3,600 seconds. A snapshot exactly 3,600
seconds old is still current. This check is independent of policy expiry and
qualification expiry. Reissuing a policy without a newly authenticated
revocation snapshot does not refresh the snapshot timestamp. HQ cannot reset
that timestamp, increase the limit or override a revocation. Machine checks
freshness offline.

This value does not qualify an adapter or installation. The owner-signed
policy, authenticated reports, release attestation, measured installed inputs
and protected-host results remain separate prerequisites.
