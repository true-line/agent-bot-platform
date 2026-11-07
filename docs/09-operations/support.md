---
Status: Draft
Doc-Type: reference
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Scope: support model, hosts, escalation
---

# Support model

What support owes operators and what operators owe support.

## Host support matrix

| Host | Profile | Status |
|---|---|---|
| Linux reference host | **protected** | MVP target (§13) |
| macOS | **cooperative** | MVP target; per-member protected profile is Stage 4 |
| Windows | — | later (§16) |
| Declared reference machine | — | latency targets (§14); [UNSPECIFIED] hardware spec for local models |

Workflow differences: none in features; containment differs —
see [profiles](../03-architecture/trust-domains-and-profiles.md).

## What support asks you to attach

1. `hq diag bundle <soul>` — admission result, profile, SoulLock digests,
   adapter manifests, render log, eval plan, last 100 receipts (content
   redacted), OTLP export ([how-to](../user-guide/how-to/diagnostics.md))
2. Task/operation IDs and correlation IDs (every error carries one,
   Appendix A)
3. The failing window's receipt timeline
4. Revision digest + adapter versions (test results name revision,
   policy digest, dependency versions, profile — §14)

**Never send** member homes or workspaces; bundles are content-free by
construction (§12).

## Triage paths

| Class | First responder | Runbook |
|---|---|---|
| Unknown external outcome | operator, then support | [reconcile](runbooks/reconcile-unknown-outcome.md) |
| Crash loop / quarantine | support | [crash loop](runbooks/harness-crash-loop.md) |
| HQ down | on-call | [HQ restart](runbooks/hq-restart.md) |
| Suspected containment failure | **security immediately** | [threat model](../05-security-privacy/threat-model.md), revoke grants, capture bundle |
| Import/render failures | support + adapter owner | [render plugins](../user-guide/adapters/render-plugins.md) |

## Service levels (proposed)

- Stage 3 pilot: best-effort, business hours, one named contact per pilot
- GA: [UNSPECIFIED] — propose SLAs with the operating model paper (§15)

## Known-limitation disclosures

Support must state these up front, not on request:

- Cooperative macOS containment is **reported, not enforced**
- Federation relay runtime **not authorized yet** (agent-comms ADR-0028 accepted,
  runtime pending)
- Unmanaged Souls: **observability at best**; no general context
  feedback mechanism yet
