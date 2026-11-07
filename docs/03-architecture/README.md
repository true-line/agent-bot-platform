---
Status: Draft
Doc-Type: index
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
---

# Architecture

How the platform is divided into trust domains, repositories and contracts. The repository catalog and seams pages are generated from `registry/`; every other page explains a design the registries and soul-contracts schemas make normative.

| Page | Contents |
|---|---|
| [Overview](overview.md) | Two planes, components on one machine, dependency direction, the enforcement point |
| [Repository catalog](repository-catalog.md) | Every repository with its charter, admission criteria and proposed disposition |
| [Seams](seams.md) | Every contract between repositories, its provider, consumers, home and status |
| [Trust domains and profiles](trust-domains-and-profiles.md) | Protected and cooperative profiles; where host-side secrets live |
| [Lifecycle](lifecycle.md) | Admission, sleep, upgrade and recovery of a Soul |
| [Federation](federation.md) | Messaging upward through site and cloud hubs |

## Interfaces

Interface pages summarize a contract for readers. The schema in soul-contracts is normative; where a page and a schema disagree, the schema wins and the page gets a DRIFT entry.

| Page | Seam |
|---|---|
| [hq/v1](interfaces/hq-v1.md) | `hq-v1`: runtime admission and supervision |
| [wire/v1](interfaces/wire-v1.md) | `wire-v1`: message envelope |
| [Task state machine](interfaces/task-state-machine.md) | `task-v1`: task states and transitions |
| [Error registry](interfaces/error-registry.md) | `error-registry`: shared error codes |
| [Package format](interfaces/package-format.md) | `soul-package-format`: the `.soul` directory |
