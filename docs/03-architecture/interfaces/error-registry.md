---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-05
Normative-Source: true-line/soul-contracts error registry
---

# Error registry

All error codes live in **one place**: the `true-line/soul-contracts`
error registry. **Codes are added only there, before any implementation
emits them** ([repository plan §3.1](../../papers/repository-plan-2026-10-24.md#1-repository-map)).
The registry holds a description and a retryable flag for each of the
24 codes.

> **Normative source:** the registry file in `soul-contracts`. This page
> lists the codes that documentation elsewhere relies on; regenerate from
> the registry at build time rather than editing here.

## Codes cited in docs and tests

| Code | Meaning | Retryable | Raised by | See |
|---|---|---|---|---|
| `destination_denied` | grant/destination check failed | no | broker | §4, §7, [grants](../../user-guide/how-to/grants-and-approvals.md) |
| `grant_revoked` | authority withdrawn | no | broker | §4, §7 |
| `budget_exhausted` | ceiling hit | no (operator re-grants) | broker | §8, [budgets](../../user-guide/how-to/budgets-and-costs.md) |
| `render_failed` | render plugin failed; **names the class** | depends on class | soul build | §10, [render plugins](../../user-guide/adapters/render-plugins.md) |
| `eval_coverage_missing` | candidate accepted without eval coverage | no | eval gate | §10, T27 |
| revision conflict | concurrent writers on a task | retry with fresh revision | task CAS | [state machine](task-state-machine.md) |
| version mismatch | protocol version unsupported | no | frame check | T14, [wire/v1](wire-v1.md) |

Every error carries a **correlation ID** (Appendix A); test results name
revision, policy digest, dependency versions, and profile (§14).

## Governance

1. Proposing a code: PR against `soul-contracts` error registry (with
   fixtures where the code guards a schema rule).
2. A PR adding a test updates Appendix D's traceability matrix **in the
   same change**.
3. Implementation repos emit codes only after the registry lands them.
