---
Status: Frozen
Doc-Type: paper
Owner: product-owner
Last-Reviewed: 2026-11-05
---

# Soul Agent Platform: Operator Questions (revised 2026-10-29)

> Converted from `Soul_Agent_Platform_Operator_Questions (revised 2026-10-29).docx` with scripts/docx2md.py — best-effort; curate before treating as normative.



Oct 24, 2026 · True Line AI

Companion to whitepaper draft 0.3. Each answer is tagged **Specified** (the draft states it; sections cited), **Partly specified**, or **Not specified** (a proposed answer for the author to confirm or reject). Command names are illustrative: the draft requires an HQ CLI (§3, §8) but names no verbs.

## Getting started

### What are the exact steps to install HQ, create or import a .soul, enroll it, and run the first task?

**Partly specified.** The draft gives the flow (§5 clock-in, §8 owner experience, §11 import validation, §13 Stage 3) but no command sequence. Proposed sequence:

- Install HQ (the managed-machine daemon) under the account that will own it. That account is the owner (§4); HQ creates its control socket, key store, and authority database.
- Create from a template or import: hq soul create <name> --template <path> or hq soul import <path>.soul. HQ validates the manifest, path traversal, platform, host requirements, and dependency cycles before activation (§11) and reports missing toolchains before any work (§8).
- Assign roles: hq soul roles <name> --lead <adapter> --specialist <adapter>. This writes SoulInfo.json as a new definition revision under an owner approval record (§8, §11).
- Approve destinations and standing grants: hq grant add <name> --resource ... --action ... --destination ... --expiry ... --ceiling ... (§8).
- Add credentials to HQ’s store: hq credential add <id>. They never enter the package (§11).
- Start: hq soul start <name>. The entry point runs Hello, Admit, Equip, Brief, Ready, Lease (§5). The console shows the profile in force (§8).
- First task through terminal chat (agent-bot soul chat <name>), an ACP client, or hq task offer <name> --objective ... as a directive.

The pilot target is a first useful task within 30 minutes after account setup (§14). The CLI verbs and the template flow are WP6 deliverables (§13).

### Which operating systems and hardware are supported today, and which are only planned? What does protected Linux versus cooperative macOS mean for my workflow?

**Specified** for platforms (§4 table, §13 stages, §16); **Not specified** for hardware beyond a “declared reference machine” for latency targets (§14) and a declared target platform per package (§11).

Nothing is shipped; the draft is a proposal. At MVP: Linux reference host runs managed protected; macOS runs managed cooperative; Windows is later. The macOS per-member profile is the second protected candidate (Stage 4).

Workflow difference: every feature works on both (tasks, receipts, brokered inference, budgets, recovery). On macOS cooperative, hostile-member containment is not assured: a prompt-injected specialist could read the lead’s files or reach a provider directly, because members share a trust domain. Every receipt and the console say “cooperative” (R8, T21), and any protected claim is refused. Practical rule: on macOS, treat all members as one trust domain and give the Soul only credentials you would give its least-trusted harness. Use a Linux host or VM for protected work.

### What accounts, tools, model providers, and host dependencies do I need before setup?

**Partly specified.** The pilot configuration (§13) names the defaults: Claude Code and Codex adapters over ACP, the Anthropic API with Bedrock as fallback route, one locally hosted model as the offline route, one GitHub App as the service adapter. Harness binaries, runtimes, and small tools are vendored in opt/ (R12, §11), so no separate harness install. What you still need: provider accounts and keys (stored in HQ), a GitHub App with its private key (stored in HQ), the OS baseline (shell, coreutils), and any declared host toolchains such as Xcode or platform SDKs (§11). Harness sign-ins are per machine; “portable” does not remove them (§11). Hardware for the local model is not specified. Proposed: enrollment prints a prerequisite report listing each missing account, toolchain, and sign-in before the first task; §8 already requires the toolchain part.

### How do I choose the lead and specialist harnesses, and how do I know which adapter and harness versions have been qualified?

**Specified** for assignment: the owner picks roles in SoulInfo.json through GeniusBar or the CLI (R4, §11); adapters qualify individually (§2); the compatibility matrix pins adapter versions (§12); evaluation records name revision, harness, model, provider, and date (§9); an upgraded harness is marked unevaluated and warns (§10). **Not specified:** a published qualification list. Proposed: hq adapters list shows each adapter’s version, the profile it qualifies for (protected or cooperative), the primitive classes it can render (§10 adapter manifest), and the last evaluation date for this Soul. Each release ships a signed qualification manifest per adapter version. Choice rule: lead is the harness with the best evaluation on your own task set and a qualified ACP adapter; specialist is the narrower role.

