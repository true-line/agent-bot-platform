---
Status: Proposed
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-16
Date: 2026-11-16
Discussion: https://github.com/true-line/agent-bot-platform/discussions/75
Affects-Repos: [soul-contracts, soul-conformance, agent-bot-hq, agent-bot-comms, agent-bot-souls]
Affects: [hq-v1, wire-v1, conformance-report, R7, R8, quality-bar]
---

# PDR-0075 T14 uses supported-major inventory and asserted profile evidence

This proposal would make T14's previous-major coverage depend on an explicit,
reviewed inventory of supported protocol majors, and count only semantic checks
actually asserted under the reported enforcement profile. It is **not accepted**:
[Discussion #75](https://github.com/true-line/agent-bot-platform/discussions/75)
and [issue #74](https://github.com/true-line/agent-bot-platform/issues/74) track
review. Overall T14 acceptance and Stage 0 exit remain blocked pending the
owner's decision and the required evidence; this proposal grants no exception.

## Context

- Approved [R7](../02-requirements/product-requirements.md#r7-contracts-first-n-and-n-1)
  requires the current and previous supported major contract versions with
  explicit capability negotiation. [T14](../07-verification/conformance-catalog.md)
  specifies N-1 and unknown-required-capability stimuli. Neither defines the
  evidence needed when a protocol has only its first supported major.
- Package releases such as soul-contracts v0.4.1 and v0.5.0 are not protocol
  majors. Comparing those packages does not prove previous-major interoperability
  for a family that still uses protocol major 1.
- The [soul-conformance T14 stub](https://github.com/true-line/soul-conformance/blob/d645818961371dab50c21833c3ca474bed6264d6/suites/T14-version-mismatch/README.md)
  says protected is required and cooperative may report unenforced. Its
  [suite overview](https://github.com/true-line/soul-conformance/blob/d645818961371dab50c21833c3ca474bed6264d6/suites/TESTS.md)
  says unenforced can pass a weaker profile. This does not establish T14's
  required observation that supported versions work and unsupported semantics
  fail explicitly. [R8](../02-requirements/product-requirements.md#r8-honest-profiles)
  also requires actual guarantees to be reported honestly.
- [DRIFT-021](../00-governance/drift-register.md#drift-021-t14-previous-major-and-profile-evidence)
  records the unresolved interpretation and component-stub conflict.
  [soul-conformance #2](https://github.com/true-line/soul-conformance/issues/2)
  tracks the executable suite; passing component checks do not settle this
  platform decision.

## Decision

The following rules are proposed, not active policy:

1. **Inventory supported protocol majors explicitly.** A reviewed platform
   registry would identify each tested protocol family, its current supported
   major, its previous supported major when one exists, and verifiable source
   evidence. A first-major family whose only supported major is 1 may record
   that no previous supported major exists only with reviewed evidence. A
   missing, stale or unverifiable inventory blocks qualification; an absent
   entry is not evidence that N-1 is inapplicable.
2. **Exercise the previous major when it exists.** T14 must execute actual
   interoperability against the declared previous supported major. It may not
   substitute package releases, fabricated protocol major 0, or an unsupported
   version refusal for a supported previous-major success. Where the reviewed
   inventory establishes no previous supported major, report that specific
   coverage as inapplicable with its evidence, never as an executed pass.
3. **Always assert the current semantic checks.** Supported-current-major
   positive behavior, unsupported-version refusal and unknown-required-capability
   refusal remain mandatory, including for a first-major family. Record each
   boundary exercised and its actual result; schema validity alone does not
   establish the requested effect or refusal.
4. **Qualify only the guarantees tested.** T14 semantic checks may run under an
   actual cooperative enforcement profile and count only when their assertions
   pass. Unenforced behavior is not a pass. Report the actual profile and
   limitations; do not derive a protected claim from these checks. T01, T02,
   T03 and T21 retain their separate containment and profile-honesty gates.
   This does not resolve the terminology conflict in DRIFT-018 or amend
   [PDR-0055](PDR-0055-a-soul-is-managed-when-hq-starts-it.md).
5. **Keep authority and evidence in their homes.** Platform owns the acceptance
   rule and supported-major inventory; soul-contracts owns wire versions and
   fixtures; soul-conformance owns executable assertions and reports. Consumers
   read platform main under
   [PDR-0020](PDR-0020-components-read-the-platform-at-main.md) and record the
   exact main SHA checked. Missing or unaccepted policy cannot be replaced by
   a local override or a passing component run.

## Consequences

- **Platform, after acceptance:** add the reviewed compatibility inventory in
  `registry/`, reconcile T14 and related release guidance with this decision,
  and regenerate affected pages. This proposal does not add that inventory or
  change R7, T14's current registry status, or the Stage 0 gate.
- **soul-contracts:** provide source evidence for supported protocol majors and
  their fixtures; package version changes do not invent another protocol major.
- **soul-conformance:** replace the conflicting T14 stub guidance, verify the
  reviewed inventory and report asserted outcomes separately from blocked or
  inapplicable coverage. Until acceptance and adoption, retain the overall
  T14 result as blocked even if individual checks pass.
- **HQ, comms and Souls:** expose their supported-version behavior to the
  independent suite; do not weaken validators or authority checks to obtain a
  pass. DRIFT-021 remains open until the controlled rule is accepted and the
  conflicting component guidance is replaced. Owner Stage 0 signoff remains
  separate from implementation or CI success.

## Alternatives considered

- **Infer N-1 from package releases.** Rejected in this proposal because package
  versions and supported protocol majors describe different compatibility facts.
- **Silently skip a missing previous major.** Rejected because missing evidence
  cannot establish first-major status or make required coverage disappear.
- **Require protected containment for every T14 semantic assertion.** Not
  recommended: it conflates version/capability behavior with separate hostile
  containment gates. Actual profile limits still have to be reported.
- **Count unenforced cooperative checks as passes.** Rejected because a report
  must demonstrate the required semantic observation, not merely disclose that
  it was not enforced.
