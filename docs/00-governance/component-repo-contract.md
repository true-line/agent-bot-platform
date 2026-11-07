---
Status: Accepted
Doc-Type: governance
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
Decided-By: PDR-0001
---

# Component repository contract

What every repository in the [repository catalog](../03-architecture/repository-catalog.md) does so its agents build against the platform instead of beside it. The contract is deliberately small: a pointer, a pin and a few prohibitions.

## Platform block in AGENTS.md

Each component's AGENTS.md carries this block next to the org's governed discovery block. It names the repository, never a commit: agents read the platform at `main`, so the rules they build against are always current ([PDR-0001](../04-decisions/PDR-0001-platform-repository-is-the-product-source-of-truth.md), amended).

```markdown
<!-- platform:agent-bot-platform:start -->
Platform: true-line/agent-bot-platform, read at main.
This repository's charter, seams and requirements are in the platform's
registry/repos.yaml entry for <repo-name>. Read the platform's AGENTS.md
at the start of every task, and before changing a seam or anything a
requirement covers.
<!-- platform:agent-bot-platform:end -->
```

## What a component keeps

- Its implementation design, build and module documentation.
- Its own ADRs, numbered by its own issues, citing the PDR when one applies.
- Its changelog, CI and repository-specific test plans, which cite T-series IDs when they implement a platform test.

## What a component must not keep

- A copy of a platform requirement, term definition, architecture description or cross-repo decision. Link to the platform at `main` instead.
- A pinned platform commit, a lock file or a cached copy of a platform registry. Checks that depend on the platform fetch its `main` and fail, never skip, when they cannot reach it or when a cited ID or linked path is missing there.
- A schema or error code that belongs in soul-contracts.
- A decision that binds another repository. Raise a Decisions discussion in the platform instead.

## Adopting the contract

Adoption happens one repository at a time, by PR in that repository. PDR-0001 was accepted on 2026-11-07, so adoption can start. The repository catalog's `follow-up` field lists what each repository needs to move or delete. The drift register tracks every copy that remains until then.