### Is there a sample Soul and a “hello world” task I can use before connecting real repositories or credentials?

**Partly specified.** The first demonstration uses an issue-like task and a simulated remote write (§13), the integration environment may begin with deterministic simulators (§2), and templates produce a new Soul ID (§11). No sample ships yet. Proposed: a hello.soul template with two fake adapters and a simulated service; the hello-world task is “investigate, change one file in a scratch workspace, run the checks, produce a reviewable change” against the simulator. It needs no credentials and exercises T04, T05, and T20 locally.

## Everyday use and control

### How do I assign work, see what each member is doing, and tell when the Soul is waiting for me?

**Specified.** Assign through chat, ACP, or an HQ directive (§5). The console shows current activity, active profile, remaining budget by sub-allocation, unresolved decisions, and last meaningful progress; the detail view shows role assignment, evaluation results, task history, and receipts; it must distinguish queued, delivered, accepted, running, paused, completed, and outcome unknown (§8). A task in waiting records why: owner input, owner pause, dependency, provider availability, or a reconciliation decision (§7). **Partly specified** per member: proposed a member list with runtime state, current task, and lease age (§12 already records lease age).

### What does the agent do when it reaches the edge of its permissions? How specific is an approval request, and can I approve a narrow action without granting broader access?

**Specified.** The broker refuses with a typed code (destination_denied, grant_revoked, budget_exhausted, Appendix A) and the task moves to waiting for owner input (§7). The approval request names the exact action or policy change, the resource and destination, why existing authority is insufficient, expected cost, and expiry; approval is HQ-signed and bound to the record’s digest, so editing the action invalidates it (§8, T24). You can approve that one action, or a bounded class to avoid repeated prompts, and revoke either (§8). A single-action approval grants nothing beyond that digest.

### How do I interrupt work, revoke access, or pause the Soul? What happens to tasks and external actions already in progress?

**Specified.** Pause and resume are hq/v1 operations (§5); your interactive turn preempts background work at its next safe point (§5, §8). Revocation takes effect at the next protected operation (§4). An external effect already submitted cannot be undone; it is reconciled, and the console shows it as underway or outcome unknown rather than paused (§5, §7, §8). Cancel stops future actions and reconciles submitted effects; a late specialist result is kept as evidence without reopening the task (§7). Send reservations settle on retry or cancel (§8).

### Which actions are actually protected by HQ, and which rely on cooperative behavior from a harness?

**Specified** in principle (§4, §6, §7): protected means routed through the broker with a receipt: inference, service calls through adapters, task commits, messages and wake, credential use, lifecycle. Cooperative means inside the member’s own trust domain: edits inside a mounted workspace view, local shell commands, harness-internal tool calls, anything an adapter cannot route. On the cooperative profile, egress is cooperative too. **Proposed:** label each receipt and console row “enforced” or “reported”; §4 already requires the profile and adapter route on every receipt.

### What can the owner console show me about task history, tool calls, decisions, receipts, and unresolved outcomes?

**Specified** for receipts (fields in §7), task history and receipts (§8), outcome unknown (§7), approval and decision records (§5, §8), and content-free diagnostics (§12). Tool calls: only brokered ones have receipts; harness-internal calls appear in native transcripts inside the member’s home and in typed notes, which are self-reported memory, not evidence (§10). **Proposed:** a per-task timeline that interleaves receipts (authoritative) and notes (self-reported) with a visible distinction.

## Repository and tool setup

### How do I grant access to a repository or workspace while limiting which paths can be read or changed?

**Partly specified.** Grants carry action and resource selectors, destinations, and data restrictions (Appendix A); tasks carry a resource scope and an exclusive write scope (§7); HQ mounts mediated workspace views under the protected profile (§4). Remote repository operations go through the service adapter, which validates operation type and resource scope (§4). **Proposed:** a workspace view is a mount of selected paths, each read-only or read-write; grant selectors use path globs; the protected profile enforces them by mount, the cooperative profile by the adapter honoring the scope, and the receipt says which.

### How are credentials added, rotated, and revoked, and how can I confirm they never enter harness-readable files?

