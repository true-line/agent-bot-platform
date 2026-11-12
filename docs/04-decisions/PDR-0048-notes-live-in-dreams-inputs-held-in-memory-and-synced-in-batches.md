---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-11
Date: 2026-11-11
Accepted: 2026-11-11
Discussion: https://github.com/true-line/agent-bot-platform/discussions/48
Affects-Repos: [agent-bot-hq, agent-bot-souls, soul-package, soul-contracts]
Affects: [soul-package-format, hq-v1]
---

# PDR-0048 Notes live in dreams/inputs, held in memory and synced to the Soul in batches

Ordinary notes live at `dreams/inputs/` inside the Soul. The working copy is held in memory and an append-only sync writes it to the Soul's durable storage every 30 seconds. The most important consequence: a hard crash loses at most 30 seconds of ordinary notes and nothing that another party relies on, while the disk is not written on every note.

## Context

- The sources disagreed on where ordinary notes live: the OS temp folder, a `tmp/` folder in the package, or durable inputs. S6 §10 proposes durable, access-controlled `dreams/inputs/` with batched writes, a 30 second interval, immediate flush of handoff and open-task state to `comms/`, and no shutdown nap. The [decision log](decision-log.md) lists "Notes durability" as open, needed by Stage 3.
- The owner wants notes to live in the Soul so nothing is lost, without constant small writes to the SSD.
- S6 §10 does not say how batching is achieved, so one implementation could buffer in a process and another could write every note to disk and call it a batch.

## Decision

1. **One path.** Ordinary notes are written to `dreams/inputs/` in the Soul root. No note is written to the OS temp folder. `tmp/` stays disposable scratch and is never a source for consolidation.
2. **Working copy in memory.** The directory an agent writes to is memory-backed: a tmpfs mount on Linux, a RAM disk on macOS, and an in-process write-behind buffer where neither is available (Windows, or a host where the mount fails). On every host the mount is private to the Soul with the same access control as the Soul root, and it is size-capped. Teardown leaves no copy behind: no swap pages and no RAM-disk image.
3. **Batched, append-only sync.** New notes are appended to the durable copy in the Soul's storage every 30 seconds. The sync also runs at clock-out, sleep, nap, drain, on SIGTERM, and at once when the mount reaches its cap. It never rewrites or deletes a durable note; only consolidation deletes. Because every clean stop flushes, only a hard crash can lose the batch window.
4. **Write-through for what others rely on.** Decision, commitment and handoff notes, and open-task state, are written durably to `comms/` before the write returns. They do not wait for the batch.
5. **The durable copy is the truth.** After a crash the working copy is rebuilt from the durable copy. The loss bound is 30 seconds of ordinary notes and zero write-through notes, and that bound is part of the decision: "nothing is lost" does not mean zero loss for ordinary notes. No shutdown nap is required for correctness.
6. **Consolidation.** Sleep forces a sync, reads the durable copy, writes its result and watermark transactionally, then deletes the consumed inputs from both copies (S6 §10). Forgetting stays intended.
7. **Fallback never weakens the rule.** If the memory mount cannot be created, the runtime uses the in-process buffer with the same interval and the same write-through rule. It does not fall back to direct per-note disk writes or to the OS temp folder.

## Acceptance

Option B was accepted on the owner's behalf on 2026-11-11 in the marked answer to [discussion #48](https://github.com/true-line/agent-bot-platform/discussions/48). An agent posted that answer for the owner; the owner confirms it by merging this record. The answer has four conditions: soul-contracts names the write-through kinds and tests show they survive a crash; clean stops flush; the mount stays under the Soul's access control and is torn down without a leftover copy; and batched sync keeps S6's forgetting rule. Points 2, 3, 4 and 6 carry them.

## Consequences

- **agent-bot-platform.** The decision log records "Notes durability" as decided. Still to do: tests to `registry/tests.yaml` for: a killed Soul loses no write-through note and no ordinary note older than 30 seconds; no note reaches the OS temp folder; the fallback buffer meets the same bound.
- **agent-bot-hq.** Create and tear down the memory mount when it launches and stops a Soul, private to that Soul, with a size cap and no leftover copy. Whether `hq/v1` reports the mount is unspecified here and is agent-bot-hq's to propose.
- **agent-bot-souls.** Run the sync, the write-through rule and the fallback buffer. Force a sync before clock-out, sleep, nap and drain, and on SIGTERM.
- **soul-package.** Record `dreams/inputs/` as Life data whose packaged copy is the durable, synced one. The memory mount is never packaged or transferred.
- **soul-contracts.** Name in the typed-note record which note types are write-through.

## Alternatives considered

- **Leave it open.** Implementations pick different places for notes, and crash recovery differs per harness.
- **Write every note straight to disk.** Nothing is lost, at the cost of constant small writes, which is what the owner wants to avoid.
- **OS temp folder, promoted at sleep.** Fewest writes, but a crash before sleep loses the day and private notes sit outside the Soul's access control.
- **Memory only, with a shutdown nap.** Depends on a graceful shutdown, which S6 §10 already rejects.
