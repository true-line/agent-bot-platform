---
Status: Accepted
Doc-Type: governance
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
Decided-By: PDR-0001
---

# Document control

How a platform document is labeled, owned, reviewed and retired, so an agent can tell a rule from a draft by reading the first lines. `tools/check_platform.py` enforces everything on this page.

## Front matter

Every page under `docs/` starts with YAML front matter. Keys are capitalized so the org docs-gov gate reads the same fields.

```yaml
---
Status: Draft            # Draft | Proposed | Accepted | Superseded | Retired | Frozen
Doc-Type: explanation    # see the table of document types
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
Superseded-By: docs/... # required when Status is Superseded
Sources: S6 §4           # optional: the source sections this page promotes
---
```

The H1 follows the front matter, and the first paragraph after it states the point of the page.

## Status

| Status | Meaning | Who sets it |
|---|---|---|
| Draft | Being written. Not to be relied on. | Any contributor |
| Proposed | Complete and awaiting the owner's acceptance. Describes intent. | Any contributor |
| Accepted | Normative. Agents follow it. | Product owner, by approving the PR |
| Superseded | Replaced; `Superseded-By` names the replacement. Never deleted. | The PR that accepts the replacement |
| Retired | No longer applies and has no replacement. | Product owner |
| Frozen | A source paper. Never edited except to fix a conversion error. | Nobody |

Pages migrated from the earlier `soul-docs` portal entered as Draft on 2026-11-07. They were converted and curated by agents without an owner review, so none of them is Accepted yet.

## Document types

| Doc-Type | Used for |
|---|---|
| index | Section landing pages |
| governance | How this repository works |
| concept | Vision and scope |
| requirements | Requirement prose not generated from the registry |
| explanation | Architecture and design reasoning |
| interface | Thin overview of a seam, pointing to its contract |
| decision | PDRs and decision indexes |
| security | Threat model, data flow, key boundaries |
| intelligence | Memory, improvement and evaluation design |
| strategy, plan, report | Verification and release artifacts |
| runbook, how-to, tutorial, reference | Operator and developer documentation |
| generated | Pages written by `tools/gen_docs.py` |
| paper, archive | Frozen provenance |

## Owners

Owners are roles, so a document survives a change of person. The roles follow the work packages in whitepaper draft 0.4 section 13.

| Role | Responsible for |
|---|---|
| product-owner | Scope, requirements, acceptance of PDRs and Accepted status |
| platform-maintainer | Structure, tooling, registries, document hygiene |
| protocol-maintainer (WP1) | Contracts, glossary, interfaces, traceability |
| security-reviewer | Threat model, key boundaries, privacy, security sign-off |
| verification-lead (WP7) | Test strategy, conformance catalog, release evidence |
| security-implementer (WP2), runtime-implementer (WP3), comms-implementer (WP4), portability-implementer (WP5), product-implementer (WP6) | Accuracy of pages about their work package |

## Citing sources

Cite a source by its ID from `registry/sources.yaml` and a section mark: "S6 §4", "S1 D2". A bare section mark with no source ID, such as "§7", means S6 at the version pinned in the registry; migrated pages use this shorthand throughout. The PR that re-pins S6 to a new version checks every bare mark. Cite an external standard by its X-series ID and a repository's own decision with its repository name.

## Review cadence

Accepted pages are reviewed at least every 90 days; the checker warns when `Last-Reviewed` is older. A review that changes nothing still updates the date in a PR, so the history shows who confirmed the page.
