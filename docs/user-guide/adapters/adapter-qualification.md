---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: adapter-developers
---

# How to: qualify an adapter

Take a harness adapter from code to a signed qualification manifest that
operators can trust per profile.

**Model (specified, §2, §10, §12):** adapters qualify **individually**; the
compatibility matrix pins adapter versions; each release ships a signed
qualification manifest per adapter version. A qualified adapter declares
which profile it qualifies for (**protected** or **cooperative**) and
which primitive classes it can render (§10 adapter manifest).

## The qualification artifacts

1. **ACP adapter** implementing the per-harness protocol surface
   ([soul-adapters](../../papers/repository-plan-2026-10-24.md#3-plan-by-repository), WP3)
2. **Render plugin** implementing the render-plugin interface
   ([render plugins how-to](render-plugins.md))
3. **Signed qualification manifest**: version, qualified profile(s),
   renderable primitive classes
4. **Evaluation evidence**: records naming revision, harness, model,
   provider, date (§9) — a harness upgrade marks the cell *unevaluated*
   (§10)

## Passing the hostile-member suite (protected claim)

A **protected** qualification requires the adapter to honor: HQ-controlled
launch, per-member principals, protected connection binding, caller-bound
handles, and **state redirection** (member state under the member's home,
not the harness's default location). Prove it with the hostile-member
suite under the protected label (T01, T02, T03, T21; Stage 2a exit).

If your adapter can only run cooperatively, **qualify it cooperative only**.
Any protected claim is refused unless proven — and every receipt says
which profile was in force (R8, T21). Unenforceable claims are refused or
reported, never silently downgraded.

## Entry in the compatibility matrix

Pin exact adapter versions in the matrix (§12). The matrix answers "which
adapter works with which harness, on which profile, at which version".
Operators see this via `hq adapters list` (proposed shape — see
[Operator Questions](../../papers/operator-questions-2026-10-29.md#getting-started)).

## After a harness upgrade

Your previously qualified pairing becomes **unevaluated**: it warns and
keeps running; it does not block until a guardrail violation disables the
route (§9, §10). Re-render and re-evaluate to restore the green cell
(T27).

## Checklist

- [ ] ACP adapter passes conformance fixtures from `soul-contracts`
- [ ] Render plugin deterministic; renders to per-adapter digest in
      `SoulLock.json` (§10)
- [ ] Hostile-member suite green (if claiming protected)
- [ ] Qualification manifest signed; profile + primitive classes declared
- [ ] Evaluation cells recorded for every role on the target harness
- [ ] Compatibility matrix updated in the same PR
