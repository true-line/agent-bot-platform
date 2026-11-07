---
Status: Accepted
Doc-Type: governance
Owner: product-owner
Last-Reviewed: 2026-11-07
Decided-By: PDR-0001, PDR-0020
---

# Change control

How a platform-level change is raised, decided, recorded and adopted by component repositories. Process mechanics (issues, branches, PR review, merge) come from the SOP through the governed block in [AGENTS.md](https://github.com/true-line/agent-bot-platform/blob/main/AGENTS.md); this page records only the platform's deltas.

## Is it a platform decision?

A decision is a PDR only if at least one is true:

1. It binds two or more repositories.
2. It changes a seam: a contract between repositories, or who provides it.
3. It changes product requirements, scope or the quality bar.
4. It changes trust domains, authority, or the enforcement model.
5. It changes the repository topology (create, merge, split, archive, transfer).

Otherwise it is a decision in the one repository it affects, recorded there as that repository's ADR. Signing teams, build tools, module layout, a component's storage engine and a single repository's CI are all component decisions. The platform does not index them unless one later constrains a seam.

Every PDR declares `Affects-Repos` and `Affects` (seams, requirement IDs or `topology`) in its front matter. The checker rejects a PDR that names fewer than two repositories and affects no seam, requirement or topology.

## Decision flow

1. **Raise.** Open a discussion in [Decisions](https://github.com/true-line/agent-bot-platform/discussions/categories/decisions) using its form: the question, why it is platform-level, options with trade-offs, affected repositories and seams, and a recommendation. The discussion number N is the decision's ID, PDR-N, written with four digits. GitHub numbers issues, PRs and discussions from one sequence, so two agents can never allocate the same number.
2. **Deliberate.** Agents comment under their own identity with evidence. An agent's opinion is advice; it is not approval.
3. **Record.** A PR adds `docs/04-decisions/PDR-NNNN-slug.md` from the [PDR template](https://github.com/true-line/agent-bot-platform/blob/main/templates/pdr.md) with `Status: Proposed` and the discussion URL.
4. **Accept.** The product owner marks the chosen answer in the discussion and approves the PR that sets `Status: Accepted` and the `Accepted` date. The merged PR is the record of acceptance.
5. **Fan out.** Each affected repository gets an issue that cites the PDR. Repository-local ADRs that implement it cite it too. A component never re-decides an accepted PDR locally.
6. **Supersede, never rewrite.** A changed decision is a new PDR with `Supersedes`; the old one gains `Superseded-By` and keeps its text.

## Changing a requirement, test or seam

Requirements, tests, repository charters and seams change by PR to `registry/`. The PR runs the generator so the generated pages change with it. A change to an Approved requirement, to what a test must prove, or to a seam's provider is a decision and needs a PDR first.

A contract change follows the same order: the PDR or requirement changes here, then the schema and fixtures change in soul-contracts, then implementations follow. No agent changes a shared schema to make its own implementation pass.

## Reading the platform

Component repositories read the platform at `main` ([PDR-0020](../04-decisions/PDR-0020-components-read-the-platform-at-main.md)). Building against stale rules costs more than a rule changing mid-task. An agent reads the platform at the start of every task, and its PR's CI checks against `main` again before merge.

- Each component's AGENTS.md carries a platform block that names no commit. See [component repository contract](component-repo-contract.md).
- A component's CI that depends on the platform fetches `main` and fails, never skips, when a cited ID or linked path is missing. It logs the platform commit SHA it fetched.
- A component CI failure caused by a platform change on `main` is a real signal. It is fixed, never bypass-merged.
- A platform PR that retires a page, ID, requirement or seam a component relies on opens an issue in each affected repository and links it from the PR. R and T IDs are never reused and source papers are frozen, so most platform changes cannot break a component.
- A commit SHA may record what was checked, as in a release conformance report or a CI log. It is never the context an agent builds against. The `baseline/1` to `baseline/3` tags remain as history.

## Drift

Any agent that finds two sources in conflict adds a DRIFT entry to the [drift register](drift-register.md) in the same PR, or in a dedicated PR when it is mid-task elsewhere. An entry closes only when one side is removed or replaced by a link.
