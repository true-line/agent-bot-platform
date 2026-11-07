---
Status: Frozen
Doc-Type: paper
Owner: product-owner
Last-Reviewed: 2026-11-05
---

# Agent Bot North Star

> Converted from `Agent Bot north star.docx` with scripts/docx2md.py — best-effort; curate before treating as normative.



Oct 24, 2026 · True Line AI

## Vision

One network of agents in five tiers: you attach to one cloud node and reach every agent through it. The same pattern repeats at each tier, and the Soul is the smallest unit the network addresses.

agent network · five tiers, two planes

Messaging and presence run from the Soul up to the cloud. Supervision runs only from the machine manager down to harnesses.

## Existing foundations

Much of this is already specified or built. New work extends these instead of replacing them.

| Piece of the vision | Where it already lives | State |
| --- | --- | --- |
| Soul as a portable meta-harness | Native Shareable Soul Packages v0.3 (True Line AI, 2026-10-20); agent-bot-identity docs/soul-package.md | Paper: proposed requirements. .soul format 1/2: implemented. |
| Sleep / dream maintenance | agent-bot-identity docs/soul-skill-dream-design.md (#603, #887, #903) | Scheduler, journal, conversation and memory inputs, checkpoints: implemented. Owner-gated; coverage unverified. Knowledge search: #902. |
| Site and cloud hubs, federation | agent-comms ADR-0028, docs/federation-contract-proposal.md and federation-* docs | Policy accepted 2026-10-11. No runtime authorized yet; crypto and provider review pending. |
| Remote tiers have no control authority | Same federation contract: a remote soul gets no launch, cold-wake, owner or credential authority | Accepted policy; matches invariant 2. |
| Node enrollment | Same federation contract: per-relay key, pinned peers, owner-verified out-of-band challenge | Accepted policy; matches direction 5. |

## Alignment with the Soul paper (v0.3 overview)

| Paper says | Consequence for this architecture |
| --- | --- |
| Stable Soul ID, separate definition revision | Sleep and upgrades produce new definition revisions; the Soul ID and its address never change. Pinning (D3, D4) pins a definition revision. |
| Credentials stay in external stores; the package carries references | HQ owns the stores (direction 4). Standalone mode uses a local store behind the same reference format. |
| Access is enforced by the host, because harness and agent shell share a trust domain | HQ is the enforcement point. In standalone mode the Soul brain must run as a separate trust domain from its harnesses, or the Soul runs unenforced and says so. |
| Life transfer: new host validates, restores, rebuilds indexes, reconnects credentials, reports gaps | That is the clock-in flow on a new machine. One flow covers first start, daily report-in and migration. |
| No promise of synchronized writers or globally exclusive execution | First profile: one active installation per Soul, fenced by an installation epoch at HQ's broker. Presence carries the installation ID. Intentional replicas are a later profile. |
| Template = new Soul ID; fork = new ID with parent provenance | Both are HQ lifecycle operations alongside start, stop and move. |

## Alignment with the identity paper (Agent Identity and Delegated Authority, draft 0.1)

| Paper says | Consequence for this architecture |
| --- | --- |
| A trusted supervisor admits runtimes; a broker mediates protected operations, outside the agent shell's trust domain | That pair is HQ. agent-comms inside the Soul routes and coordinates (D4) but never holds keys or enforces grants. |
| Harnesses are internal members with Soul-qualified IDs; runtimes get fresh credentials on replacement | Brain regions = members. Census records Soul, member, installation, runtime and session separately. |
| A shared GitHub App can serve several Souls if the broker keeps scope and attribution separate | Direction 3 stands: as many Apps as the owner needs, all held by HQ's broker, never by a harness. |
| Standing policies let an owner authorize a class of work once | HQ directives are standing grants; human confirmation only when policy requires it. |
| Dreams are admitted workflows with no administrative authority | Sleep runs under a dream grant; accepting instruction changes needs a separate grant (matches the Sleep section). |
| Participation presets (quiet, chatty, goal oriented) enforced by the comms service across all harnesses | agent-comms owns one Soul-level send budget; four harnesses never get four allowances. |
| Unenforceable profiles must be refused or reported, never silently downgraded | Standalone mode is a declared, weaker profile. It works, and its receipts say so. |
| Suggested path: glossary + fixtures for Soul, member, installation, runtime, session; then multi-harness admission with caller-bound grants and a hostile-worker test | This is the natural first build increment for the manager split. |

## Invariants

Every PR in the four repos is checked against these. A change that breaks one needs an explicit decision recorded below.

- **One wire, every tier.** Machine, site and cloud nodes speak the same versioned comms protocol. Tiers differ by config, not code path.
- **Control plane stays on the box.** Upstream tiers route messages and presence only. Nothing upstream can start, stop or exec locally.
- **The Soul is the addressable unit.** Harnesses and models are private to the Soul. Outside it: one Agent ID, one inbox.
- **Uplinks are optional.** Each tier keeps working when its upstream is gone; messages queue store-and-forward.
- **Contracts before code.** Cross-tier changes start as a versioned contract change; each side supports N and N-1.
- **Vendor-neutral.** No contract names a model, provider or harness vendor. Any (harness, model, provider) combination may fill any role if it passes that role's evals and its provider is an approved data destination for the Soul. Vendor names appear only in configuration and eval records.
- **The user assigns roles.** The owner picks which harness, model and provider fills each role in each Soul, including the lead and its understudies, in soul.json through GeniusBar. Evals inform the choice and sleep may propose changes, but neither applies one. A failing eval shows as a warning; only a guardrail violation blocks an assignment.
- **A Soul looks like one harness to its user.** The entry point is also the Soul's front door: an interactive terminal chat (agent-bot soul chat, or a per-Soul alias like bob) and an ACP agent server over stdio, so any ACP client (editors, other tools) can drive the Soul exactly like a harness. Behind it, the lead orchestrates the rest. The owner's interactive turn preempts background work, which pauses at its next safe point.
- **A Soul owns everything it runs on.** Runtimes, harness binaries, agent-identity, the agent-comms client and nested Souls are vendored and pinned by SHA (extending today's .soul-state/runtimes). Size is an accepted cost. Copy the package to a brand-new machine and it runs with nothing installed. The only exception is the OS baseline (shell, coreutils); small tools like jq and yq are vendored too, because their versions differ between machines. Several Souls on one machine may share identical files through a content-addressed store (hardlinks or APFS clones), invisible to the Souls.

**Content-addressed package (keeps sharing open).** The Soul manifest lists every file, runtime and nested Soul by SHA-256. export materializes a fully self-contained archive today. Later, without changing the contract: shared base layers across Souls, shared or store-distributed Souls, and delta upgrades that fetch only changed SHAs. On disk it stays a plain, inspectable .soul directory with a SHA manifest; an OCI image layout is a possible export format later (registries, signing, mirroring).

**The Soul is its own root (owner: "you could chroot a Soul package").** Lay the Soul out so it can become a jail: every path relative to the Soul root, and the entry point sets HOME, XDG_*, PATH and temp dirs inside the Soul. Then the only ways out are the ones we grant: HQ's broker socket, workspace views HQ mounts in, and a network allowlist. That is the identity paper's "complete mediation" made physical.

| Platform | Isolation profile (no full containers) | Host tools stay visible |
| --- | --- | --- |
| Linux | bubblewrap namespaces around the Soul root | Host /usr, /opt bound read-only |
| macOS | Dedicated user account per Soul plus a sandbox profile | Xcode, SDKs and other global tools usable as installed |
| Windows | Dedicated account plus AppContainer | Global toolchains usable as installed |

**Host toolchains stay global (owner).** Full containers are out: platform toolchains like Xcode and OS SDKs must stay global. They are a second, declared exception to invariant 9: large, licensed, OS-integrated tools are listed in soul.json as host requirements (for example xcode >= 16), checked at activation, and reported as missing instead of vendored. Everything else stays inside the Soul.

**Souls inside Souls: vendored, pinned by SHA (owner).** A Soul used as a harness is copied into the parent and lives there like any other runtime, pinned by the content digest of its definition revision (alongside .soul-state/runtimes). It runs as a member of the parent: Bob's identity, Bob's grants, Bob's memory, with the embedded definition's publisher provenance recorded. Upgrading it means bumping the SHA, which sleep may propose and the owner approves. Guards: cycles and nesting depth are checked when the package is built (a dependency graph of SHAs), and budgets are shared, never multiplied. Calling a live Soul elsewhere is a different thing: that is cross-Soul collaboration over comms, where each keeps its own identity.

## Decisions and working assumptions

Confirmed decisions are fixed until revisited. Working assumptions are reversible defaults we build on until evidence changes them.

| ID | Kind | Statement | Why | What would change it |
| --- | --- | --- | --- | --- |
| D1 | Confirmed (owner, 2026-10-24) | Split planes: messaging and presence federate upward; supervision stays machine-local. | Each plane can be developed and tested on its own; a cloud outage cannot stop local agents. | Nothing planned. |
| D2 | Confirmed (owner, 2026-10-24) | The manager is the managed-machine daemon. It is also GeniusBar's backend entry point; GeniusBar is a front end only. | One daemon per box owns the machine; one place for the UI to talk to. | Nothing planned. Replaces working assumption A1. |
| D3 | Confirmed (owner, 2026-10-24) | agent-identity (today agent-bot) is the CLI inside each Soul: the toolset the agent uses for every task it performs. | Capabilities pinned per Soul; upgrade one Soul without touching others. | Nothing planned. |
| D4 | Confirmed (owner, 2026-10-24) | A lead harness is the Soul's brain and orchestrates the other harnesses (lead role configurable; no lead means the Soul is down, its mailbox keeps queuing). agent-comms is its nervous system: it carries and enforces that orchestration, and it is the Soul's single point of contact with the manager and third-party services. | One runtime presents one agent outward; one egress point to audit. | Nothing planned. |
| A2 | Working assumption | Tiers 1 to 3 run the agent-comms broker in local, site or cloud mode, with outbound uplinks. In-Soul orchestration is a separate module of the same package. | One codebase for every hub; NAT-friendly; matches invariant 1. | Broker cannot scale to cloud load, or cloud needs a different store. |
| A3 | Working assumption | Agents are addressed by agent_<uuid>; presence propagates up the tree to build routes. | A Soul can move machines without changing its address. | A need for human-readable or org-scoped names on top. |
| A4 | Working assumption | Migrate strangler-style: the managed-machine daemon first supervises today's agent-bot daemon, then absorbs its manager parts; the ACP engine and warm pool move into agent-comms. | Keeps a working system at every step. | None expected. |

Directions on the open questions (owner, 2026-10-24)

- **Control API: the manager is the machine's HQ.** It is not just a process supervisor. It gives orders to agents, and agents can probe it with questions (see true-line agent-watcher). The API needs three channels: lifecycle (start, stop, drain), directives (HQ to agent), and queries (agent to HQ).
- **Lifecycle: managed, or standalone.** The manager starts and stops Souls by triggering their daemons. A Soul must also run as an independent agent when no manager is installed, so every manager dependency needs a standalone fallback.
- **Orchestration and identity: harnesses are brain regions.** Each harness owns its own sessions and context and serves a configurable role, for example Claude Code for development and Copilot for Microsoft products. A Soul holds as many GitHub Apps as it needs (two today: qwts and true-line, unless the Apps go public), chosen per user.
- **State: the manager hires and equips agents.** It owns machine orchestration, app installation and credentials, one layer above the agent. Agents report in for the day (clock in) and receive their credentials and orders.
- **Trust across tiers: start simple, stay extensible.** Tunnels, OAuth and Kerberos all exist. Start with one simple scheme behind a pluggable authenticator interface so the others can be added later.

Sleep: self-improvement between shifts (proposal)

A Soul package is a **meta-harness**: a harness of harnesses. Each harness is a brain region with its own prompt, skills, tools and memory, and the Soul adds the layer above them: roles, routing, handoff and shared memory. Harness² improves harnesses with model weights fixed, so sleep can tune both levels. At the region level it tunes each harness's config for its role. At the meta level it tunes which role takes which work and how context passes between regions.

- **Clock out.** HQ schedules sleep when the Soul is idle and grants a sandboxed, network-restricted budget.
- **Review the day.** Read every harness session since the last sleep watermark: what failed, what was retried, where a harness worked around a missing tool.
- **Improve the primitives.** Propose edits to the shared primitives the harnesses rely on: skills, scripts, tool guidance, hooks, agent-identity CLI usage, memory. Probe candidates by replaying the day's tasks, then compose the winners (Harness² propose, probe, compose). soul build renders one set of primitives into every harness's config, so one fix lifts every region.
- **Wake as a candidate.** The result is a candidate definition revision under the same Soul ID, not an in-place edit. It is adopted only if it beats the old one on replay, and changes to instructions, helpers or policy need the owner or an independently authorized delegate (HQ can be that delegate). A candidate never approves its own rules. The old revision stays pinned for rollback, and the watermark advances.

Guardrails: sleep never edits credentials, identity bindings or its own guardrails without approval, and runs with no network beyond its model provider. Harness² is Python 3.12 with OpenCode/Codex executors, so it runs as a sleep-time tool the brain invokes, not as code inside the Soul runtime.

Brain recovery (proposal)

No lead, no Soul, so the Soul's entry point runs a recovery ladder whenever the lead harness stops. The entry point is the Soul's pinned agent-bot CLI in long-running mode (`agent-bot soul run`): it is the Soul's mini daemon. HQ (or launchd/systemd in standalone mode) supervises the entry point; the entry point supervises the harnesses. It holds no keys and enforces no grants; it only keeps the brain alive. Each rung is tried only after the one before it fails.

- **Restart.** The entry point restarts the same lead harness with backoff (5 s, 30 s, 2 min, then every 10 min). Five crashes within an hour quarantines the Soul instead of looping.
- **Re-equip.** On a sign-in or credential failure, HQ refreshes the binding. If it needs the owner, it raises an owner decision in GeniusBar.
- **Backup provider.** The same harness and model family on another provider route (for example, Claude through the Anthropic API, then Bedrock). Only routes the owner declared in soul.json, because a provider is a data destination.
- **Coma.** If all rungs fail, the Soul is marked down. The broker keeps queuing, senders get a "queued, Soul unavailable" receipt, and HQ notifies the owner.
- **Resume.** When the lead returns, it reads the Soul journal and open tasks. Any external action with an unresolved outcome is reconciled before work continues, so nothing runs twice.

The entry point classifies each failure first. A local harness crash goes to rung 1. A provider outage (timeouts, 5xx, provider status) skips rungs 1 and 2 and goes straight to rung 3, because restarting cannot fix a remote outage. Example: a Codex lead on OpenAI falls back to Azure OpenAI (same models), and a Claude lead falls back to Bedrock or Vertex.

**Backup routes are checked by evals, not assumed.** "Same model" on another provider can differ in version, limits and behaviour. During sleep, the Soul replays a sample of the day's tasks on each declared backup route and records the pass rate against the primary. HQ fails over only to routes the owner picked, in the owner's order; a route without a passing eval within 7 days for the current revision is used but flagged. The eval record names the exact revision, harness, model, provider and date, as the identity paper's evaluation identity section requires. Only a guardrail violation removes a route until the owner overrides it (invariant 7).

**Understudy brain.** A different harness can also back up the lead if it is trained for the role and meets the eval bar. Sleep renders the lead-role primitives for the understudy, replays the day's lead decisions on it, and tunes it like any other region. Default bar: at least 95% of the primary's pass rate on the replay suite, zero guardrail violations, fresh within 7 days for the current revision. The owner picks understudies and their order; eval results are advice, shown as warnings (invariant 7). It resumes from the Soul journal, never from the primary's native session. Rung 3 tries the same harness on a backup provider first, then a qualified understudy.

An understudy can differ from the primary on any of three axes, all under the same eval gate: provider route (Codex on OpenAI to Azure OpenAI), model under the same harness (Codex CLI with DeepSeek through an OpenAI-compatible endpoint), or harness (Codex to Claude Code). Only a route swap can carry the native session; the other two hand off through notes. Each new provider is a data destination and needs owner approval per Soul; a locally hosted model avoids that and also works offline.

Soul journal and memory (proposal)

Two layers: a structured journal is the source of truth, and embeddings are the recall layer derived from it.

| Layer | Format | Used by |
| --- | --- | --- |
| Live feed | ACP session/update (already consumed by the daemon) | Normalizer only |
| Journal | ATIF v1.7 for the curated eval set only; the journal itself is typed notes (see note-taking below) | Sleep replay, evals, understudy handoff, audit |
| Correlation | OTel GenAI trace and span IDs on every entry (agent-bot already exports OTLP) | Cross-tier tracing |
| Recall | Embedding index over the journal and knowledge, tagged with its embedding model | Lead and understudy context, memory retrieval |

Rules: the embedding model is pinned in soul.json; every index records the model that built it and is rebuilt in sleep when the model changes; embeddings inherit the source restrictions of what they embed and never leave the Soul's disclosure scope.

**Memory model (owner: short-term and long-term memory; primitives are the cache).**

| Memory | Soul layer | Lifetime |
| --- | --- | --- |
| Working | Context window of the current session | One task |
| Short-term | Notes changed since the last sleep | Days |
| Long-term | Knowledge records + embeddings | Until evicted or corrected |
| Cache (habits, "muscle memory") | Primitives: skills, scripts, tool guidance | Until unused or invalidated |

Sleep does what human sleep does: **consolidate** short-term into long-term, **promote** what is recalled repeatedly into the cache, **evict** unused primitives back to long-term, and **invalidate** a primitive when its evidence changes.

**The journal is note-taking, not recording (owner).** Members write notes on purpose, the way a person does, instead of the Soul storing full transcripts. Harnesses keep their own native transcripts; the Soul does not copy them.

- Note types: decision, finding, commitment, open question, handoff state. Each note carries member, time, task and source references.
- When: at task boundaries, before any handoff, and at clock-out. A handoff note is required before the lead yields, so an understudy can pick up from notes.
- Notes are self-reported, so they are memory, not evidence. Truth comes from receipts written by the enforcing services, and evals use the curated eval set (task inputs plus observed outcomes, stored in ATIF).
- Sleep reads the notes since the last sleep (short-term memory) and consolidates them into long-term memory.

**Note storage (owner: notes are short-term, not long-lived).** Notes live in a per-user private temp location and are deleted once sleep has consolidated them: $XDG_RUNTIME_DIR on Linux (RAM-backed, mode 0700) and $TMPDIR on macOS (per-user, private). Not the shared /tmp. Writes are write-behind: repeated updates coalesce in memory and flush at task boundaries or every 30 s. Exception: handoff notes and open-task state go to the Soul's persistent state directory, because brain recovery must survive a reboot. On shutdown, HQ asks the Soul for a short consolidation (a nap) so a reboot does not erase the day.

**Forgetting is a feature (owner).** Memory is lossy on purpose, like human memory: details fade and what matters generalizes. The Soul forgets like a person but keeps receipts like a professional.

| Kept | For how long (default) | Why |
| --- | --- | --- |
| Raw journal | Until the next sleep consolidates them, then deleted | Short-term scratch; what matters moves to long-term memory |
| Action receipts (consequential external effects) | Per the owner's retention policy | Accountability under the identity paper |
| Knowledge records (assertions with sources) | Until evicted or corrected | The source embeddings are rebuilt from when the embedding model changes |
| Curated eval set (about 50 tasks per role) | Refreshed each sleep | Backup-route and understudy qualification need replay material |
| Embeddings | Rebuilt from knowledge records | Storage, lossy by design |

First build increment (plan, not started)

Goal: prove one Soul with two harnesses runs under HQ admission and caller-bound grants, and that a hostile member cannot get around the broker. This follows section 15 of the identity paper. It needs the owner's go-ahead before any code.

| Step | Repo | Deliverable | Done when |
| --- | --- | --- | --- |
| 1. Glossary | agent-bot-identity (docs/identity-contract.md) | One shared definition of Soul, member, installation, runtime, session, definition revision, installation epoch | The three papers and the code use the same terms |
| 2. Fixtures | agent-bot-identity, agent-comms | Golden JSON records for each entity, plus negative vectors (wrong purpose, stale epoch, copied handle) | Both repos' tests load the same fixtures |
| 3. Census v2 | agent-bot-identity (agent-population.mjs) | Census records members and runtimes per Soul instead of one harnessAuth | Two harnesses in one Soul show up as two members |
| 4. Admission | agent-bot-identity daemon (HQ half) | Hello, admit and equip from section 9.2, over the existing loopback API | A Soul clocks in and gets one grant handle per member |
| 5. Caller-bound grants | agent-bot-identity (delegation-grants.mjs, keyd) | Handles bound to the admitted caller; durable spent-nonce store | A handle copied to another member is refused, also after restart |
| 6. Hostile-worker test | agent-bot-identity tests | A member that tries to read broker keys, reuse a handle, or call the credential CLI directly | Every attempt is refused or reported as an unenforced profile |

This stays inside the agent-bot daemon on purpose (A4, strangler path). The managed-machine daemon takes over supervision once steps 1 to 6 pass.

Watch list: what could hang us

Each item has a default we proceed on and the piece of vision that would change it.

| Risk | Default we proceed on | Vision input that would change it |
| --- | --- | --- |
| ENG-0339 gives each harness its own macOS account; a multi-harness Soul needs them in one trust domain | One OS account per Soul, harnesses share it, HQ in its own account. Needs an amendment in qwts-agent-sop (outside this project). | If harnesses inside a Soul must be isolated from each other, keep per-harness accounts and accept more brokered calls. |
| HQ holds every Soul's App keys, so one HQ compromise exposes all of them | Acceptable for one owner per machine | Machines shared by several owners need one key store per owner. |
| Who runs the cloud mesh | Self-hosted relay first, per ADR-0028; no spending | If it becomes a True Line hosted service, OAuth accounts, billing and a privacy policy move up the list. |
| Standalone mode is unenforced | Fine as a fallback for developers | If store customers will mostly run Souls without HQ, standalone becomes the main experience and needs real enforcement. |
| Two daemons coexist during the strangler migration | agent-bot daemon keeps its launchd label until HQ takes supervision | GeniusBar release timing could force an earlier cutover. |
