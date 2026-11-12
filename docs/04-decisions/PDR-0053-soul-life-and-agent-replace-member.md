---
Status: Accepted
Doc-Type: decision
Owner: product-owner
Last-Reviewed: 2026-11-12
Date: 2026-11-12
Accepted: 2026-11-12
Discussion: https://github.com/true-line/agent-bot-platform/discussions/53
Affects-Repos: [soul-contracts, agent-bot-hq, agent-bot-comms, agent-bot-souls, agent-bot-machine]
Affects: [trust-model]
---

# PDR-0053 Soul, Life and agent replace member

A Soul is a package, not an agent. A running Soul is a Life; its lead harness is the brain, and the agents that run in its harnesses are its motor functions, talents and traits. "Member" is retired as the name for what runs in a harness, and the OS account unit is one account per harness credential, not one per member. Contract field names such as `member_id` stay, so no wire format changes.

## Context

- In a working session the owner described the model:
  - A Soul is a package. It can run by itself, or preferably managed by HQ.
  - A running Soul is a Life: "a running soul over time which captures memories, experiences, and new abilities/skills (not to confuse with skills.md)". It is something bigger than an agent.
  - Inside it, a lead harness is the brain, the orchestration layer.
  - The agents that run in the harnesses are the motor functions, talents and traits of that bigger thing. An agent is not the equivalent of a person; the Life is.
  - A capability can have more than one harness, picked by the kind of task.
  - "Member" implies agent, and a Soul is not n agents. The glossary line "Member: a harness brain-region inside a Soul" is a false abstraction.
- Controlled records disagree with that model:
  - The [glossary](../glossary.md) Soul line comes from S6 §3, which calls a Soul "a persistent multi-member agent". DRIFT-009 already tracks a Soul and principal conflict with agent-comms.
  - The glossary Member line (S5) reads "a harness brain-region inside a Soul".
  - The glossary Life line (S6 §3) defines only the stored half.
  - agent-bot-hq D7 (in the [decision log](decision-log.md) under the repository's former name, agent-bot-daemon D7) and its plan rows 16a to 16d give each member its own OS account and keep state in the member's home.

## Decision

1. **The glossary takes these definitions.** The [glossary](../glossary.md) is their single home.

   | Term | Definition |
   |---|---|
   | **Soul** | A package: a definition plus what its Life has captured. One stable ID. It runs by itself or, preferably, managed by HQ. A Soul is not an agent |
   | **Life** | A Soul running over time. It captures memories, experiences and new abilities. Its captured state is stored in the package and moves with the Soul |
   | **Lead** | The Life's brain: the one harness that orchestrates, routes work and finalizes decisions |
   | **Agent** | What runs in a harness inside a Life: a motor function, talent or trait of the Life. Not the equivalent of a person; the Life is. One Life has several |
   | **Harness** | The program an agent runs in. One credential and one OS account per harness credential |

2. **"Member" is retired** as the name for what runs in a harness. Field names in released contracts, such as `member_id`, stay as they are and take their meaning from the glossary: they identify an agent of a Soul. No wire format changes.
3. **One OS account per harness credential.** The account unit is one OS account per harness credential (one GitHub bot identity), not one per member of each Soul. Per-member accounts multiply without bound. One harness account can run many harness processes at once, and the agents of every Soul that uses that harness share it.
4. **Not decided here.** Whether a harness account shared between Souls can earn the `protected` label, the name of the package directory `home/<member>/`, and whether requirement and test texts need rewording stay unspecified.

## Acceptance

The owner accepted option B on 2026-11-12, in the marked answer to [discussion #53](https://github.com/true-line/agent-bot-platform/discussions/53).

## Consequences

- **soul-contracts:** prose and field descriptions that say "member" use the glossary's terms. Field names stay, and no schema or fixture changes.
- **agent-bot-hq:** agent-bot-hq D7 and plan rows 16a to 16d move from one OS account per member to one per harness credential, and stop describing state as kept in the member's home. agent-bot-hq D7 also said the SOP's per-harness account record is amended to per-member. The SOP's agent-bot identity reference still gives each harness one account, which is what this record decides, so the SOP needs no change.
- **agent-bot-comms, agent-bot-souls, agent-bot-machine:** prose that says "member" uses the glossary's terms.
- **Platform:** the glossary, the trust-domain, lifecycle and package-format pages, and the decision log follow this record. DRIFT-017 tracks the component records until each repository corrects them, and DRIFT-009 notes the new Soul definition.

## Alternatives considered

- **Option A: leave the glossary as it is.** Every later row keeps building on "member", which implies that a Soul is a set of agents; the owner called that a false abstraction. The account model keeps multiplying accounts.
- **Option C: change the words only and keep one OS account per member (agent-bot-hq D7).** It keeps the strongest separation between the agents of a Soul, and keeps the account growth the owner objected to.
