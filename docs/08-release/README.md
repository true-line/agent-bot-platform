---
Status: Draft
Doc-Type: index
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
---

# Release

How platform, protocol, schema and adapter versions move together, and what evidence a release must carry. A component releases on its own cadence; this section governs only what crosses repositories.

| Page | Contents |
|---|---|
| [Versioning](versioning.md) | Version policy for platform, protocol, schema and adapters |
| [Release conformance report](release-conformance-report.md) | The T01 to T30 evidence a release publishes |

A platform baseline is a tag on this repository (`baseline/N`) that pins requirement, seam and test versions together. Each component records the baseline it builds against, as the [component repository contract](../00-governance/component-repo-contract.md) describes.
