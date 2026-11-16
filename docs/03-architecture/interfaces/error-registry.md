---
Status: Draft
Doc-Type: interface
Owner: protocol-maintainer
Last-Reviewed: 2026-11-16
Normative-Source: true-line/soul-contracts errors/registry.json
---

# Error registry

Error codes are registered in soul-contracts before an implementation emits them.
This generated reference table projects the released registry; the canonical
source owns each code's meaning, retryability and emitting components.

## Released source

The table was regenerated on 2026-11-16 from the
[v0.5.0 registry](https://github.com/true-line/soul-contracts/blob/b96239cc47571237f7064ddbcbd0edec8e365c6b/errors/registry.json).
Its 27 entries are byte-identical to the
[v0.4.1 registry](https://github.com/true-line/soul-contracts/blob/d9ca0731fbe7bbf7a29d066c8a23cd92717ee9bd/errors/registry.json)
used by the bounded T14 report. Registry format version `0.3.0` is distinct
from those package release versions. Source SHA-256:
`999ce0bed9bf7cfd8b1bed63d35d080fd0b5c00a7ebda42362d8caf118d7c365`.

The [typed-refusal schema](https://github.com/true-line/soul-contracts/blob/b96239cc47571237f7064ddbcbd0edec8e365c6b/schemas/common/v1/error-response.schema.json)
requires `error`, a safe `explanation` and `correlation_id`; it may echo
`request_id`. `unsupported_version` and `required_capability_missing` are the
registered T14 codes. The report names actual boundary-specific refusals;
not every malformed frame is a shared typed-refusal response.

## Codes

<!-- Regenerated from the immutable released registry using the command below. -->
| Code | Description | Retryable | Raised by |
|---|---|---|---|
| `unsupported_version` | The peer's contract version is outside the supported N and N-1 window (T14). | no | hq, broker |
| `required_capability_missing` | A frame requires a capability the receiver has not negotiated. | no | broker |
| `caller_mismatch` | The authenticated caller does not match the claimed runtime or handle binding (T01). | no | hq, broker |
| `stale_epoch` | A commit carries an installation epoch older than the authoritative current one. | no | broker, hq |
| `lease_expired` | The runtime execution lease has expired; protected commits stop until a new lease is acquired. | yes | hq, broker |
| `grant_revoked` | Authority was revoked; consume, wake, and execution refuse it (T08). | no | broker, hq |
| `destination_denied` | The destination is not approved for this task's data restrictions (T09). | no | broker |
| `budget_exhausted` | The ceiling or sub-allocation is spent; new protected spend refuses (T26). | no | broker |
| `revision_conflict` | Compare-and-swap on the expected task revision failed; retry with the fresh revision. | yes | hq |
| `message_conflict` | A message ID was reused with different content; the message is quarantined. | no | broker |
| `mailbox_full` | Backpressure at the mailbox capacity limit; accepted work is never silently dropped (T18). | yes | broker |
| `frame_too_large` | The frame exceeds the inline size limit; use an authorized content reference. | no | broker |
| `message_expired` | A queued message passed its expiry and is purged, not treated as new work (T25). | no | broker |
| `quarantined` | The message or Soul is quarantined (poison threshold, conflict, or crash loop) until the cause is resolved (T23). | no | broker, hq |
| `definition_not_accepted` | Hello presented a definition digest that is not an accepted revision. | no | hq |
| `evidence_missing` | Completion criteria require evidence that was not supplied; supply it and retry. | yes | hq |
| `approval_mismatch` | The proposed action no longer matches its approval record digest (T24). | no | hq, broker |
| `write_scope_conflict` | A task's write scope overlaps an active one without owner-allowed concurrent writers. | no | hq |
| `outcome_unknown` | An external effect's outcome is ambiguous; reconcile through lookup, never blind replay (T06). | no | broker, hq |
| `eval_coverage_missing` | Candidate acceptance lacks a passing cell for a (role, harness version) pair (T27). | no | hq |
| `candidate_rejected` | The whole candidate was rejected on a failed cell; a narrowed candidate may be re-evaluated (T28). | no | hq |
| `render_failed` | A non-optional primitive could not be rendered for an adapter; the failure names the class. Retryability depends on the named class. | no | soul-build |
| `source_chain_unapproved` | A proposal derived from peer or external-untrusted content waits for owner approval of its source chain (T30). | no | hq |
| `dream_limit_exceeded` | A dream run breached its wall-clock or maintenance limit; no candidate is emitted (T29). | no | hq |
| `credential_unavailable` | The identity service is unreachable; protected effects that need a fresh credential wait and retry when it returns. | yes | hq, identity-service |
| `device_revoked` | The device is revoked; cached tokens are dropped and recovery requires new enrollment. | no | hq, identity-service |
| `profile_insufficient` | A protected claim was made under a weaker enforcement profile (T21). | no | hq, broker |

## Regeneration

Run this command to reproduce the table rows in registry order. It refuses a
source-byte mismatch before rendering. Update the source pin and digest only
after reviewing a new released registry; do not invent or rename codes here.

```sh
python3 - <<'PYCODE'
import hashlib, json, urllib.request
url = "https://raw.githubusercontent.com/true-line/soul-contracts/b96239cc47571237f7064ddbcbd0edec8e365c6b/errors/registry.json"
data = urllib.request.urlopen(url, timeout=30).read()
assert hashlib.sha256(data).hexdigest() == "999ce0bed9bf7cfd8b1bed63d35d080fd0b5c00a7ebda42362d8caf118d7c365"
for entry in json.loads(data)["codes"]:
    print("| `{}` | {} | {} | {} |".format(
        entry["code"], entry["description"],
        "yes" if entry["retryable"] else "no", ", ".join(entry["raised_by"])))
PYCODE
```

New codes and their fixtures belong in soul-contracts. A component adopts them
only after registration; platform tests and traceability cite the released name.
