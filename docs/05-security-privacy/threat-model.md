---
Status: Draft
Doc-Type: security
Owner: security-reviewer
Last-Reviewed: 2026-11-05
Scope: Soul Agent Platform, draft 0.4 surface
---

# Threat model

The enterprise-facing summary of what the platform defends, what it
honestly cannot, and which tests prove each control.

## Trust domains

| Domain | Members | Boundary |
|---|---|---|
| HQ | managed-machine daemon, key store, authority DB, broker | outside the agent shell — the enforcement point (§4) |
| Soul shell | entry point, agent-comms client, notes | routes and coordinates; **never holds keys or enforces grants** |
| Member (runtime) | one harness instance | protected profile: isolated principal + private state; cooperative profile: shares one domain with its peers |
| Remote tiers | identity service, relays, web console | outer frames only; no launch/wake/owner/credential authority (agent-comms ADR-0028) |

## Assets

| Asset | Location | Exposure if compromised |
|---|---|---|
| Provider keys, GitHub App key | HQ key store | full account access — hence T02 boundary |
| Grants/authority DB | HQ | attacker gains standing authority |
| Member state (homes) | package `home/<member>/` | memory poisoning, cross-member reads on cooperative |
| `.soul` package | portable | tampering → hostile instructions on import |
| Wire messages | in transit | relay sees outer frame only; content sealed |

## Threats and controls

| # | Threat | Interface | Control | Proven by |
|---|---|---|---|---|
| 1 | Prompt-injected member reads lead's files | member↔workspace | per-member principals, mediated views (protected only); declared cooperative on macOS | T21, R8 |
| 2 | Member reaches provider directly | egress | brokered inference; allowlist + narrow API | §4, receipts |
| 3 | Secret leaks into harness-readable files | Equip | references, never secrets; `hq audit secrets` scan | T02 |
| 4 | Approval tampering | owner approvals | HQ-signed, digest-bound; edit invalidates | T24 |
| 5 | Malicious/compromised package | import | manifest digests, traversal/symlink/expansion checks, cycles refused | T16 (§11) |
| 6 | Blind replay of an unknown effect | reconciliation | broker lookup before any resubmission | T06 (§7) |
| 7 | Relay content inspection | wire | sealed envelopes; outer frame only | §6, crypto profile (open) |
| 8 | Stale/forged frames | wire | expiry, epoch hint, message-ID dedup, required capabilities | wire fixtures, T12/T13 |
| 9 | Version downgrade attack | protocols | version negotiation refusal | T14 |
| 10 | Unauthorized local control | HQ socket | access-controlled socket, owner-session stamping on every record | §4 |
| 11 | Rogue installer item | agent-machine | signed catalog only; never root | architecture, catalog signing |
| 12 | Candidate smuggling (eval bypass) | dreams | eval-coverage gate, guardrail disable, partial acceptance disallowed | T27, T28 |

## Residual risks (accepted, stated)

- **Cooperative profile:** containment not assured — reported, not
  enforced ([profiles](../03-architecture/trust-domains-and-profiles.md))
- **Relay metadata:** timing/size observable by relays (§6)
- **Short-lived-token route:** provider key reaches harness in that
  exception; labeled in every receipt (§4)
- **Unmanaged Souls:** observability at best; no general context
  feedback mechanism yet (open problem, Oct 29)

## Review cadence

Re-run per stage exit and per adapter qualification. Record in a
[security review](key-boundaries.md#what-a-reviewer-should-ask-for) built on the
security-review template with SoulLock
digests of the reviewed build. Findings table lives in the review doc;
this page links them.
