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

Every release conformance report records the platform commit SHA its evidence was checked against ([PDR-0020](../04-decisions/PDR-0020-components-read-the-platform-at-main.md)). That SHA is evidence. Components never pin a platform commit; they read the platform at `main`, as the [component repository contract](../00-governance/component-repo-contract.md) describes.