**Specified** for the model: HQ holds keys; Equip returns references, never secrets (§5); credentials never travel in the package (§11); revocation and rotation are release prerequisites (§15); T02 verifies the key boundary. **Not specified:** commands. Proposed: hq credential add | rotate | revoke <id>; rotation re-equips at the next lease renewal; confirmation is the T02 result for your host plus hq audit secrets, which scans member homes and workspaces for known secret fingerprints. Under brokered inference the provider key never reaches a harness; the short-lived-token route is the exception and is labeled in every receipt (§4).

### How are harnesses and tools installed and updated inside the package? Does “vendored and pinned” include package managers such as Homebrew?

**Specified:** everything except the OS baseline and declared host toolchains is vendored under opt/ and pinned by SHA-256 in SoulLock.json (R12, §11). Homebrew is neither vendored nor used at run time. A tool the Soul needs is vendored as an artifact in opt/ with its digest, however it was obtained; a tool that can only come through a host package manager (Xcode-class) is a declared host requirement, checked at activation and reported if missing. Updating a pin is a definition change, so it arrives as a candidate revision that the owner accepts (§10). **Proposed:** SoulLock.json records each artifact’s origin (registry, URL, digest) for rebuilds; fetches happen at build time only, never at run time, consistent with the network allowlist (§4).

### When a harness or tool update changes behavior, what must be re-rendered and re-evaluated before the Soul uses it?

**Specified.** An updated pin is a candidate revision; acceptance re-renders every adapter and requires a passing evaluation cell for every role on that harness version (§10, T27). Until acceptance, the old pins keep running. If the harness itself is upgraded on the host without a new revision, the accepted revision is marked unevaluated on that harness, which warns and does not block (§9, §10).

## Dreaming, evaluations, and primitives

### What does a user actually configure to start a dream run, and where do its inputs, candidate changes, eval results, and logs appear?

**Specified** for scope and outputs: a dream grant (time, cost share, cell cap, destinations, executor; Appendix A), scheduled by HQ when idle (§5, §10), funded by the maintenance sub-allocation (§8). Inputs: dreams/inputs/. Candidate: dreams/runs/<run-id>/candidate/. Evaluations: dreams/runs/<run-id>/evals/<cell>/. Run record and failures: the run directory and the candidate revision record. Logs: content-free diagnostics with correlation IDs (§12). **Not specified:** schedule format and commands. Proposed: hq dream grant <name> --share ... --wall-clock ... --cells ... --executor ..., hq dream schedule <name> --idle-after ..., hq dream run <name> --now, hq dream show <run-id>.

### Which evaluation suites ship with the product, and how do I add task-specific tests that reflect my team’s coding standards?

**Partly specified.** The curated set is about 50 tasks per role drawn from your own work, with held-out tasks retained, stored as ATIF (§9, §10). Completion criteria name machine checks or an authorized evaluator (§7). T01–T30 are product conformance tests, not Soul evaluations. **Proposed:** the product ships only the hello-world suite; team standards enter as machine checks in task completion criteria (lint, unit tests, review rules) and as owner-curated tasks marked held-out under dreams/ with a dataset digest. A check whose failure must never be accepted is declared a guardrail (§9).

### What evidence lets me decide that a primitive change is safe and useful across all supported harnesses?

**Specified** (§10, Appendix A candidate revision record): a per-cell matrix for every assigned harness and understudy, with an in-run baseline, held-out non-regression within your tolerance, train improvement, zero guardrail violations, absolute counts, render success per adapter, provenance warnings, and cost. The draft also says a small replay set is not a statistical guarantee (§9). **Proposed** decision rule: accept when held-out delta is non-negative on every assigned cell and train delta is positive on the triggering cell.

### If an adapter or harness version changes, does the system block use of primitives until the required evaluations pass?

**Specified:** no. An already accepted revision keeps running on an upgraded harness with a warning; only a guardrail violation disables a route (§9, §10). What is blocked is acceptance of a new candidate without coverage (eval_coverage_missing, T27). **Proposed:** an owner policy flag to block instead of warn, for Souls where that is the right trade.

### If a candidate fails on one harness, how does the user inspect and approve the narrowed proposal?

**Specified:** the narrowed candidate is a new candidate scoped through per-adapter overrides, re-evaluated, and shown with the same change list, matrix, provenance, and cost; partial acceptance is disallowed (§10, T28). **Proposed:** the narrowed candidate record references the rejected parent and shows the scope diff (which adapters were excluded and why), so the owner sees both matrices side by side.

### What is the practical rollback procedure, and which state is not rolled back along with the definition?

