---
Status: Draft
Doc-Type: tutorial
Owner: platform-maintainer
Last-Reviewed: 2026-11-17
Audience: operators
---

# Run your first Soul task on a Mac

Run `hello.soul` from Terminal using the cooperative development profile. The sample uses real HQ and the Soul runtime with two deterministic adapters. It needs no provider account, API key or administrator access.

## Prepare a clean checkout

You need Git, Python 3, Node.js 20 or later with npm, and network access to the public True Line repositories. From a directory where you keep source code, run:

```sh
git clone https://github.com/true-line/soul-conformance.git
cd soul-conformance
npm run prepare:pins
```

The preparation command downloads and verifies the pinned inputs. If you already have a checkout with edits, clone into a new directory. The evidence runner requires a clean working tree.

## Run the sample

```sh
npm run quickstart -- --out reports/quickstart-latest.json
```

The runner starts HQ and the Soul runtime for this task. The specialist repairs a scratch file, runs its check, and submits a proposal. The lead makes the final commitment. The sample writes to a disposable copy of the template.

## Check the result

```sh
node -e 'const r = require("./reports/quickstart-latest.json"); console.log(r.outcome, r.host.os, r.enforcement_profile.in_force)'
```

On a successful Mac run, the output is `pass darwin managed-cooperative`. The JSON report includes the task ID, checks, source revisions, and adapter versions. Keep it when comparing results between machines.

The protected Mac pilot has a separate qualification gate for account isolation, key custody, and enforcement on the designated host. The cooperative sample remains useful for checking your toolchain while that work proceeds. See the [Mac pilot decision](https://github.com/true-line/agent-bot-platform/discussions/85) and [conformance runner](https://github.com/true-line/soul-conformance/tree/main/suites/quickstart).
