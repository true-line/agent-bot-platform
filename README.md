# agent-bot-platform

The product source of truth for the Soul Agent Platform: what the product must do, how its repositories fit together, what was decided, and how a release is proven. Component repositories implement; this repository specifies and decides.

## What lives here

| Path | Contents | SDLC / STLC phase |
|---|---|---|
| [docs/00-governance](docs/00-governance/README.md) | Authority order, fact ownership, document control, change control, identifiers, drift register | Governance across all phases |
| [docs/01-concept](docs/01-concept/README.md) | Vision, scope, users | Concept |
| [docs/02-requirements](docs/02-requirements/README.md) | Product requirements, quality attributes, traceability | Requirements; test analysis |
| [docs/03-architecture](docs/03-architecture/README.md) | Architecture, trust domains, repository catalog, seams, interfaces | Design |
| [docs/04-decisions](docs/04-decisions/README.md) | Platform decision records (PDR), cross-repo ADR index | Design |
| [docs/05-security-privacy](docs/05-security-privacy/README.md) | Threat model, key boundaries, data flow and retention | Design; security testing |
| [docs/06-intelligence](docs/06-intelligence/README.md) | Memory, bounded improvement, evaluation and accuracy | Design; evaluation |
| [docs/07-verification](docs/07-verification/README.md) | Test strategy, conformance catalog | Test planning and design |
| [docs/08-release](docs/08-release/README.md) | Versioning, release criteria, conformance reports | Release |
| [docs/09-operations](docs/09-operations/README.md) | Support, runbooks | Operations |
| [docs/10-program](docs/10-program/README.md) | Roadmap, stages, work packages, risks | Planning and tracking |
| [docs/user-guide](docs/user-guide/README.md) | Tutorials, operator how-to, adapter guides, CLI reference | Product documentation |
| [docs/papers](docs/papers/soul-platform-draft-0.4.md), [docs/archive](docs/archive/soul-platform-draft-0.3.md) | Frozen source papers and superseded drafts | Provenance |
| `registry/` | Machine-readable requirements, tests, repositories, seams, sources, identifiers | All |
| `templates/` | Templates for PDRs, test plans, runbooks and other records | All |
| `tools/` | Generator, drift gate, converters | All |

## Working here

Agents start at [AGENTS.md](AGENTS.md). People start at the [documentation home](docs/index.md) or build the site:

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Decisions are raised in the [Decisions discussions](https://github.com/true-line/agent-bot-platform/discussions/categories/decisions) and recorded as PDRs; see [change control](docs/00-governance/change-control.md). Contribution rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, copyright True Line AI LLC; see [LICENSE](LICENSE). The platform repositories share this license. Owner products built on top of the platform, such as GeniusBar, are proprietary ([PDR-0002](docs/04-decisions/PDR-0002-repository-topology-and-admission.md)).
