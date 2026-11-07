---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: backup, restore, and transfer a Soul

Move a Soul to another machine, or recover it after loss. Specified (§11,
§15).

## What travels where

| Part | Lives | Travels by |
|---|---|---|
| Life: `memorial/`, `dreams/`, `comms/` mirror, `home/<member>/`, `workspaces/` | package | the package |
| `cache/` | package | rebuilt, not copied |
| `host/` | package | recreated at restore |
| `tmp/` | package | dropped |
| Credentials, grants, nonces, task ledger, dedup records, receipts | **HQ store** | protected, authenticated export only — **secrets and reusable grants excluded** (§11, §15) |

**Copying the directory never transfers authority.** Restore is admission
first, then life (§11).

## Export

```bash
hq soul export <soul> --life --offline-artifacts   # the package side
hq export history <soul>                           # the HQ-store side
```

## Restore on the target machine

1. Import the package: `hq soul import <path>.soul` — full validation runs
   (manifest, traversal, platform, host requirements, dependency cycles,
   §11)
2. Import history from the protected export
3. Enroll the Soul on the new host (owner-verified out-of-band challenge)
4. Re-grant: authority is *not* in the export, by design
5. Start: admission repeats, then life comes back
   ([quickstart admission steps](../tutorials/quickstart.md#5-start-the-soul))

The new host **validates, restores, rebuilds indexes, reconnects
credentials, and reports gaps** — that is the clock-in flow, and one flow
covers first start, daily report-in, and migration (north star, life
transfer).

## Templates and forks

**Template = new Soul ID.** **Fork = new ID with parent provenance.** Both
are HQ lifecycle operations alongside start, stop and move (§11). You
cannot fork your way to keeping the same ID — stable identity is the point.

## Offline artifacts

`--offline-artifacts` packages vendored, pinned artifacts (SHA-256 in
`SoulLock.json`) for a target platform — for machines that must build
without network (§11, Stage 4).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Import refuses with traversal error | package tampered or badly built | rebuild from source template; investigate origin |
| Restore works, no credentials | secrets excluded from export by design | re-add via `hq credential add` |
| History import rejects | export/soul mismatch | match export to Soul ID + epoch |
