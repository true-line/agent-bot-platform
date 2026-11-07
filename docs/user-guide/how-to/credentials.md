---
Status: Draft
Doc-Type: how-to
Owner: platform-maintainer
Last-Reviewed: 2026-11-05
Audience: operators
---

# How to: manage credentials

Add, rotate, revoke, and — most importantly — verify that secrets never
reach harness-readable files.

**Model (specified, §5, §11, T02):** HQ holds keys. `Equip` returns
*references*, never secrets. Credentials never travel in the `.soul`
package. Rotation and revocation are release prerequisites (§15).
Under brokered inference the provider key never reaches a harness; the
short-lived-token route is the exception and is labeled in every receipt (§4).

## Add a credential

```bash
hq credential add <id>
```

HQ prompts for the secret; it lands in the HQ key store, keyed by `<id>`.
The Soul's grants reference the id — the package carries references only.

## Rotate

```bash
hq credential rotate <id>
```

Rotation re-equips at the **next lease renewal** — in-flight protected
operations continue under the old lease; new ones pick up the new secret.

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

On **cooperative** (macOS), harnesses share a trust domain: the broker
still holds the keys, but a prompt-injected member can reach anything its
harness can. Give the Soul only credentials you would give its
least-trusted harness ([trust domains](../../03-architecture/trust-domains-and-profiles.md)).

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `credential_revoked` on a protected op | rotation/revocation landed | re-grant or restore credential |
| Receipt shows direct provider route on cooperative | egress is cooperative in this profile | expected; move protected work to Linux |
| Secret fingerprint found in a member home | a harness wrote it out | file it — this is a T02 violation |
