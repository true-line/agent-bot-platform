# Contributing

How to change the platform record. Issue, branch, review and merge mechanics come from the org SOP linked in [AGENTS.md](AGENTS.md); this page covers only what is specific to this repository.

## Decide whether the change belongs here

A change belongs here only when it passes the platform test in [change control](docs/00-governance/change-control.md): it binds two or more repositories, or changes a seam, a requirement, the quality bar, the trust model, the topology or the scope. A change that touches one repository is that repository's own ADR or spec.

## Kinds of change

| Change | Where | How |
|---|---|---|
| A decision that needs the owner | [Decisions discussions](https://github.com/true-line/agent-bot-platform/discussions/categories/decisions) | Open the discussion first; its number becomes the PDR number. Record the outcome as a PDR in a PR. |
| Requirement, test, repository, seam, source | `registry/*.yaml` | Edit the registry, regenerate the views, open a PR. |
| A conflict between two sources | [Drift register](docs/00-governance/drift-register.md) | Add the next DRIFT entry; do not choose a winner in the same PR. |
| Explanation, runbook, guide | The page under `docs/` | Keep the front matter current; a new page joins the `mkdocs.yml` nav. |
| A new source paper | `registry/sources.yaml` and `docs/papers/` | Keep the original outside the repository and pin its SHA-256. Add a converted copy as Frozen, with personal names replaced by "True Line AI", and pin the conversion too. |

## Before you open a PR

```sh
.venv/bin/python tools/gen_docs.py
.venv/bin/python tools/check_platform.py
.venv/bin/mkdocs build --strict
```

CI runs the same three steps and the org docs-gov gate. Generated pages carry a do-not-edit banner; a hand edit to one fails the checker.

## Never commit

Personal or legal records of any kind: filings, identity documents, personal names, addresses, phone numbers, personal email. Keep them outside the working tree entirely. The privacy check is part of `tools/check_platform.py`, so it runs before every push and in CI. Do not set `core.hooksPath` in this repository: it would replace the machine's agent-bot hooks.
