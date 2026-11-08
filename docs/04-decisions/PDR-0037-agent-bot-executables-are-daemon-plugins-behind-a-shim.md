---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-08
Date: 2026-11-08
Accepted: 2026-11-08
Discussion: https://github.com/true-line/agent-bot-platform/discussions/37
Affects-Repos: [agent-bot-identity, agent-bot-hq, agent-bot-souls, agent-comms]
Affects: [identity-cli, hq-plugin-contract]
---

# PDR-0037 agent-bot executables are daemon plugins behind a shim

Each component ships its own `agent-bot-*` executable. `agent-bot` is a light shim CLI that hands `agent-bot <name> …` to `agent-bot-<name>`. When agent-bot-daemon is installed, every `agent-bot-*` package is a plugin to it. This is the owner's existing design. The platform records did not state it, and the agent-bot-daemon plan read them as one CLI owned by agent-bot-identity.

## Context

- The [repository catalog](../03-architecture/repository-catalog.md) gives agent-bot-identity the "agent-bot CLI", agent-bot-daemon the "HQ CLI", and agent-bot-souls `agent-bot soul run` and `soul chat`. The agent-bot-daemon plan (§7) calls the owner's client "the `agent-bot` CLI". Read together, these records describe one binary owned by a repository that, after plan §9 row 25, no longer holds most of its commands.
- The owner confirmed on 2026-11-08 that this was never the design: the binaries are their own, and `agent-bot` is a shim over them.

## Decision

1. **One executable per component, named for it.**
   - `agent-bot-daemon` comes from agent-bot-daemon.
   - `agent-bot-comms` comes from agent-comms.
   - `agent-bot-identity` comes from agent-bot-identity.
   - `agent-bot-souls` comes from agent-bot-souls.
   - Each future component is `agent-bot-<name>`.

   Each executable runs on its own, without the daemon. A repository rename renames its executable by the same rule.
2. **`agent-bot` is a shim CLI.** `agent-bot <name> …` execs `agent-bot-<name>` with the remaining arguments, inherits stdio, and returns its exit code. It has no options, no config and no authority of its own.
3. **With agent-bot-daemon installed, every `agent-bot-*` package is a daemon plugin.**
   - It registers through `hq-plugin-contract`, in the trust domain its catalog entry gives it. Examples: comms registers its broker mode; identity registers member surfaces (PDR-0027); souls registers the Soul runtime's HQ side.
   - The shim resolves `<name>` from the daemon's installed, pinned plugins. It never runs an `agent-bot-<name>` it merely finds on PATH.
   - Without the daemon, it runs only the `agent-bot-*` executables installed beside it.
4. **Single homes.**
   - The shim's resolution rules are documented in the `identity-cli` contract home, which is agent-bot-identity's README.
   - The plugin side of each package is documented in agent-bot-daemon's `hq-plugin-contract`.
   - Each executable's commands are documented in its own repository.

## Acceptance

The owner gave this design on 2026-11-08 in a working session and marked the answer in [discussion #37](https://github.com/true-line/agent-bot-platform/discussions/37) that day.

## Consequences

- **agent-bot-identity:** ships the `agent-bot` shim and moves today's commands behind `agent-bot-identity`. Golden tests cover:
  - resolution through the daemon's pins;
  - running without the daemon;
  - the refused PATH lookup;
  - the exit code;
  - the message when a target is missing.
- **agent-bot-daemon:**
  - Ships `agent-bot-daemon`; today that is `node hq/main.mjs`.
  - Gives the shim a read of its installed, pinned plugins.
  - Its plan's §7 and §9 rows 14, 21 and 25 name the executables.
- **agent-comms:** ships `agent-bot-comms`. Its broker mode is the row 13b plugin.
- **agent-bot-souls:** ships `agent-bot-souls`, reached as `agent-bot souls …`. §9 row 14 builds it.
- **Platform:** the catalog entries for the four repositories and the `identity-cli` seam cite this record.

## Alternatives considered

- **One executable in agent-bot-daemon**, loading the other repositories' commands. The other repositories could not run without the daemon, and the daemon would carry their command code.
- **One executable in agent-bot-identity**, as the records read. A repository chartered inside the Soul would front owner and HQ commands it does not own.
