---
Status: Frozen
Doc-Type: paper
Owner: product-owner
Last-Reviewed: 2026-11-05
---

# Soul Agent System Architecture

> Converted from `Soul Agent System Architecture.docx` with scripts/docx2md.py — best-effort; curate before treating as normative.



Oct 25, 2026 · True Line AI

*Architecture draft 0.2. Proposed design, not a description of shipped software. Package paths follow the layout in Native Shareable Soul Packages draft 0.3.*

We propose a system in which persistent agents, called Souls, run on any machine, cooperate across machines, and present themselves to their user as a single agent. Each machine has one headquarters daemon (HQ) that equips, briefs and supervises its Souls. Each Soul is a self-contained, vendor-neutral meta-harness: a lead harness acts as its brain and orchestrates other harnesses as specialised regions, while the user chooses which software fills each role. Souls take notes during the day and consolidate them in sleep, improving the primitives their harnesses rely on. Messages and presence federate from machine to site to cloud over one wire; control never leaves the machine.

This paper is the system-level companion to three others:

| Paper | Status | Owns |
| --- | --- | --- |
| Native Shareable Soul Packages | Draft 0.3 | Package layout, data classes, portability, transfer profiles, export and sharing |
| Agent Identity and Delegated Authority | Draft 0.1 | Identity, grants, attribution, receipts |
| Agent Communications and Trustworthy Coordination | Outline 0.2 | Wire, delivery, tasks, participation, federation |
| Soul Agent System Architecture (this paper) | Draft 0.2 | How the parts fit: tiers, components, HQ, the Soul runtime, memory, packaging, invariants, implementation path |

Where this paper states a default, the companion paper that owns the topic is authoritative once it specifies otherwise.

## 1 The network

A user attaches to one node and reaches every agent through it. The same pattern repeats at every tier: a node accepts downstream connections and keeps one outbound uplink.

agent network · five tiers, two planes

**Two planes, split on purpose.** The messaging plane (messages, tasks, presence) federates from the Soul up to the cloud over one wire (tiers 4 to 1), while internal brain regions run as ACP sessions under the Soul's entry point (tier 5). The control plane (start, stop, admit, equip) exists only between HQ and the Souls on its own machine. No upstream tier can start, stop or execute anything locally; it can only deliver messages. When an inbound message is eligible to wake an idle Soul, HQ's local broker verifies the sender's wake grant and the Soul's wake budget, then asks local HQ to start or wake the Soul over hq/v1. A cloud or site outage therefore degrades reach, never local operation.

**Addressing.** Messages address a Soul ID, which is independent of its machine, harness or key. Presence propagates up the tree so each tier knows which downlink reaches a Soul. In the first profile a Soul has one active installation; HQ fences older installations with an installation epoch when a Soul moves.

**Uplinks are optional.** Every tier works without its upstream. Messages for unreachable destinations queue and deliver when the uplink returns.

## 2 Components and repositories

Four components, each with one job. Three map to existing repositories; GeniusBar is the front end.

| Component | Repository | Role | Runs |
| --- | --- | --- | --- |
| HQ | managed-machine (daemon) | The machine's headquarters: installs apps, owns credentials and keys, admits and supervises Souls, issues directives, answers queries, brokers inference, hosts the machine broker | One per machine, outside every Soul's trust domain |
| Entry point | agent-bot-identity (the agent-bot CLI, pinned per Soul) | The Soul's front door and supervisor: terminal chat, ACP server, keeps the brain alive, runs brain recovery; also the toolset the Soul acts through | One per Soul (agent-bot soul run), inside the Soul |
| Nervous system | agent-comms (client per Soul, broker at HQ and hubs) | Carries messages, tasks and orders; enforces send budgets and participation presets; the Soul's only door to HQ and third-party services | Client inside each Soul; broker at HQ, site and cloud |
| Front end | GeniusBar | The owner's UI over HQ: role assignment, approvals, enrollment codes, review queue, status | Desktop app talking to HQ |

Inside a Soul, the **lead harness** is the brain: it thinks, plans and routes work. The entry point keeps it alive; agent-comms carries and checks what it decides; HQ's broker enforces grants. Software that decides is never the software that enforces.

Today the HQ role lives in agent-bot-identity's daemon (census, lifecycle, wake dispatch, approvals), and managed-machine is a provisioner only. Section 10 describes the migration.

## 3 HQ, the machine's headquarters

