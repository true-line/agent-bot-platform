# AGENTS.md

This repository is the product source of truth for the Soul Agent Platform. Agents working in any platform repository read it before changing behavior that crosses a repository boundary. It holds intent and cross-repo design; component repositories hold implementation.

<!-- governed:shared-agent-discovery:start -->
Shared agent conventions, skills, SOPs and org-wide decisions are discovered from [qwts/qwts-agent-sop](https://github.com/qwts/qwts-agent-sop): start at the [agent conventions](https://github.com/qwts/qwts-agent-sop/blob/main/docs/reference/agent-conventions.md), then the [SOP index](https://github.com/qwts/qwts-agent-sop/blob/main/docs/sop/README.md) and the [ENG decisions index](https://github.com/qwts/qwts-agent-sop/blob/main/docs/decisions/README.md). Inherit by default and vary by explicit delta (ENG-0008). Resolve the current approved SOP head once per operation and record the commit you read.
<!-- governed:shared-agent-discovery:end -->

## Read order

1. [Authority and ownership](docs/00-governance/authority-and-ownership.md): which source wins and where each kind of fact lives. Read it before writing anything.
2. [Repository catalog](docs/03-architecture/repository-catalog.md) and [seams](docs/03-architecture/seams.md): what each repository is for and the only legitimate couplings between them.
3. [Product requirements](docs/02-requirements/product-requirements.md) and the [traceability matrix](docs/02-requirements/traceability-matrix.md).
4. The [decisions index](docs/04-decisions/README.md) for any PDR touching your change, then the [drift register](docs/00-governance/drift-register.md) for known conflicts in your area.

## Rules

- **One fact, one home.** Before writing a requirement, term, architecture statement or decision anywhere, find its home in the ownership table. Link to it; never restate it in a component repository.
- **Registries first.** Requirements, tests, repositories, seams, sources and identifiers live in `registry/*.yaml`. Pages generated from them carry a do-not-edit banner. Change the registry, then run `.venv/bin/python tools/gen_docs.py`.
- **IDs resolve or they do not exist.** Cite only IDs declared in [identifiers](docs/00-governance/identifiers.md). Cite a repository's own ADR with its repository name ("agent-comms ADR-0028"). Never mint an ID by hand: a PDR number is its Decisions discussion number.
- **Conflicts stop work.** When two sources disagree, do not pick one. Add or update a DRIFT entry and raise a Decisions discussion if it needs a choice.
- **No new repository without a charter.** A repository is created only after its entry in `registry/repos.yaml` merges here, under [PDR-0002](docs/04-decisions/PDR-0002-repository-topology-and-admission.md).
- **Papers are frozen.** Files in `docs/papers/` and `docs/archive/` are provenance, pinned by hash in `registry/sources.yaml`; the original files stay with the owner, outside the repository. Promote their content into a controlled record and cite the source ID; do not edit them.
- **Unspecified stays unspecified.** If no controlled record says it, write that it is unspecified and link the open discussion. Do not infer normative behavior from a paper's prose.
- **No personal or legal records.** Legal filings, identity documents, personal names, home or registered-office addresses, phone numbers and personal email never enter this repository; write "True Line AI" or "the owner" instead of a person's name, not even in an ignored folder. Keep them outside the working tree. `tools/check_platform.py --privacy` fails on them by path and content.
- **Process lives in the SOP.** Issue, branch, PR, review and release procedure come from the governed block. This repository records only its deltas, in [change control](docs/00-governance/change-control.md).

## Validate before push

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/gen_docs.py
.venv/bin/python tools/check_platform.py
.venv/bin/mkdocs build --strict
```

All three must pass. CI runs the same commands plus the org docs-gov gate.
