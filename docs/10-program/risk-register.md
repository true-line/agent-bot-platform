---
Status: Draft
Doc-Type: plan
Owner: product-owner
Last-Reviewed: 2026-11-07
Sources: S6 §16; S1 watch list
---

# Risk register

Product and program risks that could invalidate the platform's claims or plan. Each risk names its source and the default the plan proceeds on. Risks are reviewed at every stage exit.

| ID | Risk | Source | Default we proceed on | Watch for |
|---|---|---|---|---|
| RISK-001 | Vendor harnesses have enforcement gaps that no adapter can close | S6 section 16 | Adapters qualify individually; cooperative profile is declared, never upgraded by label | A pilot harness that cannot pass T03 |
| RISK-002 | HQ concentrates authority; one compromise exposes every Soul on the host | S6 section 16; S1 | Acceptable for one owner per machine | Machines shared by several owners need one key store per owner |
| RISK-003 | The identity service concentrates key custody | S6 section 16 | Owner-operated service; hosts hold only short-lived device-bound tokens | Any requirement to cache long-lived keys on hosts |
| RISK-004 | External services cannot be reconciled reliably after an ambiguous effect | S6 section 16 | Durable intent before send, idempotency keys, unknown outcome raised to the owner | A pilot service with no lookup or idempotency |
| RISK-005 | The Linux protected profile does not match the macOS machines first users run | S6 section 16 | macOS runs cooperative and says so until its protected profile qualifies in Stage 4 | Pilot users who cannot run Linux |
| RISK-006 | Coordination costs more than the value it delivers | S6 sections 15 and 16 | Measure cost per accepted task against single-harness baselines in the pilot | Pilot cost per accepted result above the baseline |
| RISK-007 | Standalone mode is unenforced but becomes the main experience | S1 watch list | Standalone is a declared developer fallback | Store customers running Souls without HQ |
| RISK-008 | Two daemons coexist during the strangler migration | S1 watch list | The agent-bot daemon keeps its launchd label until HQ takes supervision | Owner-console release timing forcing an early cutover |
| RISK-009 | Repository sprawl recreates drift faster than the platform removes it | 2026-11-07 survey | Admission rule and charters in PDR-0002 | A repository created without a catalog entry |
| RISK-010 | The code name GeniusBar collides with Apple's Genius Bar trademark | Owner, 2026-11-07 | GeniusBar is an internal code name only, never used in public material | Any public release, store listing, domain or marketing copy |
| RISK-011 | Opening platform repositories exposes personal data or secrets in their history | Owner, 2026-11-07 (MIT licensing) | A repository goes public only after the privacy check passes on every commit in its history | A visibility change requested without a history scan |
