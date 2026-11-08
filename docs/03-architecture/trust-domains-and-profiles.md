---
Status: Draft
Doc-Type: explanation
Owner: platform-maintainer
Last-Reviewed: 2026-11-07
Sources: S6 §4; S8; agent-bot-hq D4
---

# Trust domains and enforcement profiles

Why "protected" and "cooperative" are not the same feature with different
marketing — they are different guarantees, and every receipt says which
one you got.

## The core rule

**Access is enforced by the host**, because harness and agent shell may
share a trust domain. HQ is the enforcement point: a trusted supervisor
admits runtimes; a broker mediates protected operations outside the
agent shell's trust domain. If containment cannot be guaranteed, the Soul
**runs unenforced and says so** — unenforceable profiles are refused or
reported, never silently downgraded.

## Where host-side secrets live

HQ and the admin sandbox are separate trust domains on the same host
(agent-bot-hq D4). HQ (agent-bot-hq) holds the device key and
short-lived credentials in memory only. The admin sandbox
(agent-bot-machine) guards host-side credentials at rest and the signed
policy HQ enforces, installs only signed catalog items, and verifies owner
presence before a policy write. A compromised HQ process therefore cannot
rewrite its own policy. The [repository catalog](repository-catalog.md)
records which repository owns each half.

## What "protected" buys

Under the protected profile (Linux reference host), every protected
operation is brokered *and* containment is enforced:

- HQ-controlled launch of every member runtime
- per-member principals
- protected connection binding
- caller-bound handles
- private member state (state redirection into the member's home)

Proven by the hostile-member suite: T01, T02, T03, T21 (Stage 2a exit).

## What "cooperative" honestly means

On macOS today, members **share a trust domain**. Every feature still
works — tasks, receipts, brokered inference, budgets, recovery — but a
prompt-injected specialist could read the lead's files or reach a
provider directly. Cooperative is *reported*: every receipt and the
console say "cooperative" (R8, T21), and any protected claim is refused.

## Protected vs cooperative

| | Protected (Linux) | Cooperative (macOS) |
|---|---|---|
| Feature set | full | full |
| Broker receipts | yes | yes |
| Hostile-member containment | **assured** (enforced) | **not assured** |
| Egress control | brokered | cooperative |
| Label on receipts/console | `protected` | `cooperative` |
| Planned protected candidate | shipped first | per-member profile is Stage 4 |

## Practical rules for operators

1. Treat all members on a cooperative host as **one trust domain**.
2. Give the Soul only credentials you would give its **least-trusted
   harness**.
3. Use a Linux host or VM for protected work; receipts confirm the
   profile in force on every operation.

## Why receipts must label the profile

Attribution (S6 §7) records the adapter route and profile per operation. The
"enforced vs reported" distinction is the difference between an audit
trail and a story. Windows support is later (S6 §16); the profile table is
maintained in [support](../09-operations/support.md#host-support-matrix).

## Deep dives

- S6 §4 (authority and enforcement profiles)
- Hostile-member suite and what it proves:
  [release conformance](../08-release/release-conformance-report.md#conformance-suite-t01-t30)
- Profile differences for daily work:
  [Operator Questions → Getting started](../papers/operator-questions-2026-10-29.md#getting-started)