HQ is to a machine what headquarters is to a company: it hires and equips agents, gives orders, answers questions and keeps the keys. It is also the trusted supervisor and broker the identity paper requires, because enforcement must sit outside the trust domain that harnesses share.

3.1 Channels

| Channel | Direction | Transport | Purpose |
| --- | --- | --- | --- |
| Lifecycle | HQ to Soul entry point | Local control API (hq/v1) over a protected socket | Start, stop, pause, drain, sleep, move, fork, retire |
| Directives | HQ to Soul | Broker envelope, kind directive | Orders: a task offer carrying a standing grant |
| Queries | Soul to HQ | Broker envelope, kind query | "May I", "which binding", "I need a token", "ask the owner"; answers are decision records |

3.2 Clock-in

One flow over hq/v1 covers first start, the daily report-in and arrival on a new machine; once equipped, the Soul opens its broker session to receive its brief.

- **Hello.** The entry point presents Soul ID, definition revision, installation ID, prior installation epoch (on move) and supported contract versions over hq/v1.
- **Admit.** HQ checks enrollment, verifies any incoming life transfer (Soul paper §12), sets or advances the installation epoch, and admits one runtime per role. Any message or task commit carrying an older epoch fails closed at the broker.
- **Equip.** HQ returns opaque grant handles and credential references over hq/v1. Long-lived keys never leave HQ; HQ signs or mints on request.
- **Brief.** The Soul connects to HQ's broker with its admitted session and receives the day's directives in its mailbox.
- **Ready.** The Soul reports each role over hq/v1: harness, version, auth state, warm or cold.
- **Lease.** Heartbeats over hq/v1 renew a lease. A missed lease marks the Soul stale, not stopped.

Clock-out reverses it: drain, settle tasks, report, and sleep if a dream grant is due. On machine shutdown HQ grants a short nap so the day's notes are consolidated before reboot. On move, clock-out produces a life transfer: the definition plus selected durable life, including the Soul's comms state (section 7.2), so the receiving HQ can resume without replaying settled work.

3.3 Credentials, keys and inference

HQ owns machine orchestration, app installation and credentials, one layer above the agents. A Soul may hold as many GitHub Apps or other service identities as its owner needs; one App may serve several Souls, because HQ's broker keeps each Soul's scope and attribution separate. No harness ever holds an App private key.

**Inference is brokered.** Under the protected profile a model call is a brokered operation, as the Soul paper requires: the harness sends the request to HQ's broker over the local socket, the broker checks the destination provider against the active task's grant and data classification, attaches the provider credential and forwards the call. Provider keys never enter a harness's environment, and this check is the enforcement point for understudy destinations (section 5). Where a harness cannot be pointed at a proxy, the broker issues a short-lived token scoped to one provider and the receipt records the weaker route.

3.4 Standalone profile

A Soul must run on a machine without HQ. The entry point then runs the same three channels against a built-in stub: the OS supervisor (launchd, systemd, Windows task) handles lifecycle, there are no directives, queries are answered by a local policy file and owner prompts, credentials come from a local store, and harnesses call providers directly. Because harnesses and stub share one trust domain, every receipt records profile: standalone-unenforced.

## 4 The Soul as a meta-harness

A Soul is a harness of harnesses. To its user it is one harness; inside, a lead harness orchestrates the others as regions of one brain.

inside a Soul · front door, brain, regions, nervous system

**One harness to the user.** The entry point offers terminal chat (agent-bot soul chat bob, or an alias such as bob) and an ACP agent server over stdio, so any tool that can host a harness can host a Soul. What happens behind it is invisible; the user sees only outcomes, and the owner can open the audit trail.

**The lead is the brain.** It thinks, plans and routes work to regions over ACP sessions. No lead, no Soul: if the lead cannot run, the Soul is down and its mail queues (section 5).

**Regions are roles, and the user assigns them.** Each region is a harness with its own sessions and context, serving a role such as development, Microsoft products or review. Regions never message each other directly; they report back to the lead and write typed notes. The owner decides which harness, model and provider fills each role, including the lead and its understudies, in the Soul definition (SoulInfo.json) through GeniusBar. Evals advise; sleep may propose; neither applies a change.

**Deciding is not enforcing.** The lead decides; agent-comms checks budgets and task authority before anything leaves the Soul; HQ's broker enforces grants and holds keys. A prompt-injected lead can therefore do no more than the Soul's grants allow.

**The owner's turn wins.** When the user chats while the Soul works on an HQ directive, background work pauses at its next safe point.

## 5 Brain recovery

