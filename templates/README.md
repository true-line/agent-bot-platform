# Templates

Starting points for platform records. Copy one into its section under `docs/`, fill every angle-bracket field, delete the guidance quotes, and add the page to the `mkdocs.yml` nav. Field rules are in [document control](../docs/00-governance/document-control.md).

| Template | Use for | Section |
|---|---|---|
| [pdr.md](pdr.md) | A decision that passes the platform test | `docs/04-decisions/` |
| [test-plan.md](test-plan.md) | The plan for a stage's exit evidence | `docs/07-verification/` |
| [explanation.md](explanation.md) | Why a design is the way it is | `docs/03-architecture/`, `docs/05-security-privacy/`, `docs/06-intelligence/` |
| [how-to.md](how-to.md) | One operator task | `docs/user-guide/how-to/` |
| [runbook.md](runbook.md) | One failure class that spans repositories | `docs/09-operations/runbooks/` |
| [security-review.md](security-review.md) | A review that changes a trust boundary, seam or requirement | `docs/05-security-privacy/` |

There is no ADR template here: a decision inside one repository is that repository's ADR, written from its own template. There is no RFC either; a cross-repository proposal starts as a Decisions discussion.
