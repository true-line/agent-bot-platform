---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-08
Date: 2026-11-08
Discussion: https://github.com/true-line/agent-bot-platform/discussions/40
Affects-Repos: [agent-bot-hq, agent-bot-comms, agent-bot-identity, agent-bot-souls]
Affects: [topology]
---

# PDR-0040 Repository renames and transfers to true-line

On 2026-11-08 the owner made three moves:

| Before | After | Kind |
| --- | --- | --- |
| true-line/agent-bot-daemon | true-line/agent-bot-hq | rename |
| qwts/agent-comms | true-line/agent-bot-comms | transfer and rename |
| qwts/agent-bot-identity | true-line/agent-bot-identity | transfer |

Under PDR-0037 the executables follow the repository names: `agent-bot-hq`, `agent-bot-comms` and `agent-bot-identity`. Seam, requirement and test IDs don't change.

## Context

- The plan, the catalog and the code call agent-bot-daemon's component HQ. "Daemon" already names the legacy per-account daemon (`agent-bot daemon`) that HQ replaces, so under PDR-0037 `agent-bot daemon` would have been ambiguous.
- agent-comms kept its name under PDR-0002 point 5, which named it as an exception. With executables named for repositories, the `agent-bot-` prefix makes it `agent-bot-comms`, matching the rest of the set.
- The registry already planned the transfers of agent-comms and agent-bot-identity to true-line. Both repositories were public before and remain public.

## Decision

1. **The three moves above stand.** GitHub redirects the old URLs, remotes and archive downloads.
   - On 2026-11-08 the agent-bot-identity v0.15.17 archive kept its sha256 under the redirect.
   - The agent-comms formula installs from git, so the Homebrew taps keep working unchanged.
   - No repository may be created again under an old name, because that would break its redirect.
2. **The registry keeps the old names.** Entries carry `former-names` (`agent-bot-daemon`, `agent-comms`). `tools/check_platform.py` accepts a former name wherever a repository qualifies a label or an ADR, so records written before the moves stay valid as written.
3. **Accepted records keep their text.**
   - Their `Affects-Repos` frontmatter names the current repositories.
   - The drift register and the decision log are not rewritten.
   - The registry, the generated pages and current docs use the new names.
4. **The Homebrew taps stay in qwts for now.** Moving a tap is a separate change, made only when it breaks no install (PDR-0002).

## Acceptance

The owner made the three moves on 2026-11-08 and listed them in a working session. The answer in [discussion #40](https://github.com/true-line/agent-bot-platform/discussions/40) is for the owner to mark.

## Consequences

- **agent-bot-hq:** its README, AGENTS.md and plan use the new name, and its executable is `agent-bot-hq`.
- **agent-bot-comms:** its README, AGENTS.md, CI and docs-gov issue pattern use true-line/agent-bot-comms, and its executable becomes `agent-bot-comms`. Its LICENSE ("All rights reserved") still conflicts with the platform's MIT and needs the owner's decision.
- **agent-bot-identity:** links use true-line/agent-bot-identity.
- **Platform:** this PR covers the registry, the checker, the generated pages and current docs.

## Alternatives considered

- **Keep the old names and orgs.** This keeps the clash with the legacy daemon and an exception to the `agent-bot-` set. Two platform repositories would also stay outside the org that governs them.
