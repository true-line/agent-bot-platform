---
Status: Draft
Doc-Type: security
Owner: security-reviewer
Last-Reviewed: YYYY-MM-DD
Scope: <seam, trust boundary or requirement under review>
---

# Security review: <scope>

<One paragraph: what was reviewed, at which commits, and the overall finding.>

> Use this template only when the review changes a trust boundary, a seam or
> a requirement. A review of one component lives in that component.

## Scope and trust boundaries

Components and the trust domain each runs in; what is protected (enforced by HQ) and what is cooperative.

## Assets

| Asset | Held by | Exposure if compromised |
|---|---|---|

## Threats

Per interface: attack, existing control, residual risk.

## Controls relied on

Each threat mapped to the T-series tests that prove its control.

## Data handling

What leaves the host per route, disclosure labels, retention and deletion.

## Findings

| Finding | Severity | Remediation | Repository | Tracking issue |
|---|---|---|---|---|

## Sign-off

Reviewer role, date, and the commits or SoulLock digests reviewed.
