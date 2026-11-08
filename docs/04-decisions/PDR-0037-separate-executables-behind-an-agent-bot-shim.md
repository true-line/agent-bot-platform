---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-08
Date: 2026-11-08
Discussion: https://github.com/true-line/agent-bot-platform/discussions/37
Affects-Repos: [agent-bot-identity, agent-bot-daemon, agent-bot-souls]
Affects: [identity-cli, hq-plugin-contract]
---

# PDR-0037 Separate executables behind an agent-bot shim

Each repository that provides commands ships its own executable. `agent-bot` is a light shim that hands each command off to one of them. No repository loads another repository's code to build the command line. Owner commands and `soul run` work without a running HQ.

## Context

- The [repository catalog](../03-architecture/repository-catalog.md) gives agent-bot-identity the "agent-bot CLI", agent-bot-daemon the "HQ CLI", and agent-bot-souls `agent-bot soul run` and `soul chat`. The agent-bot-daemon plan (§7) calls the owner's client "the `agent-bot` CLI", and its §9 row 25 removes host, Soul and comms code from agent-bot-identity. Together these leave one binary in a repository that no longer holds most of its commands.
- Commands registered through `hq-plugin-contract` reach members only through a running HQ. Owner commands must answer when HQ is down or in safe mode, and `soul run` starts before any admission, so neither can depend on HQ to be reachable.

## Decision

1. **One executable per repository.**
   - `agent-bot-hq` from agent-bot-daemon: the HQ CLI and owner commands.
   - `agent-bot-soul` from agent-bot-souls: `soul run` and `soul chat`.
   - `agent-bot-identity` from agent-bot-identity: the member tools, the fail-closed `gh`, the hooks, and today's top-level commands.
2. **`agent-bot` is a shim**, shipped by agent-bot-identity, which already owns the name.
   - It reads only the first word. `hq` goes to `agent-bot-hq` and `soul` goes to `agent-bot-soul`. Every other word goes to `agent-bot-identity`, so existing commands keep working.
   - It execs the target with the remaining arguments, inherits stdio, and returns the target's exit code. A missing target names the package to install.
   - It has no options, no config and no authority of its own.
   - Its table is fixed. It never runs an `agent-bot-<word>` it finds on PATH, so a planted executable cannot claim a command word.
3. **Single homes.** The shim's table and behavior are documented in agent-bot-identity's README, the `identity-cli` contract home. Each executable's commands are documented in its own repository.
4. **Plugin commands are unchanged.** Member commands registered with `ctx.commands.register` still resolve to broker queries (PDR-0027). They are served by `agent-bot-identity`.

## Acceptance

The owner chose option 2 on 2026-11-08 in a working session ("agent-bot should just be a light shim that calls them"). That answer is recorded in [discussion #37](https://github.com/true-line/agent-bot-platform/discussions/37) for the owner to mark.

## Consequences

- **agent-bot-identity:** ships the `agent-bot` shim and moves today's commands behind `agent-bot-identity`. The shim gets golden tests: the table, the exit code, the refused PATH lookup, and the missing-target message.
- **agent-bot-daemon:** ships `agent-bot-hq`, which today is `node hq/main.mjs`. Its plan §7 and §9 rows 21 and 25 name the executable.
- **agent-bot-souls:** ships `agent-bot-soul`. §9 row 14 builds it, reached as `agent-bot soul run`.
- **Platform:** the catalog entries for the three repositories and the `identity-cli` seam name cite this record.

## Alternatives considered

- **One executable in agent-bot-daemon** that loads pinned command modules from the other repositories. A dispatcher in one repository would load another's code, and the souls and identity commands would wait on daemon releases.
- **Keep agent-bot-identity as owner of every command.** This keeps the mismatch in the context, and it needs another path for commands that cannot go through HQ.
