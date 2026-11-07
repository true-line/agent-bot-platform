---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: adapter-developers
---

# How to: write a render plugin

Produce deterministic per-adapter renders of a `.soul` package behind the
plugin interface.

**Model (specified, §10, §11):** `soul build` renders **through the plugin
interface** (`soul-package/spec/RENDER-PLUGIN.md`), writing a
rendered-output digest per adapter into `SoulLock.json`. Rendering must be
**deterministic**: same definition digest + plugin → byte-identical
output. Failure is loud: `render_failed` naming the class (§10) — a
silent fallback is a conformance failure.

## Interface contract

Implement, per adapter:

1. **Render** — definition tree → executable tree for your harness
2. **Digest** — the rendered-output digest recorded in `SoulLock.json`
3. **Manifest declaration** — which primitive classes you can render
   (§10 adapter manifest); undeclared classes must refuse, not guess

Respect the definition-digest byte rules (§11): the manifest's own digest
field is excluded from its digest; everything else is pinned by SHA-256.

## State redirection (protected adapters only)

Under the protected profile, the plugin must honor **state redirection**:
member state lives under the member's home in the package — never in the
harness's default location (§4, Stage 2a). The first real adapter proved
this pattern; copy it
([repository plan §3](../../papers/repository-plan-2026-10-24.md#3-plan-by-repository)).

## Determinism and gating

- Render determinism is a **unit gate for Stage 1** — same input twice,
  identical bytes
- Render failures carry a class: name the cause
  (`missing_plugin`, `unsupported_primitive`, …) so operators see
  *which* class failed in the render log
  ([diagnostics](../how-to/diagnostics.md))
- An updated pin is a candidate revision: acceptance **re-renders every
  adapter** and requires a passing evaluation cell per role on that
  harness version (§10, T27)

## Vendoring rules your render depends on

Everything except the OS baseline and declared host toolchains is vendored
under `opt/`, pinned by SHA-256 in `SoulLock.json`; fetches happen at
**build time only**, never at run time (R12, §11). If your render emits
references to host toolchains (Xcode-class), declare them as host
requirements in `SoulInfo.json` — checked at activation, reported if
missing (§8, §11).

## Related

- [Package format reference](../../03-architecture/interfaces/package-format.md)
- [Adapter qualification](adapter-qualification.md)
- `true-line/soul-package` — spec/RENDER-PLUGIN.md is normative; this page
  summarizes it
