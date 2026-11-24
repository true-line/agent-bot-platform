---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Date: 2026-11-23
Last-Reviewed: 2026-11-24
Discussion: https://github.com/true-line/agent-bot-platform/discussions/124
Amends: PDR-0102
Affects-Repos: [agent-bot-platform, agent-bot-machine, agent-bot-souls, soul-contracts, soul-conformance]
Affects: [R8, trust-model, quality-bar]
---

# PDR-0124 Bound the stock Claude external input exception

The owner approved one exact-file exception for Stage 2a qualification of
the selected stock Claude CLI. The general external file limit stays at
256 MiB; the exception cannot grant a protected launch or a test pass.
[Recorded owner decision](https://github.com/true-line/agent-bot-platform/discussions/124).

## Context

The selected stock Claude executable is 354,630,016 bytes, above the
256 MiB external launch-input limit in the
[controlled measurement rule](../03-architecture/interfaces/stage2a-measurement.md).
Increasing the general limit would admit unrelated oversized code. The
owner selected a smaller qualification-only ceiling bound to the exact
file rather than the discussion's broader 512 MiB option.

## Decision

1. For one exact owner-reviewed qualification plan, the external regular
   file at relative installed path `runtime/bin/claude` may use a 384 MiB
   per-file ceiling only when its mode is `0550`, size is exactly
   354,630,016 bytes and SHA-256 is
   `e85547190ef8cd983033ba61b17194045a6fea00035da349efeabed86badacc9`.
   Every other external file remains limited to 256 MiB. The external array
   stays at most 64 files and 1 GiB aggregate. Frozen `Contents/` keeps its
   separate 512-entry, 256 MiB per-file and 1 GiB bounds.
2. The reviewed plan selects the complete installed path, size, mode and
   hash inventory and the command and ordered arguments. The exact CLI row
   joins the frozen stock manifest declaration and selected R adapter
   inventory. Machine and Souls enforce the same tuple; Machine remeasures
   the installed bytes through its no-follow custody path before each
   one-use start. A changed byte, path, mode, size, command, inventory or
   plan requires fresh owner review. No other file inherits the ceiling.
3. The rule takes effect only after matching Contracts, Machine and Souls
   implementations are released and the exact installed inventory is
   verified. It does not authorize ordinary protected work, change
   PDR-0091 custody, or certify T01–T03/T21. A one-use reservation and
   completed host-signed physical evidence remain required.

## Consequences

- The [controlled measurement interface](../03-architecture/interfaces/stage2a-measurement.md)
  records the narrow successor while retaining the current gate until
  matching releases and installed proof exist.
- agent-bot-machine must reject any broader oversized R inventory or
  external launch-input row, including changed tuple fields, and preserve
  descriptor-based remeasurement and the existing count and total bounds.
- agent-bot-souls must enforce the exact external tuple without widening
  frozen definition limits. soul-contracts and soul-conformance must carry
  compatible schema and refusal fixtures for the installed closure.

## Alternatives considered

- Keep the 256 MiB external ceiling with no exception: the selected stock
  distribution would refuse qualification.
- Permit 512 MiB for any reviewed external file: this is broader than the
  selected executable needs and would weaken refusal for unrelated files.
