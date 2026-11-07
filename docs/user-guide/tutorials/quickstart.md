---
Status: Draft
Doc-Type: tutorial
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# Quickstart: your first Soul task

Get from zero to one completed task on a sample Soul — no real repositories
or credentials. Target: **first useful task within 30 minutes of account
setup** (whitepaper §14). Uses the `hello.soul` template with two fake
adapters and a simulated service, exercising T04, T05, and T20 locally.

> [UNSPECIFIED — proposed] CLI verb names below are the proposed sequence
> from [Operator Questions](../../papers/operator-questions-2026-10-29.md#getting-started);
> the draft requires an HQ CLI (§3, §8) but does not name verbs. WP6 owns
> the final names ([CLI reference](../reference/cli.md)).

## What you need

- One host: **Linux** (runs protected) or **macOS** (runs cooperative —
  see [trust domains](../../03-architecture/trust-domains-and-profiles.md#protected-vs-cooperative))
- An account on the host; that account becomes the **owner** (§4)
- Model provider account and key, or the offline local-model route
- ~15 minutes

## 1. Install HQ

Install the managed-machine daemon under the account that will own it.
HQ creates its control socket, key store, and authority database (§4).

```bash
# install managed-machine (mechanism TBD — provisioning exists today)
```

## 2. Create a Soul from the sample template

```bash
hq soul create my-first-soul --template hello.soul
```

HQ validates the manifest, path traversal, platform match, host
requirements, and dependency cycles before activation (§11), and reports
missing toolchains before any work (§8).

## 3. Assign roles

```bash
hq soul roles my-first-soul --lead fake-lead --specialist fake-specialist
```

Writes `SoulInfo.json` as a **new definition revision** under an owner
approval record (§8, §11).

## 4. Add credentials (optional for hello.soul)

The sample needs none — the simulated service takes no keys. For real
Souls:

```bash
hq credential add <id>
```

Keys go into HQ's store; they never enter the package (§11,
[credential details](../how-to/credentials.md)).

## 5. Start the Soul

```bash
hq soul start my-first-soul
```

The entry point runs the admission sequence: **Hello, Admit, Equip, Brief,
Ready, Lease** (§5). The console shows the profile in force (§8) — check
it says `cooperative` on macOS, `protected` on Linux.

## 6. Offer the hello-world task

```bash
hq task offer my-first-soul --objective "investigate, change one file in the scratch workspace, run the checks, produce a reviewable change"
```

Or chat: `agent-bot soul chat my-first-soul`. The task runs against the
simulated service: scoped proposal first, then one final commitment (T04,
T05).

## 7. Watch it finish

The console distinguishes **queued → delivered → accepted → running →
completed** (§8). When it completes, inspect:

- The **receipts timeline**: every brokered action with task, caller,
  destination, settled cost (§7)
- The **task record**: proposal, commitment, outcome
- `hq receipts my-first-soul` — what went where

## What you just did

A Soul was admitted under a declared profile, did one scoped task with
brokered, receipted effects, and finished — without any credential ever
reaching a harness. Next: [connect real work in the pilot
tutorial](first-pilot-task.md), or read
[why this design](../../03-architecture/trust-domains-and-profiles.md).

## Troubleshooting

| Symptom | Likely cause | Where to look |
|---|---|---|
| Activation refuses with a platform error | Target platform mismatch in manifest | import validation report (§11) |
| "missing toolchain" before first task | Declared host requirement absent | §8 prerequisite report |
| Task stuck in `waiting` | Recorded reason: owner input / dependency / provider | console detail view (§7) |
| hello.soul render fails | render plugin stub | [render plugins](../adapters/render-plugins.md) |
