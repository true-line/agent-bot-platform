---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: collect diagnostics

What to gather when setup, admission, rendering, or an evaluation fails —
for yourself or for a support bundle.

## One command

```bash
hq diag bundle <soul>
```

Collects (proposed; each item is individually specified):

- the admission result
- profile in force
- `SoulLock.json` digests
- adapter manifests
- the render log — including any `render_failed` with its named class (§10)
- the evaluation plan and cell summaries
- the last 100 receipts, **content redacted** (§12)
- an OTLP span export (OpenTelemetry GenAI traces, §12)

**Never member homes or workspaces.** Diagnostics are content-free (§12).

## Reading failures in place

| Failure | First evidence | Specified by |
|---|---|---|
| Setup/prereqs | prerequisite report: missing account, toolchain, sign-in | §8 |
| Admission | admission result: profile, digest, refusal code | §5, Appendix A |
| Render | render log, `render_failed` naming the class | §10 |
| Evaluation | eval plan + cell summaries, `eval_coverage_missing` | §9, §10, T27 |
| Runtime errors | typed error code + correlation ID on every error | Appendix A |

Every error carries a **correlation ID** (Appendix A); test results name
revision, policy digest, dependency versions, and profile (§14).

## Telemetry baseline

Available signals (§12): error codes, task and operation IDs, queue depth,
lease age, adapter latency, budget use, recovery events, OTel GenAI
traces. Trace export **excludes content**.

## When attaching to a report

Attach the `hq diag bundle` output plus:

- the task/operation ID and correlation ID
- the receipt timeline for the failing window
- the Soul revision digest and adapter versions

See also: [HQ restart runbook](../../09-operations/runbooks/hq-restart.md) ·
[release conformance report](../../08-release/release-conformance-report.md)
(ask for T02/T21 results for your host).
