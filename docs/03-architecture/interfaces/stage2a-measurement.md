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
The owner accepted the A-owned successor in PDR-0121. It takes effect only
when matching contract and implementations are released. Until then the
current root-owned staging and snapshot rule below remains the protected
qualification gate. The owner rejected a root helper; the current nonroot
Machine draft cannot satisfy that gate by adding one.


The owner approved this qualification-only rule on 2026-11-21 for one exact
`hello.soul` suite plan on the designated Mac. The plan names candidate,
suite, template, installation, inventory and expected measurements. Changed
inputs require a new plan and approval. Each actual start, including T21 or
a restart, spends a distinct Machine reservation; profiles cannot replay
one another. This grants no ordinary HQ work or Stage 3 import authority.

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

Until PDR-0121 is accepted, Machine separately measures the root-owned host projection (including exact
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

## Accepted Machine-admin custody pending release

Under PDR-0121, A owns frozen snapshots, spent claims, host projection and
enumerated runtime inputs. During the reviewed install, root may copy only
into fresh private staging nodes transferred with pinned identities to A.
A's fixed child, under A's effective UID with direct network denied,
reopens no-follow descriptors, remeasures the full approved inventory,
exclusively renames, seals read-only, syncs and rechecks final bytes and
identity. Root observes the final tree before installing the rule and
policy; it cannot publish it. An uncertain seal refuses. The plan pins A
distinct from HQ, R, B and C; missing protected accounts refuse. OS images
retain OS custody and build/signing pins. Only R reads its frozen inputs;
HQ, R, B, C and siblings cannot write. A and root remain trusted, so changes
require fresh approval. Machine authorizes one-use starts; HQ invokes fixed
R/B launchers, which recheck bytes before exec. Machine observes the child
and selected code closure before finalization. R/B transition remains an
unproven gate; no new root helper is authorized.

PDR-0091 forbids direct network from secure-admin/root processes. Installed
confinement must deny IPv4, IPv6 and DNS/provider traffic, allowing only
reviewed local IPC. HQ carries network exchange; current Machine admin
download providers migrate or refuse. No root snapshot/claim helper is installed.

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

