---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-08
Date: 2026-11-08
Accepted: 2026-11-08
Discussion: https://github.com/true-line/agent-bot-platform/discussions/27
Affects-Repos: [agent-bot-daemon, agent-bot-identity]
Affects: [hq-plugin-contract, trust-model, topology]
---

# PDR-0027 HQ identity authority lives in agent-bot-daemon

All of HQ's identity authority is a built-in part of HQ in agent-bot-daemon: enrollment, the identity-service link, the device key and signer, credential references, grants and approvals. agent-bot-identity's `hq-plugin-contract` plugin registers member surfaces only (MCP tools, CLI commands, hook handlers), and they resolve to broker queries. Each repository stays in one trust domain, and code that holds authority is reviewed and signed under HQ's rules in one place. This closes DRIFT-016.

## Context

- The [repository catalog](../03-architecture/repository-catalog.md) puts agent-bot-identity inside the Soul, untrusted for authority, and says it must not own HQ authority, keyd or approvals. agent-bot-daemon is the one local authority outside every Soul, and it holds the device key and short-lived credentials in memory.
- agent-bot-identity also consumes `hq-plugin-contract` ([seams](../03-architecture/seams.md)). The catalog did not say whether that plugin may carry HQ-side code. agent-bot-daemon's plan had made agent-bot-identity HQ's identity plugin, holding the signer, grants, approvals and credential references (DRIFT-016).
- PDR-0002 criterion C1 keeps each repository in one trust domain.
- The plugin SDK (agent-bot-daemon#78) and agent-bot-identity's Stage 0 cycle-breaking both needed the answer before building.

## Decision

1. **HQ identity authority is built into HQ.** Enrollment, the identity-service link, the device key and signer, credential references, grants and approvals are part of HQ core in agent-bot-daemon. They are not a plugin, and no other repository ships them.
2. **agent-bot-identity's plugin registers member surfaces only.** Through `hq-plugin-contract` it registers MCP tools, CLI commands and hook handlers that members run in the Soul. Each one resolves to a broker query and never to direct authority.
3. **The catalog says so.** agent-bot-identity's catalog entry names the member-surface scope, and the `hq-plugin-contract` seam note cites this record.

## Acceptance

The owner accepted option 1 on 2026-11-08, in the marked answer to [discussion #27](https://github.com/true-line/agent-bot-platform/discussions/27), and asked that it be recorded as PDR-0027.

## Consequences

- **agent-bot-daemon:** owns plan section 9 PRs 15 and 18 and the HQ half of today's identity module, as its adopted plan already says. Its plugin host bootstraps identity as part of HQ core rather than as a plugin, and its plan drops the open question it recorded under DRIFT-016.
- **agent-bot-identity:** its `hq-plugin-contract` consumption covers member surfaces only. Its HQ authority moves out (agent-bot-daemon plan section 9 PR 25).
- **Platform:** the agent-bot-identity catalog entry and the `hq-plugin-contract` seam note cite this record, and DRIFT-016 is resolved.

## Alternatives considered

- **agent-bot-identity ships an HQ-side, authority-bearing plugin.** A repository chartered as untrusted for authority would hold authority code, splitting trust domains inside one repository. It would need a catalog change and per-domain review and signing rules, the opposite of C1.
- **Leave it unspecified.** The plugin SDK and agent-bot-identity's Stage 0 work would build toward the wrong shape.