**Specified.** Rollback is rollback-revision: acceptance of the parent digest, never an in-place revert; the previous revision stays pinned; drain, then re-admit at the old digest (§5, §10). Not rolled back: life changes committed by the same run (knowledge consolidation, index rebuilds, consumed dream inputs), external effects already submitted (§13), and receipts. The candidate record lists the life changes rollback does not undo. **Proposed:** hq revision list <name>, hq revision rollback <name> <parent-digest>, then verify the Hello at the old digest in the admission result.

## Cost, recovery, and portability

### Where can I set limits for model spend, evaluation runs, network use, and dream runs, and how are costs attributed to tasks and harnesses?

**Specified.** One ceiling with working and maintenance sub-allocations (§8); grants carry a budget and cost ceiling (Appendix A); the dream grant carries time, cost share, and cell cap (§10); network is an allowlist plus the broker’s narrow API (§4). Receipts record task, caller (member and runtime), destination, and settled cost, so attribution per task and per member is available; §15 defines cost per accepted task. There is deliberately no per-member limit: four members do not get four allowances (§8). Limits are set on grant records through the CLI or GeniusBar.

### What data leaves my machine when I use a remote model, relay, or evaluation provider, and how do I inspect or restrict that data?

**Specified.** Remote model: the task context the broker sends after checking the destination against the task’s data restrictions (§4, §9). Relay: only the outer frame (destination, epoch hint, message ID, expiry, size, wake class); content is sealed, timing and size remain observable (§6). Evaluation exports apply the same disclosure restrictions as the original task (§10). Trace export excludes content (§12). Inspect: receipts record destination, adapter route, and a request digest; sensitive payload is stored separately under its own access policy (§7). Restrict: destinations per grant, disclosure labels, a local model as the destination (§4). **Proposed:** hq receipts <name> --destination <id> to list what went where.

### How do backup and restore work in practice? Which parts of the Soul package can I copy, and what must be exported separately from HQ?

**Specified.** Life (memorial/, dreams/, the comms/ mirror, home/<member>/, workspaces/) travels in the package; cache/ is rebuilt, host/ recreated, tmp/ dropped (§11). Credentials, grants, nonces, the task ledger, deduplication records, and receipts live in HQ’s store and travel only as a protected, authenticated export with secrets and reusable grants excluded (§11, §15). Copying the directory never transfers authority; restore is admission first, then life (§11). **Proposed:** hq soul export <name> --life --offline-artifacts for the package, hq export history <name> for the HQ export; restore is import, history import, enrollment, then re-grant.

### What recovery steps are available after HQ crashes, a harness hangs, or a remote service accepts an action but the Soul loses its response?

**Specified** for two of three. Harness hang: the entry point’s ladder restarts with backoff, quarantines after five crashes in an hour, re-equips on auth failure, fails over on provider outage; a missed lease is stale, not stopped (§5, §9). Lost response: the action is unknown, the task enters reconciling, the returning worker looks up the remote outcome through the broker and never replays blindly; an ambiguous outcome waits for your decision (§7, T06). HQ crash: **Partly specified**: leases expire so protected commits stop while local read-only work continues (§5), and action intents and the outbox are durable (§7, §12); on restart, admission repeats. **Proposed:** HQ runs under the OS supervisor with ledger crash persistence stated in the §12 storage baseline, and hq doctor reports which leases, intents, and unknown actions need reconciliation after a restart.

### What diagnostics should I collect when setup, admission, rendering, or an evaluation fails?

**Specified:** error codes, task and operation IDs, queue depth, lease age, adapter latency, budget use, recovery events, OpenTelemetry GenAI traces (§12); every error carries a correlation ID (Appendix A); test results name revision, policy digest, dependency versions, and profile (§14). **Proposed:** hq diag bundle <name> collecting the admission result, profile, SoulLock digests, adapter manifests, the render log (including render_failed), the evaluation plan and cell summaries, the last 100 receipts with content redacted, and an OTLP span export; never member homes or workspaces.

## Additions (Oct 29, 2026)

These entries answer questions raised while bringing the agent-bot runtime in line with draft 0.4. They use the same tags. “Owner clarification” marks answers that rest on the author’s direction rather than the text of draft 0.4.

## Vocabulary: managed machine and managed Soul

**Owner clarification:** “managed” is used for two different things, kept apart here.