The body cannot live without the brain, so the entry point runs a recovery ladder whenever the lead stops. It first classifies the failure: a local crash starts at rung 1; a provider outage (timeouts, 5xx, provider status) skips to rung 3, because restarting cannot fix a remote outage.

- **Restart** the same lead with backoff (5 s, 30 s, 2 min, then every 10 min). Five crashes within an hour quarantines the Soul instead of looping.
- **Re-equip.** On a sign-in or credential failure, HQ refreshes the binding; if the owner is needed, it raises a decision in GeniusBar.
- **Understudy.** The entry point switches to the next understudy the owner picked, in the owner's order. An understudy can differ from the primary in provider route, in model under the same harness, or in harness. Before switching to an understudy on a different provider, the entry point checks that every active task's grant and data classification permit that destination; if not, it skips that understudy rather than spill restricted notes across providers. HQ's broker enforces the same check on every model call (section 3.3). Only a route change can carry the native session; the others resume from notes.
- **Coma.** With no understudy left, the Soul is marked down. The broker keeps queuing, senders receive "queued, Soul unavailable", and HQ notifies the owner.
- **Resume.** The returning lead reads the handoff notes and open tasks. Any external action with an unknown outcome is reconciled before work continues, so nothing runs twice.

**Evals advise; the owner decides.** Sleep trains understudies for the lead role and replays the day's lead decisions on each, recording a pass rate against the primary with the exact revision, harness, model, provider and date. A failing or stale result (older than 7 days) is shown as a warning; the owner's choice stands. Only a guardrail violation removes an understudy until the owner overrides it.

**Each provider is a data destination.** A new provider for an understudy needs the owner's approval per Soul. A locally hosted model avoids that and also works offline.

## 6 Memory and sleep

A Soul remembers the way a person does: it takes notes, sleeps on them, keeps what matters, and forgets the rest. Forgetting is a feature; it removes noise and lets experience generalize.

| Memory | Soul layer | Package location | Lifetime |
| --- | --- | --- | --- |
| Working | Context window of the current session | Harness session | One task |
| Short-term | Notes taken since the last sleep | tmp/notes/ | Until the next sleep |
| Long-term | Knowledge records (assertions with sources) and their embeddings | memorial/knowledge/, indexes in cache/retrieval/ | Until evicted or corrected |
| Cache (habits) | Primitives: skills, scripts, tool guidance, hooks | primitives/ | Until unused or invalidated |

6.1 Notes

Members write typed notes on purpose (decision, finding, commitment, open question, handoff), each with member, time, task, sources and source classification (owner, hq, peer, external-untrusted). Notes are written at task boundaries and at clock-out; a handoff note is mandatory before the lead yields. Harnesses keep their own native transcripts; the Soul does not copy them. Notes are memory, not evidence: truth comes from receipts written by the enforcing services.

Notes live in the Soul's tmp/notes/ (backed by tmpfs where available, and carrying the protection class of the session that wrote them), never the host's shared /tmp or OS-reaped temp folders, with in-memory write-behind batching so constant edits cost few disk writes. Handoff notes and open-task state are the exception and flush immediately to the Soul's durable comms state (section 7.2), because recovery must survive a reboot. Whether ordinary notes should instead be durable dream inputs is open (section 11).

6.2 Sleep

Sleep is an admitted workflow under a dream grant, scheduled by HQ when the Soul is idle. Each run has a durable record under dreams/runs/<run-id>/ (plan, proposals, evals, checkpoints); intermediates go to tmp/dreams/<run-id>/. It reviews the notes since the last sleep and does what human sleep does:

- **Consolidate** short-term notes into long-term knowledge in memorial/.
- **Promote** what is recalled repeatedly into a primitive, so tomorrow's harnesses start better.
- **Evict** primitives unused since the last sleep back to long-term memory.
- **Invalidate** and re-derive a primitive when its evidence changes.
- **Rehearse** understudies and backup routes on a curated eval set (about 50 tasks per role, stored in ATIF).

Because one set of primitives renders into every harness's configuration, one improvement lifts every region. Sleep tunes two levels: each region for its role, and the meta level (which role takes which work, how context passes between regions).

**Provenance travels with memory.** Every note inherits the trust classification of the sources read in the turn that produced it. Sleep consolidates external-untrusted or peer notes only as attributed claims, never as first-party facts, and no primitive may be promoted from untrusted sources without the owner approving the source chain.

