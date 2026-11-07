---
Status: Draft
Doc-Type: interface
Owner: portability-implementer
Last-Reviewed: 2026-11-05
Normative-Source: true-line/soul-package (§11); overview paper v0.3
---

# Reference: the `.soul` package format

The portable Soul package: manifest, life, vendored artifacts, candidate
trees, transfer records.

> **Normative source:** §11 of whitepaper draft 0.4, the
> [packages overview paper](../../papers/native-shareable-soul-packages-0.3-overview.md),
> and `true-line/soul-package` (`WP5`). `.soul` format 1 and 2 are
> implemented in `agent-bot-identity`.

## Directory layout

| Path | Content | On transfer |
|---|---|---|
| `SoulInfo.json` | identity, roles, definition revision | travels |
| manifest | SHA-256 per path, sizes, modes | travels |
| `SoulLock.json` | rendered-output digests per adapter, pinned artifact digests (vendored under `opt/`, R12) | travels |
| `memorial/` | long-term memory | travels (life) |
| `dreams/` | dream inputs, runs, evals, candidates | travels (life) |
| `comms/` | mirror only — authority lives in HQ | travels (life, as mirror) |
| `home/<member>/` | per-member state (state redirection target) | travels (life) |
| `workspaces/` | mediated workspace views | travels (life) |
| `cache/` | rebuildable | rebuilt |
| `host/` | host-written state | recreated |
| `tmp/` | scratch | dropped |

**Credentials, grants, nonces, task ledger, dedup records, receipts never
enter the package** — they live in HQ's store (§11).

## Digests and pinning

- Manifest: SHA-256 per path; the **definition digest** excludes the
  manifest's own digest field (byte rules in §11)
- Dependency graph; cycles refused
- Everything vendored is pinned by SHA-256 in `SoulLock.json`; fetches at
  **build time only**, never at run time (R12, §11); each artifact's
  origin (registry/URL/digest) recorded for rebuilds (proposed)
- `soul build` renders deterministically through the render-plugin
  interface → per-adapter digest into `SoulLock.json`; failures emit
  `render_failed` naming the class (§10)

## Import validation (§11, R12)

Path traversal, absolute paths, symlink escapes, expansion limits,
platform match, declared host requirements in `SoulInfo.json`,
dependency cycles. Import **validates before activation**.

## Identity rules

- **Templates and forks produce a new Soul ID**; fork records parent
  provenance (§11)
- Sleep and upgrades produce **new definition revisions**; the Soul ID
  never changes; pinning pins a definition revision (S1 D3, S1 D4)
- Candidate trees: full tree under `dreams/runs/<run-id>/candidate/` with
  own manifest + digest; promotion to an **immutable revision directory**
  (§10)

## Transfer record (§11)

Life selection by class; `comms/` as mirror; template/fork derivation;
**no secrets or reusable grants** in the transfer record. Offline
artifacts and target platforms per Stage 4.

## Related

- [Backup/restore/transfer how-to](../../user-guide/how-to/backup-restore-transfer.md)
- [Render plugins](../../user-guide/adapters/render-plugins.md)
- [Package attack tests: T16](../../08-release/release-conformance-report.md#conformance-suite-t01-t30)
