---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-20
Audience: operators
---

# How to: manage credentials

Add, rotate, revoke, and — most importantly — verify that secrets never
reach harness-readable files.

**Model (specified, §5, §11, T02):** HQ requests protected operations from Machine over the paired local channel. `Equip` returns
*references*, never secrets. Credentials never travel in the `.soul`
package. Rotation and revocation are release prerequisites (§15).
Under brokered inference the provider key never reaches a harness; the
short-lived-token route is the exception and is labeled in every receipt (§4).

Machine is the default on every platform and profile, whether HQ runs in a
dedicated account or an ordinary user account. The same custody rules apply
to setup, normal operation, migration and recovery. HQ uses its channel key
to authenticate fixed requests to Machine. Machine authorizes each request.
Machine/keyd in the secure administrative account performs protected signing,
encryption and decryption. HQ handles HTTPS. Machine/keyd signs the device
assertion with the device key and uses a separate, short-lived session key
for proof of possession of the access token. A stopped or
unreachable Machine, or a revoked pairing, cuts off those operations. See
[privileged host custody](../../04-decisions/PDR-0091-host-privileged-custody.md).

Only explicitly configured standalone HQ in its dedicated account on a Mac
without Machine installed may use a local Secure Enclave device signer. That
exception covers signing alone. Machine-backed HQ never switches to standalone
signing on failure. See [standalone eligibility](../../04-decisions/PDR-0093-standalone-hq-secure-enclave-signing.md).

## Add a credential

Provision provider keys and GitHub App private keys in Machine’s secure
administrative account. Give HQ the credential ID. The HQ credential and
audit commands in this guide are [proposed CLI forms](../reference/cli.md).

```bash
hq credential add <id>
```

The Soul's grants reference the id — the package carries references only.

## Rotate

```bash
hq credential rotate <id>
```

Rotation re-equips at the **next lease renewal** — in-flight protected
operations continue under the old lease. New leases refer to the rotated
credential.

## Revoke

```bash
hq credential revoke <id>
```

Takes effect at the **next protected operation** (§4). Tasks mid-flight
move to `waiting`; the console records why.

## Verify the boundary

```bash
hq audit secrets          # scans member homes and workspaces for known secret fingerprints
hq receipts my-soul --destination provider/anthropic   # confirm brokered route, no direct egress
```

The authoritative check is **T02** on *your* host — the conformance suite
verifies the key boundary; ask for the release report
([release conformance](../../08-release/release-conformance-report.md)).

## Profile warning

On a **cooperative** host, harnesses share a trust domain: the broker
still requests privileged operations from Machine, but a prompt-injected member can reach anything its
harness can. Grant the Soul only operations you would authorize its
least-trusted harness to perform ([trust domains](../../03-architecture/trust-domains-and-profiles.md)).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `credential_revoked` on a protected op | rotation/revocation landed | re-grant or restore credential |
| Receipt shows direct provider route on cooperative | egress is cooperative in this profile | expected; move protected work to a qualified host |
| Secret fingerprint found in a member home | a harness wrote it out | file it — this is a T02 violation |