**Sleep never accepts its own output.** Its output is a candidate definition revision under the same Soul ID. Primitives, instructions, helpers and policy are control-plane changes, and no automatic acceptance policy covers the control plane: the owner, or a delegate whose authority is established outside the proposing run, accepts each candidate (section 11). The previous revision stays pinned for rollback. The dream scheduler, journal and checkpoints already exist in agent-bot-identity; propose, probe and compose loops follow Harness².

6.3 Embeddings

Embeddings are long-term storage, lossy by design. The embedding model is pinned in SoulLock.json and the indexing recipe lives in memorial/retrieval/; every index in cache/retrieval/ records the model that built it, and sleep rebuilds the index from knowledge records when the model changes. Embeddings inherit the source restrictions and trust classification of what they embed.

## 7 Packaging and isolation

7.1 The Soul owns everything it runs on

Copy a Soul to a brand-new machine and it runs with nothing installed. Runtimes, harness binaries, the pinned agent-bot entry point, the agent-comms client, small tools such as jq and yq, local models and nested Souls are installed under opt/ (harnesses, runtimes, packages, models) and pinned by SHA-256 in SoulLock.json, replacing today's per-Soul .soul-state/runtimes. Size is the accepted cost.

The Soul paper classes opt/ as reconstructible from accepted declarations and offers offline artifacts as an export option. This system makes that option the default for life transfer and backup, so the destination needs nothing installed; templates and shared definitions carry pins only.

Two exceptions, both declared rather than assumed:

| Exception | Examples | Treatment |
| --- | --- | --- |
| OS baseline | Shell, coreutils | Assumed present |
| Host toolchains | Xcode, platform SDKs | Declared in SoulInfo.json as host requirements (for example xcode >= 16), checked at activation, reported if missing, never vendored |

Credentials never travel in the package; a new machine needs a first-run enrollment or sign-in, not an install.

7.2 Content-addressed layout and transfer

The Soul manifest lists every file, runtime and nested Soul by SHA-256 inside a plain, inspectable .soul directory, using the Soul paper's Contents/ layout. export materializes a fully self-contained archive. The same layout later allows shared base layers across Souls, store distribution and delta upgrades without changing the contract. Souls on one machine may share identical files through a content-addressed store (hardlinks or APFS clones), invisible to the Souls. An OCI image layout is a possible export format once distribution through registries is needed. Platform binaries differ, so the owner declares target platforms per Soul and the package carries binaries for each.

**Definition vs. life on move.** A .soul package carries the accepted definition revision. Moving an active Soul is a life transfer (Soul paper §12): the definition plus selected durable life (memorial/, dreams/, home/, workspaces and comms state) with offline artifacts, verified by the receiving HQ at Admit. cache/ is rebuilt, host/ is recreated and tmp/ is dropped. Sharing a Soul exports a template: definition only, new Soul ID.

**Comms state needs a home.** Mailbox deduplication watermarks, task leases, open tasks and durable handoff notes have no place in the v0.3 layout. This paper proposes a durable-life comms/ area, owned by agent-comms, for the Soul paper to adopt.

7.3 Nested Souls

A Soul can fill a role in another Soul. It is vendored into the parent and pinned by the SHA of its definition revision, like any runtime, and runs as a member of the parent: the parent's identity, grants and memory, with the embedded definition's provenance recorded. Upgrading it means bumping the SHA. Cycles and nesting depth are checked when the package is built. Calling a live Soul elsewhere is different: that is cross-Soul collaboration over comms, where each keeps its own identity.

7.4 The Soul is its own root

