---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-08
Date: 2026-11-08
Discussion: https://github.com/true-line/agent-bot-platform/discussions/40
Affects-Repos: [agent-bot-hq, agent-bot-identity, agent-comms, agent-bot-souls]
Affects: [topology]
---

# PDR-0040 Rename agent-bot-daemon to agent-bot-hq

The repository that builds HQ is true-line/agent-bot-hq, formerly true-line/agent-bot-daemon. Its executable is `agent-bot-hq` under PDR-0037, reached as `agent-bot hq`. Seam, requirement and test IDs don't change.

## Context

- The plan, the catalog and the code all call the component HQ.
- "Daemon" already names the legacy per-account daemon (`agent-bot daemon` in agent-bot-identity), which HQ replaces.
- Under PDR-0037 an executable is named for its repository, so `agent-bot daemon` would have been ambiguous between the two.
- Nothing had shipped under the old name. The new name keeps the `agent-bot-` prefix (PDR-0002 point 5).

## Decision

1. **The repository is true-line/agent-bot-hq.** The owner renamed it on 2026-11-08. GitHub redirects the old URLs and remotes.
2. **The registry entry keeps the old name** as `former-names: [agent-bot-daemon]`. `tools/check_platform.py` accepts a former name wherever a repository qualifies a label or an ADR, so records written before the rename stay valid as written.
3. **Accepted records keep their text.** Their `Affects-Repos` frontmatter names agent-bot-hq. The drift register and the decision log are not rewritten. The registry, the generated pages and current docs use the new name.
4. **IDs are stable.** `hq-v1`, `hq-plugin-contract`, `task-v1` and `observation-v1` keep their IDs, and agent-bot-hq is their provider.

## Acceptance

The owner renamed the repository on 2026-11-08 after the rename was recommended in a working session. The answer in [discussion #40](https://github.com/true-line/agent-bot-platform/discussions/40) is for the owner to mark.

## Consequences

- **agent-bot-hq:** update its README, AGENTS.md and plan to the new name. Its executable is `agent-bot-hq`.
- **agent-comms, agent-bot-identity, agent-bot-souls:** replace references to agent-bot-daemon in their own PRs. The redirects keep old links working meanwhile.
- **Platform:** this PR covers the registry, the checker, the generated pages and current docs.

## Alternatives considered

- **Keep agent-bot-daemon.** This keeps the clash with the legacy daemon, and the cost of renaming grows with every reference.
