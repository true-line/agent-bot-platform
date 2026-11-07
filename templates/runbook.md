---
Status: Draft
Doc-Type: runbook
Owner: platform-maintainer
Last-Reviewed: YYYY-MM-DD
Verified-Against: <S6 §N; T-series IDs>
---

# Runbook: <failure class>

<One paragraph: the failure this runbook resolves and the outcome it restores.>

> One runbook per failure class that spans repositories. A failure inside one
> component belongs in that component's runbooks.

## Symptoms

What the operator observes: console state, receipt states, error codes.

## Immediate actions

Numbered, copy-pasteable commands that stop the damage. Mark anything irreversible.

## Diagnosis

How to tell which variant you have.

## Resolution

Per variant. An unknown outcome is looked up, never blindly replayed (S6 §7, T06).

## Verification

How to prove the system is healthy again.

## Escalation

When to stop and whom to involve; the diagnostics bundle to attach.
