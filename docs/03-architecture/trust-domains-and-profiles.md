---
Status: Draft
Doc-Type: explanation
Owner: platform-maintainer
Last-Reviewed: 2026-11-26
Sources: S6 §4; S8; agent-bot-hq D4
---

# Trust domains and enforcement profiles

Why "protected" and "cooperative" are not the same feature with different
marketing — they are different guarantees, and every receipt says which
one you got.

## The core rule

**Access is enforced by the host**, because harness and agent shell may
share a trust domain. HQ admits a managed Soul through its runner. Host containment and the broker
for protected effects operate outside the agent shell's trust domain. Agent
networking and communications policy are outside HQ's control. The existing
protected broker layout requires [reconciliation](../00-governance/drift-register.md#drift-028-soul-traffic-and-the-hq-service-account). If containment cannot be guaranteed, the Soul
**runs unenforced and says so** — unenforceable profiles are refused or
reported, never silently downgraded.

## Where host-side secrets live

HQ and the admin sandbox are separate trust domains. HQ requests privileged key and resource operations over the signed local channel. Machine enforces policy and performs those operations in the secure administrative account, including on cooperative hosts and hosts without a dedicated HQ account. See [administrative custody and change control](../04-decisions/PDR-0091-host-privileged-custody.md). The sole exception is [standalone Secure Enclave signing](../04-decisions/PDR-0093-standalone-hq-secure-enclave-signing.md).

## What "protected" buys

Under a qualified protected profile, every protected
operation is brokered *and* containment is enforced:

- HQ-authorized Soul start and supervised harness launch in separate runtime accounts
- per-member principals
- protected connection binding
- caller-bound handles
- private member state (state redirection into the member's home)

PDR-0053 makes the OS account unit one account per harness credential,
shared by the agents of every Soul that uses that harness, not one per
member. How per-member principals and private state are provided under
it, and whether a shared harness account can earn `protected`, are
unspecified.

Stage 2a requires protected T01–T03 on the declared macOS pilot host plus the cooperative T21 refusal check. The [roadmap](../10-program/roadmap.md#delayed-stage) tracks the installed Agent Comms evidence for those gates.

## What "cooperative" honestly means

Under the cooperative profile, agents **share a trust domain**. Every feature still
works — tasks, receipts, model calls through each harness’s provider, budgets, recovery — but a
prompt-injected specialist could read the lead's files or reach a
provider directly. Cooperative is *reported*: every receipt and the
console say "cooperative" (R8, T21), and any protected claim is refused.

## Protected vs cooperative

| | Qualified protected host | Cooperative host |
|---|---|---|
| Feature set | full | full |
| Broker receipts | yes | yes |
| Hostile-member containment | **assured** (enforced) | **not assured** |
| Egress control | brokered | cooperative |
| Label on receipts/console | `protected` | `cooperative` |

## Practical rules for operators

1. Treat all agents on a cooperative host as **one trust domain**.
2. Give the Soul only credentials you would give its **least-trusted
   harness**.
3. Use a host qualified for protected work. Check the effective profile on each receipt.

## Why receipts must label the profile

Attribution (S6 §7) records the adapter route and profile per operation. The
"enforced vs reported" distinction is the difference between an audit
trail and a story. The host qualification table is
maintained in [support](../09-operations/support.md#host-support-matrix).

## Deep dives

- S6 §4 (authority and enforcement profiles)
- Hostile-member suite and what it proves:
  [release conformance](../08-release/release-conformance-report.md#conformance-suite-t01-t30)
- Profile differences for daily work:
  [Operator Questions → Getting started](../papers/operator-questions-2026-10-29.md#getting-started)