The Soul is root-relocatable: every path is relative to its root, and the entry point sets HOME (the Soul's home/), XDG_*, PATH and tmp/ inside it; host/ holds PIDs, sockets and leases and is recreated on each host. The only exits are those HQ grants: the broker socket, mounted workspace views and a network allowlist. Isolation stays lightweight, with no full containers, so global toolchains remain usable:

| Platform | Isolation profile |
| --- | --- |
| macOS | Dedicated user account per Soul plus a sandbox profile |
| Linux | bubblewrap namespaces, host /usr and /opt read-only |
| Windows | Dedicated account plus AppContainer |

Each profile states what it does and does not enforce, and receipts name the profile in use.

## 8 Communication, identity and federation

These topics belong to the companion papers. This section records the defaults the system builds on until those papers specify otherwise.

| Topic | Default | Owner | Builds on |
| --- | --- | --- | --- |
| Wire | NDJSON on every tier, canonical JSON for signed parts, outer routing frame plus endpoint-sealed inner envelope, version N and N-1 at every hop, unknown required fields fail closed | Comms | agent-comms lib/wire.mjs (v: 1) |
| Delivery | At-least-once, deduplicated by message ID; causal ordering per conversation (per task when one exists); poison-pill quarantine after N failed wakes | Comms | ADR-0004 durable mailbox |
| Task authority | The lead decides; agent-comms commits after grant and budget checks; other members only propose; commitments carry bounded leases | Comms and identity | docs/tasks.md |
| Participation | Default preset quiet; one Soul-level send budget across all harnesses | Comms and identity | New |
| Site and cloud hubs | The same broker binary in relay mode; outbound uplinks; relays inspect outer routing frames only | Comms | ADR-0028 federation |
| Enrollment | Per-node Ed25519 key plus a one-time code the owner confirms in GeniusBar; pluggable authenticator for OAuth, Kerberos and tunnels later | Comms | ADR-0028 |
| Identity | Stable Soul ID; members, installations, runtimes and sessions identified separately; definition revisions separate from authority | Identity | docs/identity-contract.md, ADR-0815 |
| Grants | Opaque, caller-bound handles held by HQ's broker; verified at send time and consume/wake time; standing grants for routine work; human confirmation only where policy requires | Identity | delegation-grants.mjs, keyd |
| Inference | Brokered by HQ under the protected profile; destination checked against grant and data classification; provider keys never in the harness environment | Identity and packages | Soul paper protected profile |
| Receipts | Every consequential action has a receipt from the enforcing service, naming the enforcement profile | Identity | ADR-0077 owner decisions |
| External services | One egress point per Soul through agent-comms (A2A, MCP, chat platforms) with destination and taint-clearance policy | Comms | ADR-0005 A2A at the broker edge |

## 9 Invariants

Every change in the four repositories is checked against these. Breaking one requires a recorded decision.

- **One wire, every tier.** Machine, site and cloud speak the same versioned protocol; tiers differ by configuration, not code path.
- **Control stays on the machine.** Upstream tiers route messages and presence only; nothing upstream can start, stop or execute locally.
- **The Soul is the addressable unit.** Harnesses and models are private to the Soul; outside it there is one ID and one inbox.
- **Uplinks are optional.** Each tier works without its upstream; messages queue.
- **Contracts before code.** Cross-tier changes start as versioned contract changes; N and N-1 are supported.
- **Vendor-neutral.** No contract names a model, provider or harness vendor; vendor names appear only in configuration and eval records.
- **The user assigns roles.** The owner picks what fills each role, including the lead and its understudies. Evals advise; only a guardrail violation blocks.
- **A Soul looks like one harness to its user.** Terminal chat and ACP in front; everything behind is invisible.
- **A Soul owns everything it runs on.** Vendored and pinned by SHA, except the OS baseline and declared host toolchains; life transfers carry offline artifacts by default.
- **Deciding is not enforcing.** Software that decides (the lead, any harness) never holds keys or enforces grants; HQ's broker does.
- **Provenance travels with memory and messages.** Untrusted external inputs carry taint across notes, sleep consolidation and egress checks; sleep never launders untrusted claims into first-party policy or primitives.

## 10 Implementation path

The system is reached by migration, not rewrite: today's agent-bot daemon keeps working at every step while its parts move to their target homes.

| Phase | What happens | Done when |
| --- | --- | --- |
| 1 Shared vocabulary | One glossary for Soul, member, installation, runtime, session, definition revision, installation epoch; golden fixtures and negative vectors shared by agent-bot-identity and agent-comms | Papers, code and tests use the same terms and fixtures |
| 2 Composite Soul | Census records members per Soul instead of one harnessAuth; source-classified typed notes in tmp/notes/ and durable handoff notes in comms/; candidate-only sleep revisions | Two harnesses in one Soul appear as two members with notes; untrusted notes cannot self-promote in sleep |
| 3 Admission and grants | Clock-in (hello, admit, equip) over today's daemon API; installation epoch fencing; caller-bound grant handles with a durable spent-nonce store and Soul-level send budgets | A copied handle or stale epoch is refused, also after restart; send budgets halt runaway turns |
| 4 Hostile-worker test | A member tries to read broker keys, reuse a handle, bypass taint rules, call a provider directly, or call the credential CLI directly | Every attempt is refused or reported as an unenforced profile |
| 5 Entry point | agent-bot soul run and soul chat; ACP server; brain recovery ladder with destination-checked understudies | A Soul survives a killed lead and a simulated provider outage without leaking restricted tasks across providers |
| 6 HQ in managed-machine | The managed-machine daemon supervises today's agent-bot daemon, then absorbs its HQ half (hq/v1) and the inference broker; GeniusBar talks to HQ | One launchd unit per machine; agent-bot daemon retired |
| 7 Self-contained package | Soul paper layout (opt/, memorial/, dreams/, host/), SHA manifest, host requirements, root-relocatable paths, life transfer with offline artifacts on move, isolation profiles | A Soul copied or moved to a clean machine runs with only enrollment |
| 8 Federation | Site hub in relay mode, then cloud, per ADR-0028 | Two LANs exchange messages through a relay; a cut uplink only queues |

Phases 1 to 4 follow section 15 of the identity paper. Nothing in this path is authorized for implementation until the owner approves it.

## 11 Risks and open decisions

Each risk has a default the design proceeds on and the vision input that would change it.

| Risk | Default | Changes if |
| --- | --- | --- |
| Open: notes on tmpfs conflict with the Soul paper keeping dream inputs durable | Notes in tmp/notes/ on tmpfs; handoff and open tasks durable in comms/; HQ grants a nap on shutdown; a hard crash is ordinary forgetting | Notes prove too valuable to lose. Recommended: write them to dreams/inputs/ with the same write-behind batching and delete each once sleep consumes it |
| Open: sleep promoting primitives is a control-plane change, and no automatic acceptance covers it | Recommended: HQ accepts as a bounded delegate within limits the owner sets in GeniusBar (revertible primitives from first-party sources only); everything else queues for the owner in GeniusBar | The owner wants to review every primitive change, or wants a broader delegate |
| Comms state has no home in the v0.3 package layout | Proposed durable-life comms/ area owned by agent-comms | The Soul paper places it elsewhere |
| Brokered inference adds a hop on every model call and a harness may not accept a proxy | Local-socket proxy; short-lived per-provider token where a proxy is impossible, recorded as a weaker route | Latency or a harness forces a different enforcement point |
| ENG-0339 gives each harness its own OS account; a Soul needs its harnesses in one trust domain | One OS account per Soul; HQ in its own account. Needs an amendment in qwts-agent-sop | Harnesses inside one Soul must be isolated from each other |
| HQ holds every Soul's keys | Acceptable with one owner per machine | Machines host Souls for several owners: one key store per owner |
| Cloud mesh operator | Self-hosted relay first; no spending (ADR-0028) | It becomes a hosted service: accounts, billing and privacy policy move up |
| Standalone Souls are unenforced | A developer fallback, clearly labelled | Store customers mostly run without HQ: standalone needs real enforcement |
| A lead provider outage takes the Soul offline | Accepted unless the owner picks understudies | Some Souls need uptime guarantees |
| macOS-native tools cannot be fully isolated | Account plus sandbox profile, labelled in receipts | A stronger boundary is required for such Souls |
| Vendored harness binaries may not be redistributable | Life transfers and backups carry offline artifacts; templates carry pins only | Vendors permit redistribution |
| Two daemons coexist during migration | agent-bot keeps its unit until HQ takes over supervision | GeniusBar release timing forces an earlier cutover |

**Not yet specified:** the HQ contract's exact message schemas; participation preset limits (starting values in the comms outline); note schema; the comms/ area's record format; the eval-set format beyond ATIF; the true-line agent-watcher model for HQ directives and queries, which this draft has not reviewed.

## References

- True Line AI. *Native Shareable Soul Packages*, draft 0.3, 2026-10-20. Zenodo 10.5281/zenodo.23547566
- True Line AI. *Agent Identity and Delegated Authority*, draft 0.1, 2026-10-20.
- *Agent Communications and Trustworthy Coordination*, outline 0.2, 2026-10-25. Outline
- Agent Bot north star (working notes for this paper). North star
- qwts/agent-bot-identity: docs/soul-package.md, docs/identity-contract.md, docs/soul-skill-dream-design.md, ADR-0815.
- qwts/agent-comms: ADR-0002 to ADR-0008, ADR-0028, ADR-0059, ADR-0077; docs/tasks.md; docs/federation-*.md.
- qwts/managed-machine and qwts/managed-machine-config (provisioning, fleet, catalog).
- Google Research. Harness²: recursive agent harnessing.
- Harbor. Agent Trajectory Interchange Format (ATIF) v1.7.
- OpenTelemetry. GenAI semantic conventions.
