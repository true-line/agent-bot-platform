---
Status: Draft
Doc-Type: explanation
Owner: platform-maintainer
Last-Reviewed: 2026-11-12
Sources: S6 §5, §9; S1; Oct 29 vocabulary
---

# Lifecycle: admission, sessions, recovery

How a Soul comes alive on a machine, how conversations relate to it, and
how it recovers.

## Admission: one sequence

Start, first clock-in on a new machine, daily report-in, and migration
are **one flow** (the clock-in flow):

```
Hello → Admit → Equip → Brief → Ready → Lease
```

- **Hello** announces Soul, agent (`member_id`, PDR-0053), installation,
  runtime, session identities
- **Admit** validates and admits; the result names profile + definition
  digest
- **Equip** returns **credential references** — never secrets
- **Brief** delivers the brief plus directives waiting under existing
  grants; a returning lead reads handoff notes and open tasks before
  continuing (§10)
- **Lease** fences authority in time; leases expire, so a crashed HQ
  stops protected commits while read-only work continues

Life transfer on a new host: **validate, restore, rebuild indexes,
reconnect credentials, report gaps** (§11).

## Souls, agents, installations, runtimes, sessions

Five identifiers, attributed separately (§1). The Oct 29 vocabulary
sharpened the everyday cases:

- A new conversation in a sessions-only app (Devin Desktop,
  gemini.google.com) is a **new session of the same Soul** — never a new
  Soul. New Soul IDs come only from templates or forks.
- **Managed Soul**: HQ starts the Soul. **Unmanaged Soul**: HQ does not
  start it; it is started from the command line, or an app the platform
  doesn't run owns the harness (IDE, web chat) (PDR-0055). HQ does not
  start Souls yet. An unmanaged Soul can live on a managed machine
  (Devin Desktop on an enrolled Mac).
- Sessions are identified by **at least device + client app/profile** —
  two same-family apps on one machine (Devin Desktop + Devin CLI) would
  collide otherwise.
- Only the **current admitted lead** finalises task decisions; several
  live sessions may exist, each with its own lease.

Open problem (deliberate): there is no general mechanism yet for feeding
package-maintained knowledge back into an app that only exposes sessions;
today that is observability at best.

## Recovery: the ladder

Specified rungs (§5, §9):

1. **Restart with backoff**
2. **Quarantine** after five crashes in one hour
3. **Re-equip** on auth failure
4. **Fail over** on provider outage
5. **Reconcile** unknown outcomes — broker lookup, never blind replay
   (§7, T06)

A missed lease is **stale, not stopped**. Interactive turns preempt
background work at the next safe point. Cancel reconciles submitted
effects; late results are evidence, not reopened work.

## Sleep and dreams

Sleep/dream maintenance is owner-gated and grant-bounded: dreams are
admitted workflows **with no administrative authority**; accepting
instruction changes needs a separate grant. Sleep and upgrades produce
new definition revisions; the Soul ID and address never change
([memory how-to](../user-guide/how-to/dreams-and-evals.md), paper §10).

## Sequence references

- Operator view: [quickstart admission steps](../user-guide/tutorials/quickstart.md#5-start-the-soul)
- HQ crash: [runbook](../09-operations/runbooks/hq-restart.md)
- Harness hang/crash loop: [runbook](../09-operations/runbooks/harness-crash-loop.md)
