---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-07
Date: 2026-11-07
Accepted: 2026-11-07
Discussion: https://github.com/true-line/agent-bot-platform/discussions/20
Affects-Repos: [agent-bot-platform, soul-contracts, soul-conformance, agent-bot, agent-bot-hq, agent-bot-machine, agent-comms, agent-bot-identity, agent-bot-souls, soul-package, soul-adapters, geniusbar, agent-watchtower]
Affects: [governance]
---

# PDR-0020 Components read the platform at main

Component repositories read the platform at `main`, never at a pinned commit, and their checks fail loudly when that context goes invalid. Agents no longer build against platform rules that have silently changed. This record amends decision 4 of [PDR-0001](PDR-0001-platform-repository-is-the-product-source-of-truth.md), which pinned each component to a baseline commit.

## Context

- PDR-0001 decision 4 pinned each component's platform block to a baseline commit. Change control said that moving to a newer baseline is a PR in each component, but not when. Pins therefore aged by default, and keeping them current cost one bump PR per adopted repository per baseline.
- The owner, in [discussion #20](https://github.com/true-line/agent-bot-platform/discussions/20): agents getting invalid context and developing towards a stale pin is the most expensive thing that can happen, and it happens all the time.
- The pin guarded against a cheaper and rarer failure: "a platform edit cannot change a component's rules mid-task". An agent reads the rules at the start of a task, and its PR's CI runs again before merge.
- The platform already keeps what components cite stable. R and T IDs are never reused ([identifiers](../00-governance/identifiers.md)), and source papers are frozen and pinned by hash in `registry/sources.yaml`.
- When this was decided, only soul-contracts had adopted the platform block, at `baseline/3`. Eight adoption issues in other repositories asked for `baseline/2`.

## Decision

1. **Read at `main`.** The platform block names the repository, never a commit, and agents read the platform's AGENTS.md at the start of every task. Links into the platform use `blob/main/...`. The [component repository contract](../00-governance/component-repo-contract.md) is the single home for the block.
2. **Checks fetch `main` and fail loudly.** A component check that depends on the platform fetches its `main` fresh on every run. It fails when a cited ID or linked path does not exist there, and when it cannot reach the platform. There are no lock files, pinned commits or cached copies of platform registries.
3. **Record what was checked.** CI logs the platform commit SHA it fetched, and every [release conformance report](../08-release/release-conformance-report.md) records it, so a release can always say which rules it was checked against. A recorded SHA is evidence, never the rules to build against.
4. **A platform-caused failure is a real signal.** A component CI failure caused by a platform change on `main` is not a flaky runner. It is fixed, never bypass-merged.
5. **The platform owns the breakage it causes.** A platform PR that retires a page, ID, requirement or seam that a component relies on opens an issue in each affected repository and links it from the PR.
6. **Status still governs.** Reading `main` surfaces Proposed pages and Proposed PDRs. They guide work; only Accepted ones bind it.
7. **Baselines are history.** The `baseline/1` to `baseline/3` tags stay, and no component pins them.

## Acceptance

The owner accepted option 1 on 2026-11-07, in the marked answer to [discussion #20](https://github.com/true-line/agent-bot-platform/discussions/20). The answer accepted the recommended mechanics and added decisions 3 and 4. It also confirmed decision 6, and asked that this be recorded as its own PDR, with an Amendment on PDR-0001, rather than as a rewrite or a full supersession of PDR-0001.

## Consequences

- **Platform:**
  - PDR-0001 gains an Amendment that cites this record.
  - The [component repository contract](../00-governance/component-repo-contract.md), [change control](../00-governance/change-control.md), [authority and ownership](../00-governance/authority-and-ownership.md) and the [release pages](../08-release/README.md) follow this record.
- **soul-contracts:**
  - It switches to the read-at-main block and removes `platform.lock.json` and `scripts/platform_lock.py`.
  - Its `scripts/validate.py` fetches the platform's `main`, logs the commit SHA it checked, and fails rather than skips ([soul-contracts#30](https://github.com/true-line/soul-contracts/pull/30)).
- **Every other catalog repository** adopts the read-at-main block when it adopts the platform. Its adoption issue says so.
- **Releases:** the release conformance report records the platform commit SHA its evidence was checked against.
- **Red builds are expected:** component CI can turn red because of a platform change, with no change in the component. That is the intended signal.

## Alternatives considered

- **Keep pins and automate the bumps.** A workflow would open a bump PR in each adopted repository per baseline. Context stays stale between bumps, the bumps add PR noise in every repository, and the workflow needs a cross-repository bot grant.
- **Keep pins as they are.** This is the failure the owner names.
- **Rewrite PDR-0001 decision 4 in place.** The owner chose a separate record, so the changed rule has its own decision and PDR-0001 keeps its history.
