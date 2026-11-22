---
Status: Draft
Doc-Type: interface
Owner: product-owner
Last-Reviewed: 2026-11-21
Normative-Source: PDR-0102, PDR-0121
---

# Controlled Stage 2a Soul measurement

This exact byte and custody rule implements the
[qualification decision](../../04-decisions/PDR-0102-protected-adapter-qualification.md#controlled-stage-2a-soul-measurement)
as amended for frozen-copy custody by
[PDR-0121](../../04-decisions/PDR-0121-machine-admin-custody-for-stage-2a-snapshots.md).
The A-owned successor below takes effect only after PDR-0121 is accepted
and the matching contract and implementations are released. Until then the
current root-owned staging and snapshot rule stated below remains the
protected qualification gate. The owner has rejected a root helper, so the
current nonroot Machine draft cannot satisfy that gate by adding one.


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
under `opt/` (Reconstructible), including the `Contents/` directory record.
For the `hello.soul` template after `soul-conformance` PR #38 (merged at
`8e82f47781e583e4b09352cbfef5ca3bfefe45aa`), this is five files:
SoulInfo, SoulLock, `primitives/quickstart-task.json`,
`opt/quickstart-adapter.mjs`, and `opt/quickstart-check.mjs`, plus their
directory records. The measured inventory must exactly equal the
owner-approved inventory. Unknown top-level paths or extra files in the
frozen source refuse. No file may be omitted by a wildcard. This is an exact
installation and launch byte closure; it does not establish the semantic
validity or portability of a package.

Life (`workspaces/`, `home/`, `memorial/`, `dreams/`, `comms/`), Rebuilt
(`cache/`), Recreated (`host/`) and Dropped (`tmp/`) state lives in separate
runner-owned writable paths, outside the frozen source. It cannot supply
unreviewed executable, module, configuration, policy or checker bytes for the
qualified run. `soul-conformance` PR #38 moved the template checker from
writable `workspaces/scratch/check.mjs` to frozen
`opt/quickstart-check.mjs`. The selected invocation must use that measured
checker. `answer.txt` remains writable evidence; record the seeded
issue/answer and final answer as test input and outcome.

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

`launch_input_records` is one canonical object containing the sorted external
file-record array, exact host projection values, the selected command and full
ordered `execve` argument array including `argv[0]`, static environment and
configuration selections, macOS build and selected-image signing requirements,
sandbox-policy digest, and named Machine, HQ, Souls, B bridge, HQ-hosted comms
broker, adapter, harness and test-provider digests. A changed argument or
selected configuration changes the launch-input measurement even when every
file record is unchanged. Secret broker authority is not an environment value
in this object.

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
JCS(definition_records))`. The canonical `launch_input_records` object uses
the distinct prefix `agent-bot/stage2a-launch-inputs/v1` with the same NUL and
JCS rule. Owner, group, device, inode and timestamps are custody
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

## Current snapshot custody pending successor acceptance

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

## Proposed Machine-admin snapshot custody

Machine copies approved source and code through no-follow directory
descriptors into a private staging tree owned by its secure administrative
account A. The authenticated installation and exact owner-approved plan
pin A; neither HQ nor an incoming record selects it. A is distinct from HQ,
runner R, bridge B and credential account C. If the chosen host cannot
provide those protected-profile account distinctions, that profile refuses.
Machine verifies one-link regular files and protected ancestors, hashes the
bytes actually opened, syncs every staged file and directory, then atomically
publishes a read-only A-owned snapshot and syncs its parent. Only the
assigned R receives the read and traversal access needed for that start;
HQ, R, B, C and sibling installations have no write, rename, delete or ACL
grant on the snapshot, its ancestors or the A-owned one-use claim. A and root
remain trusted to manage those files. Machine launches only the snapshot,
retaining or reopening descriptors and comparing identities and hashes
immediately before exec. The sandbox denies runner writes to source and host
projection from the first instruction. An unguarded path check followed by
a later open is insufficient. Machine must also prove that the running
process selected those exact executable and code inputs; changed identity
or late unreviewed load stops the run. The current Souls reader's
runner-owned package and writable `Contents/host` layout must be changed
before positive launch.

Agent Bot processes executing with secure-admin or root privileges, across
profiles and paths, have no direct network access. The installed host
confinement must demonstrably deny direct IPv4, IPv6 and DNS/provider
traffic while allowing only reviewed local IPC. HQ carries network exchange
in its unprivileged account through authenticated, purpose-limited Machine
requests. Machine durably spends each exact one-use claim under A before
returning a reservation; failure, uncertainty or suspected rollback keeps
the start refused. No root helper is installed or invoked for snapshot or
claim mechanics at installation or runtime. The existing root-owned host
projection and installed executable source requirements remain separate
from the A-owned frozen copies.

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