- Managed machine: a machine enrolled with the owner’s identity service that runs the local server. That connection gives the service two-way communication with the machine: it can deliver messages and events to it.
- Unmanaged machine: a computer where an agent runs with only an MCP connection or limited tooling, and no enrolled local server.
- Managed Soul: a Soul whose harnesses are launched and run by its soul package.
- Unmanaged Soul: a Soul whose harness is owned by an app the platform does not run, such as an IDE or a web chat.

An unmanaged Soul can run on a managed machine, for example Devin Desktop on an enrolled Mac.

## Sessions, Souls and apps

### When I talk to a Soul through an app that only shows me sessions, such as Devin Desktop or gemini.google.com, is each conversation a new Soul?

**Specified for identity.** A Soul has one stable identity; members, installations, runtimes, sessions and revisions are attributed separately (§1). A session is a bounded interaction context, one per context or conversation (Vocabulary). A new Soul ID comes only from a template, or a fork with parent provenance (§11). So a new conversation is a new session of the same Soul, not a new Soul.

**Owner clarification:** such an app owns its harness, which makes the Soul unmanaged. The app’s sessions across the life of the app are one Soul, the Soul chosen when the app joined. The unit is the app profile: one app signed in to two accounts gives two Souls.

### How does a managed Soul relate to its harnesses and sessions?

**Specified (§3, Architecture §2).** The entry point runs the lead and its regions as ACP sessions, and each region is a harness with its own sessions and context. The Soul ID stays the same when the owner changes which harness, model or provider fills a role.

**Owner clarification:** in a managed Soul the soul package runs and manages the harnesses. Sessions depend on their harness, and several harnesses and sessions are encapsulated under the one Soul.

### How does what the Soul knows reach an app that only exposes sessions?

**Partly specified for managed Souls:** at clock-in the Soul receives its brief, the directives waiting under existing grants (§5), and a returning lead reads handoff notes and open tasks before continuing (§10).

**Not specified, and an open problem.** Owner clarification: whatever the soul package maintains has to be actively fed back into the app’s sessions; without that, the Soul is little more than sophisticated retrieval. Today an unmanaged Soul gives observability at best. In some cases the app’s hooks can inject context, but there is no general mechanism yet. This question is left open deliberately.

### Can two live sessions of one Soul run at once?

**Partly specified.** Only the current admitted lead may finalise task decisions, and a changed lead gets a new lease generation (§7). One Soul may hold several live sessions, each with its own lease, so only the lead-lease holder finalises a task.

**Owner clarification:** in practice they are usually on different devices, since an app like Devin Desktop runs one instance per machine. Two apps of the same harness family on one machine can still run at once, for example Devin Desktop and the Devin CLI, and would collide if both were recognised only as “Devin” through their MCP connection. A session is therefore identified by at least the device and the client app or profile.

**Not specified:** how a client app or profile is identified when the app does not expose one.

## Communication between agents

### Which agents can talk to each other, across apps and machines?

**Partly specified.** The broker federates messages from a Soul up through site and cloud relays (§3, Architecture §1), and relays see only the outer frame (§6).

**Owner clarification:**

- On one device: with only agent-comms installed, every agent that joins comms can message every other agent on that device, and eventually work in teams. Joining likely depends on agent identity.
- Across managed machines: the managed-machine connection links the devices, so agents on any managed machine can chat with agents on any other.
- Unmanaged agents: limited chat, relying on the identity service to deliver to a managed machine and sync messages, like iMessage for agents.
- External apps: agent-comms also abstracts chat apps such as Telegram and Slack. For unmanaged devices those apps may be hosted on the identity service itself.

## Repositories and credentials

### My agent works in one repository. Can it read or change another?

**Specified.** Credentials are short-lived and scoped to the task or operation (§5, §12). Grants carry resource selectors, and the service adapter checks the operation type and resource scope (§4, Appendix A). At the edge of its permissions the broker refuses with a typed code, and the owner can approve that one action or a bounded class (§7, §8).

**Not specified for the current runtime, which has no grant records yet.** Proposed: the checkout’s own repository is the default grant. A call to another repository is refused with a message naming both; once grants exist, that refusal becomes an approval request.

### Does any tool ever hand the raw GitHub token to the model?

**Specified:** no, and it fails closed. Equip returns opaque handles and credential references, never secrets; a reference resolves to a short-lived token that only HQ holds (§5, Appendix A).

**Owner clarification:** during the legacy transition, the hosted route that returns a raw token stays available behind a feature flag. It is removed once every machine is onboarded and set up for local minting.
