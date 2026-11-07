---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-07
Date: 2026-11-07
Discussion: https://github.com/true-line/agent-bot-platform/discussions/2
Affects-Repos: [agent-bot-platform, agent-bot, agent-bot-daemon, agent-bot-machine, managed-machine-config, agent-machine-configurations, agent-comms, agent-bot-identity, agent-bot-souls, soul-package, soul-adapters, geniusbar, geniusbar-connector, agent-command-center, agent-github-identity, agent-watchtower]
Affects: [topology, hq-v1, governance]
---

# PDR-0002 Repository topology and admission

The platform's repositories follow trust domains and seams, not features. A repository exists only when it meets an admission criterion and owns a seam. This record applies that rule to the 22 repositories in scope today and sets the rule for every new one.

## Context

The platform's code and plans are spread across two GitHub accounts, true-line and qwts. Several repositories overlap. GitHub App identity has three homes, the web console has two with a third planned, and two products call themselves headquarters. Two repositories are empty, and the daemon's plan names repositories that do not exist. Whitepaper draft 0.4 already states the principle: repositories follow trust-domain and contract boundaries, and dependencies point toward the contract repositories. Nothing enforces it.

## Decision

1. **Admission.** A repository is created, kept or split only if it meets at least one criterion and provides or consumes at least one seam in `registry/seams.yaml`:
   - C1: it runs in a distinct trust domain or as a distinct security principal;
   - C2: it releases on its own cadence behind a versioned contract;
   - C3: it needs separation of duties;
   - C4: it needs different visibility or licensing.

   Anything else is a directory in an existing repository.
2. **Charter first.** A new repository's entry in `registry/repos.yaml` merges in this repository before the repository is created. The entry states one purpose, what it owns, what it must not own, and its seams.
3. **HQ is agent-bot-daemon**, as the owner decided on 2026-10-27 (agent-bot-daemon D1). agent-bot-machine is the host's admin sandbox and executor (agent-bot-daemon D4), not HQ.
4. **Dispositions.** The [repository catalog](../03-architecture/repository-catalog.md) is authoritative. In summary:
   - **Keep:** agent-bot-platform, soul-contracts, soul-conformance, agent-bot, agent-bot-daemon, agent-bot-machine, managed-machine-config, agent-comms, soul-package and soul-adapters.
   - **Keep as owner products:** geniusbar and agent-watchtower. They sit on top of the platform and are not part of it.
   - **Keep and split:** agent-bot-identity. The HQ half moves to agent-bot-daemon and the Soul runtime moves out; the identity CLI and hooks stay.
   - **Designate:** agent-bot-souls becomes the Soul runtime home that the daemon's plan calls soul-runtime, instead of creating a new repository.
   - **Merge into agent-bot:** agent-command-center (the web console UI) and agent-github-identity (GitHub App MCP tools). The planned agent-bot-ui is not created.
   - **Archive:** agent-machine-configurations (empty) and geniusbar-connector (prototype).
   - **Adjacent, outside the product:** embedded-skills, agent-fleet, agent-space and engineering-relay. They are listed so agents know they exist and are not platform components.
5. **Names.** Platform repositories are namespaced `agent-bot-` or `soul-` so they are easy to find as a set. A new platform repository takes one of those prefixes. Existing names outside them, such as agent-comms, are not renamed by this record.
6. **Licensing.** Platform repositories are MIT-licensed and intended to be public. Owner products (geniusbar, agent-watchtower) are proprietary. managed-machine-config holds the owner's fleet data rather than platform code and stays private. A repository becomes public only after the privacy check passes on its whole history.
7. **One account.** Platform repositories live in true-line. agent-comms, agent-bot-identity and managed-machine-config transfer from qwts when their release channels (Homebrew taps, install URLs) can move without breaking installs.

## Consequences

- The 22 repositories in scope settle into 12 platform repositories, 2 owner products, 4 adjacent tools and 4 merged or archived. One planned repository (agent-bot-ui) is never created.
- Each surviving repository has one sentence of purpose, so an agent can tell where a change belongs before writing it.
- Seams whose contracts exist only as plans or repo-local prose become visible and are ranked for promotion into soul-contracts.
- Merges and transfers cost real work: GitHub redirects, Homebrew taps, CI pins and the governed blocks in each moved repository.
- Archiving prototypes discards their momentum; their useful parts must be moved before archiving.

## Owner direction, 2026-11-07

The owner answered the four questions this record first left open. The record stays Proposed until it is accepted in its discussion.

- **agent-watchtower** is a standalone security product on top of the platform. It consumes `hq-v1` read-only and holds no control authority (DRIFT-005).
- **agent-bot-souls** keeps its name, under the naming rule in decision 5.
- **soul-adapters** stays separate, as recommended. Adapters follow each harness vendor's release cycle and are qualified one by one. Keeping them out of the Soul runtime keeps vendor names out of it, and lets third parties add an adapter without touching it. Its contract moves into soul-contracts.
- **GeniusBar** is a code name. DudlesBar is not adopted, and a product name is chosen before any public release (DRIFT-006, RISK-010).
- **Licensing** is MIT for the platform, as decision 6 records.

## Alternatives considered

- **One monorepository.** Simplest to keep consistent, but it erases the trust-domain boundary between code that holds authority (HQ, admin sandbox, identity service) and code that must not (Soul internals). Review and signing rules could no longer differ by trust domain.
- **Keep every existing repository.** No migration cost, but it keeps three homes for GitHub identity and two headquarters, which is where the drift came from.
