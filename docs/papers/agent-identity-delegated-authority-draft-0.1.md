---
Status: Frozen
Doc-Type: paper
Owner: product-owner
Last-Reviewed: 2026-11-05
---

# Agent Identity and Delegated Authority — White Paper Draft 0.1


> Converted from `agent_identity_and_delegated_authority_white_paper_draft_v0_1.pdf` (26 pages) with scripts/pdf2md.py — PDF text extraction is best-effort; curate before treating as normative. The original PDF is authoritative.


<!-- page 1 -->

20 October 2026
Agent Identity and Delegated Authority
Identity continuity and scoped authority for composite Souls
White paper draft 0.1 | True Line AI | 20 October 2026
We propose an identity architecture for a Soul that persists while its internal agents,
harness runtimes, models, and hosts change. Bob is the continuing agent. Its knowledge
specialist, coding worker, and productivity worker cooperate within Bob through
authenticated runtime membership and bounded grants. Other Souls normally address Bob.
Bob may expose a particular specialist through an explicit delegation that preserves the
same authority and disclosure rules.
The architecture separates identity, authentication, authorization, attribution, and
evaluation. A name identifies a subject; an authenticated execution establishes who is
making a request; a grant determines what that execution may do; an action record
preserves who requested, authorized, performed, and externally represented the work.
Evaluation supplies evidence about behavior under stated conditions. These records answer
different questions and must remain distinguishable.
The proposed default is practical for one local harness. A trusted supervisor registers the
runtime, a broker mediates protected operations, and the Soul retains durable identity and
provenance. Additional harnesses join the same governed composition. Remote execution,
direct specialist endpoints, and coordinated replicas require explicit extensions. A
transferable package carries identity records and selected life; activating it requires current
authority and credential bindings. Possession of copied bytes alone does not establish that
authority.
This paper is a companion to Native Shareable Soul Packages and the proposed Agent
Communications and Trustworthy Coordination paper. It defines the identity and authority
contracts those papers share. It is an architecture draft, with proposed acceptance
scenarios and unresolved choices, rather than a claim that the complete design has been
implemented or evaluated.



<!-- page 2 -->

Agent Identity and Delegated Authority
Draft 0.1   |   2
Contents
The paper defines identity and authority for one continuing Soul whose members cooperate
across harnesses, hosts, and external services.
1 Purpose and scope
2 The composite Soul and its participants
3 Stable identifiers and current authority
4 Runtime membership and internal cooperation
5 Credential ownership and key custody
6 Delegation as a bounded authority contract
7 Communication within and between Souls
8 Attribution and evidence
9 Identity through change and recovery
10 Knowledge dreaming and containment
11 Agent Stores and evaluation identity
12 Interoperability and implementation profiles
13 Existing contracts and the specification gap
14 Acceptance scenarios
15 Decisions and implementation path
References
Draft status
Section 13 distinguishes existing repository contracts from proposed extensions. Section 14
contains 32 acceptance scenarios. Section 15 identifies decisions needed for an
implementable specification.



<!-- page 3 -->

Agent Identity and Delegated Authority
Draft 0.1   |   3
1 Purpose and scope
A useful agent should retain its relationships, accepted knowledge, and accountability when
its execution software changes. A user should be able to recognize Bob after a harness
upgrade, replace a coding model without creating another Bob, and move Bob's continuing
life to a compatible host. At the same time, another process must not acquire Bob's
permissions simply by copying a package or repeating its display name.
We therefore treat the Soul as the persistent composite identity and its executing members
as delegates. The package describes the composition and stores the continuing life. Trusted
host services establish runtime membership and enforce access. External systems retain
their own account and authorization rules. The identity contract connects these layers
without pretending that their principals are interchangeable.
This paper covers identifier lifetimes, trusted enrollment, internal membership, credential
bindings, delegation, action attribution, key changes, transfer, recovery, quarantine, and
evaluation provenance. It leaves transport negotiation, streaming, delivery ordering, and
full task message schemas to the communications paper. The package paper owns the
physical layout, portable representation, and export selection rules. Each paper must use
the same entity definitions and distinguish an accepted definition revision from current
execution authority.
The design supports autonomy through standing policies. An owner can authorize a class of
work once, including bounded delegation and routine dream processing. The runtime
checks that policy when actions occur. Human confirmation is required only when the
applicable policy requires it or an action exceeds existing authority. The architecture should
make permitted work efficient and make changes of authority reviewable.
The proposal assumes that the supervisor, authorization service, credential backend, and
relevant operating-system controls are trusted to enforce their declared responsibilities.
Agents, imported content, peer messages, tools, and remote services can supply mistaken
or adversarial inputs. A compromised host administrator can defeat controls that depend on
that host. Conformance claims must name the enforcement profile and its assumptions.
2 The composite Soul and its participants
One identity across several harnesses
A Soul is a persistent composite agent with a stable identity, an accumulated life, and a
governed set of internal agents that execute through one or more configured harness
runtimes. Its members exchange tasks and findings through permitted internal channels.
The Soul remains the external identity responsible for actions carried out under its
authority.
Bob might use a Codex-based knowledge worker, a Claude-backed coding worker, a
Hermes-based productivity worker, and a separate reviewer. These assignments are
illustrative configuration choices. The architecture makes no comparative performance
claim about those products. Role selection can change as evaluations provide evidence
about suitability, cost, capability, and allowed data destinations.



<!-- page 4 -->

Agent Identity and Delegated Authority
Draft 0.1   |   4
The minimum configuration has one member and one harness runtime. A paused or stored
Soul has no active runtime but retains its identity and life. A multi-harness configuration can
run participants concurrently, coordinate them sequentially, or activate specialists on
demand. No permanent lead model is required. Routing and acceptance can be
implemented by deterministic services, delegated coordinators, or a combination with
explicitly assigned responsibilities.
Entity Responsibility Identity lifetime
Soul
Continuing external identity,
accepted definition, accumulated life,
and logical credential bindings
Survives ordinary runtime and host
changes
Controller
Principal authorized to administer
specified parts of the Soul and its
authority
Changes through an authorized
control transition
Internal member Soul-scoped worker or role with task state and delegated capabilities May persist across replacement executions
Harness
Software that executes agent
behavior and exposes native
capabilities
Named and versioned as software
Runtime instance A particular admitted harness execution environment Ends on replacement or termination
Model and provider Inference components used by an execution Recorded for each relevant execution
Installation A placement of the Soul on a host with local bindings Changes when enrolled on another host
Run or session Bounded activity with resolved inputs and execution context Stable identifier for its retained record
The baseline can register one internal member for each runtime. Named subagents inside a
harness may also be recorded. If several subagents share the same process credentials and
access channel, their names describe logical contributors; the host cannot claim
independently enforced permissions between them. Separate authority requires a caller
identity and enforcement boundary that the host can actually distinguish.
The word owner describes the person or organization controlling the Soul's use and life in
this architecture. A controller is the authenticated principal exercising a particular
administrative authority. A resource owner, external account holder, package publisher, and
host operator may all be different parties. Their relationships must be recorded rather than
inferred from a shared name.
Shared identity with specific accountability
An external answer can be attributed to Bob while its internal evidence identifies the
members and runtimes that contributed. The coding worker can propose a change, a
reviewer can assess it, and a separately authorized executor can commit it. None of those
steps requires replacing Bob's identity.



<!-- page 5 -->

Agent Identity and Delegated Authority
Draft 0.1   |   5
Conversely, the identity of the inference model does not establish the identity of the acting
principal. A model can appear in many different Souls. An external service account may
perform operations for several Souls under broker control. The authorization decision must
resolve the actual Soul, caller, credential binding, task, and target for each operation.
Figure 1  Proposed composite identity. Members act within Bob through admitted runtimes and scoped grants.
The trusted services enforce access; membership and shared storage alone do not establish permission.
3 Stable identifiers and current authority
Identity records
The proposed Soul identifier is an opaque value with a documented generation and
comparison rule. Its spelling does not encode a display name, filesystem path, current
harness, host address, or current public key. A rename, move, key rotation, or model
change preserves that identifier. A new template instance or explicit fork receives a new
identifier with retained provenance.
The identifier alone is an assertion of which Soul is intended. A verifier needs an accepted
binding between that identifier and an authority permitted to authenticate it or update its
control records. The first profile should define local trusted enrollment and a portable public
identity descriptor. Additional profiles can map the same logical Soul to a published
identifier system.



<!-- page 6 -->

Agent Identity and Delegated Authority
Draft 0.1   |   6
The descriptor should contain the Soul identifier, schema version, controller references,
purpose-qualified verification methods, supported authentication profiles, authorized
service endpoints, status references, and a control-record revision. Public material should
disclose only what a peer needs to identify and contact the Soul. Internal member
inventories, credential handles, source paths, and private memory do not belong in an
unrestricted directory listing.
There are several independent kinds of change. A definition revision identifies accepted
instructions, capabilities, and configuration. A knowledge checkpoint identifies retained
learning selected for a particular use. A control-record revision identifies a version of
identity administration. An authority epoch invalidates an older generation of runtime or
delegation authority. A host-local installation identifier and run identifier locate executions.
The specification must define each field's scope and update rule.
In particular, restoring an older package definition must not restore expired grants or an
earlier authority epoch. Security state needs a trusted current record outside the rollback
domain of ordinary Soul content. The package can preserve historical receipts, while the
local controller or configured authority determines which grants and installations are
currently valid.
Establishing trust
Local enrollment binds an inspected Soul identifier to the owner's current control policy and
credential backend. For a peer, trust can begin through an authenticated introduction, an
explicitly accepted key binding, or a registry the recipient has chosen to trust. The profile
records how that binding was established. A self-signed descriptor can demonstrate
consistency with its own key, but it cannot by itself establish that the key belongs to a
previously known Bob.
Friendly names and contact aliases are resolved within a known namespace. Two
independently enrolled Souls can both be named Bob. The recipient interface should expose
enough stable identity and relationship information to distinguish them, particularly when
permissions or recipients change. Display names are never authorization selectors by
themselves.
Every update must be validated against the prior accepted control state and its transition
policy. A larger sequence number is insufficient without an authorized transition. Conflicting
signed successors require a declared resolution procedure and a visible conflict state. The
initial profile can use one designated authority to serialize these changes; a distributed
implementation needs an explicit consistency mechanism.
W3C DID Core provides a useful reference for separating a subject from its controller and
for associating verification methods with authentication, assertions, key agreement,
capability invocation, or delegation. It also leaves substantial behavior to the chosen DID
method. This proposal can adopt a compatible mapping without requiring every local Soul
to deploy a decentralized registry. [R6]



<!-- page 7 -->

Agent Identity and Delegated Authority
Draft 0.1   |   7
4 Runtime membership and internal cooperation
Admission of an executor
A trusted supervisor admits a runtime under an enrolled installation. Admission resolves the
Soul identifier, internal member identifier, runtime instance identifier, session identifier,
accepted definition revision, executable artifacts, and effective execution profile. The profile
includes the permitted provider route, tools, source views, and isolation capabilities.
Requested configuration and observed configuration remain distinguishable.
The supervisor supplies the resulting identity through an authenticated execution channel.
Depending on the platform, this can use a protected local connection with reliable peer
binding, a sandbox or account boundary, or an enrolled remote workload identity. The
application must not accept an agent's self-declared role in a prompt, environment variable,
or tool argument as the only proof of identity.
An authenticated process may receive an opaque grant handle that the broker resolves to
its actual permissions. The handle is bound to the admitted caller and intended service.
Copying the handle into another worker's text does not transfer the grant. A remote profile
can use a verified, sender-bound credential with equivalent semantics. The exact credential
encoding is a profile choice.
The supervisor invalidates membership when it observes termination, replacement, or
withdrawal of admission, including applicable quarantine. Remote membership also follows
a declared lease and status-freshness policy. Loss of contact is not proof that a remote
workload has stopped. A replacement can retain a logical member role, but it receives new
runtime credentials and records the reassignment. Resuming a transcript or task does not
revive the old runtime's authority.
Cooperation within one Soul
The internal service permits discovery and messages among authorized members of the
same Soul. Resource and task restrictions still apply. A knowledge worker can return an
allowed source view to a coding worker; it cannot expand that worker's rights by attaching
private material to a message. A worker's suggestion to run a command is evidence or a
proposal until the appropriate policy admits the resulting action.
The trusted service assigns source restrictions to disclosed views and applies them to
derived outputs. Agent-supplied labels cannot lower those restrictions. When precise
derivation cannot be established, a conservative task or session disclosure scope can
preserve the boundary. Widening disclosure requires an authorized decision; a content
classifier's judgment that a summary looks harmless is insufficient by itself.
The trusted message envelope records sender membership, recipient, task, correlation
references, classification, and any applicable delegation. The payload can carry a request,
finding, candidate, or result. A generated sentence claiming that the owner approved an
operation cannot replace an authenticated decision record.
Internal agents normally communicate with other members under the same Soul. Cross-
Soul agent traffic goes through the Soul's external communication authority or an explicitly
delegated endpoint described in Section 7. Model inference and ordinary tool connections



<!-- page 8 -->

Agent Identity and Delegated Authority
Draft 0.1   |   8
have their own destination policies; they must not be confused with internal agent
membership.
Shared knowledge belongs to the continuing Soul and is exposed through permitted
retrieval and graph operations. Private working hypotheses, accepted assertions, external
claims, and authoritative owner directives need different record types. Copying a claim
between workers does not create additional independent evidence for it. Source lineage lets
later sessions and dreams identify that repetition.
Enforcement profiles
A protected profile requires complete mediation of the operations it claims to control. If an
agent shell can read broker keys, invoke an unrestricted credential CLI, inspect another
worker's plaintext, or reach a prohibited provider through an alternate route, the
corresponding protection is unavailable. The host reports that limitation rather than
asserting isolation from a directory structure or prompt instruction.
Dedicated operating-system accounts, containers, virtual machines, and constrained
delegates can offer different boundaries. The profile specifies the actual controls and
residual access, including process inspection, inherited environment, local sockets,
mounted files, and network routes. A user can select a less isolated mode, but evaluation
and sharing records must identify that mode accurately.
5 Credential ownership and key custody
Logical bindings and external principals
Credential bindings belong to the Soul's continuing configuration. Changing a harness
should preserve the declared relationship between Bob and the accounts it is allowed to
use. The credential backend retains or exercises secret material under that relationship.
The external service remains authoritative about the account, organization, installation,
permissions, and policies that its credential represents.
A binding therefore identifies a logical purpose, expected external principal, backend
reference, permitted operations, resource constraints, and disclosure mode. Import resolves
the binding to a verified account. A destination must not select an unrelated account merely
because its local credential has the same friendly name.
There are two different credential operations. A broker can perform an action or signature
while keeping the secret outside the agent. Some native clients instead require a readable
token or sign-in state. That mode exposes the credential to the receiving execution for its
valid scope and lifetime. The implementation must report which mode is used and cannot
describe token delivery as retained custody.
The proposed default keeps long-lived identity keys, administrative secrets, and recovery
material outside the distributable package and outside agent-readable storage. Short-lived
service tokens may be delivered where a compatible execution profile permits it. Their
scope and destination should be reduced to the required operation. Refresh credentials and
unrestricted application keys remain with the backend whenever the integration supports
that arrangement.



<!-- page 9 -->

Agent Identity and Delegated Authority
Draft 0.1   |   9
A delivered token remains usable according to the external service's scope, expiry, and
revocation behavior. The profile must state whether direct calls remain subject to broker
limits and current grant status. If they bypass those checks, the host cannot claim centrally
enforced per-call budgets or immediate descendant revocation for those calls.
Repository documentation already treats credential references and provider bindings as
distinct concerns. Its supported native authentication paths also need to be assessed
individually when adopting this stricter external-custody profile. The draft does not assume
that every existing harness can satisfy the proposed boundary. [R3]
Purpose separation
An authentication key proves an enrolled caller's identity. An authority issuer grants
operations. A package publisher signs a distributable artifact. An evaluator attests to a test
record. A credential backend authenticates to an external account. These purposes may be
administered by the same organization, but each use must be explicitly permitted. Verifiers
should not treat a valid signature for one purpose as authority for another.
For example, a store publisher's signature can authenticate the release provenance. It must
not make that publisher an administrator of every Soul instantiated from the release.
Similarly, a reviewer allowed to attest to test results does not gain permission to change
Bob's recovery policy.
Cryptographic profile selection should use established constructions and maintained
libraries. A concrete implementation must pin its signature and authentication profiles,
algorithm policy, key identifiers, canonical representation where relevant, domain
separation, and rejection behavior. Unknown required features fail verification. This paper
specifies the relationships that must be represented; it does not introduce a new signature
algorithm or claim interoperability between unspecified encodings.
Shared application identities
A shared GitHub App or other service integration can be used for several Souls if a trusted
broker keeps each Soul's effective permissions and attribution separate. The app's private
key does not belong in every harness. The broker resolves the requested account and
installation, verifies the Soul's scope, and obtains or exercises the appropriate credential.
GitHub documents installation authentication as access through an installed App to
permitted resources. Git separately records author and committer information. Those
mechanisms illustrate why a Soul author, a committing executor, and the service actor
performing an API operation must remain separately attributable. Changing commit
metadata does not change the identity authenticated to the service. [R10] [R11]
Reducing the number of service applications can simplify administration, but it places more
responsibility on the shared broker. A shared credential's underlying permissions are an
upper bound, not a grant to every Soul. Where a service cannot enforce the intended
distinctions, the host must apply narrower credentials or disclose the resulting limitation.



<!-- page 10 -->

Agent Identity and Delegated Authority
Draft 0.1   |   10
6 Delegation as a bounded authority contract
What a grant means
A delegation permits an authenticated recipient to perform specified operations for a
bounded purpose. It does not transfer the Soul's identity. An internal worker acts as a
member of Bob; an external Soul asked to help remains its own identity. Both the requester
and the executing principal appear in the retained record.
The issuer must have authority to grant the requested rights. The recipient must prove the
identity to which the grant is bound. The enforcing service must verify that it is an intended
audience and that the requested operation, resource, data disclosure, and execution
conditions remain within scope. Free-form task text explains intent but is insufficient to
define a mechanically enforceable permission boundary.
OAuth Token Exchange explicitly distinguishes delegation from impersonation and can
represent an actor acting on behalf of another subject. That provides useful semantics for
an interoperability profile. It does not supply the Soul-specific scope, enrollment, or
acceptance policy by itself. [R7]
An actor-history chain records who participated. Effective authority comes from validated
grants and policy. In particular, nested prior actors in the token-exchange representation
must not be treated as an authorization chain that independently supplies permissions. The
delegation profile needs separate, checkable authority references. [R7]
The first local profile can use opaque grant handles stored by the trusted broker. A remote
profile can use authenticated grant documents or a token exchange with equivalent checks.
The recipient should see only the claims it needs; private owner information and unrelated
lineage can remain behind authorized references.
Grant element Required interpretation
Schema and grant identifier Versioned semantics and an unambiguous reference for audit and revocation
Issuer and authority reference Which accepted authority may issue the grant and under which current control state
Subject and caller binding The member, executor, or peer permitted to exercise it, with proof tied to the execution channel
Audience The enforcing service or explicitly bounded set of services allowed to accept it
Soul and execution context Represented Soul, authorized installation, and any required member, runtime, or session binding
Task and request lineage The initiating request and purpose, linked to authenticated originator and decision records
Operations and resources Supported verbs and canonical resource identifiers or checkable selectors
Source and output constraints Permitted views, derivations, disclosures, recipients, and provider or tool destinations



<!-- page 11 -->

Agent Identity and Delegated Authority
Draft 0.1   |   11
Grant element Required interpretation
Credential bindings Permitted credential handles and operations, without embedding their secret material
Validity and status Start, expiry, authority epoch, revocation dependencies, and permitted status freshness
Delegation lineage Parent and root references, allowed recipients, remaining depth, and attenuation rules
Budget and concurrency Enforceable aggregate limits for calls, spend, fanout, or concurrent work
Policy and acceptance gates Applicable policy version, supported constraints, and any required separate decisions
Attenuation and aggregate limits
A child grant must remain within every applicable ancestor's effective authority. It cannot
add operations, broaden resources, disclose to a new destination, extend validity, exceed a
shared budget, or enable further delegation that its parent prohibits. Revoking an ancestor
invalidates descendants under the declared status policy.
The constraint language should begin with a small, versioned set of rules whose
containment can be checked. If the host cannot establish that a proposed child is narrower,
it denies that delegation or obtains a new grant from an authority allowed to decide it.
Arbitrary natural-language policies cannot be safely compared as mathematical sets
without a defined interpretation.
Delegation must not multiply a budget. Sibling workers consume reservations or counters
under the originating task's limit. Parallel requests require atomic reservation or equivalent
coordination. A budget stated in a token but never checked by the consuming services is
descriptive metadata rather than an enforced limit.
Resource resolution happens before authorization and remains tied to the authorized object
at execution. Paths need normalization, symlink treatment, and a rule for races between
check and use. Repository operations can bind a repository identity, branch or revision, and
exact proposal digest when the policy requires approval of a specific change. A broad label
such as project or coding cannot silently expand into unrelated files or accounts.
Checks at the point of action
The enforcement sequence authenticates the caller and channel, resolves current
membership and authority, validates the grant and its ancestors, resolves the target,
applies source and destination constraints, reserves shared limits, and executes the
permitted operation. It then records the observed outcome and releases or settles
reservations. A queued job is checked again when it begins; admission to a queue does not
freeze permissions indefinitely.
For consequential external effects, the enforcing service durably records the authorized
intent and stable operation identifier before dispatch. It then records attempts and
observed outcomes. A crash after dispatch leaves an unresolved attempt for reconciliation,



<!-- page 12 -->

Agent Identity and Delegated Authority
Draft 0.1   |   12
rather than an unrecorded success or an assumed safe-to-repeat failure. If the required
intent record cannot be persisted, that operation is not dispatched under this profile.
Current policy and containment state can narrow an existing grant. A worker cannot pin an
old permissive policy to bypass a later restriction. A policy change that expands authority
requires a newly admitted grant or decision; it does not retroactively widen every existing
token. Definition revisions and current authorization state are recorded separately so this
behavior is auditable.
Sender and audience restrictions reduce the usefulness of a copied token, provided the
enforcing service verifies the binding and prevents proof replay. OAuth security guidance
describes both controls and their limits when a client or its keys are compromised. This
proposal requires a concrete profile to state the binding and replay mechanism rather than
relying on a token's signature alone. [R8]
Network retries need stable operation identifiers and service-specific idempotency or
reconciliation. An uncertain external result is recorded as unknown until resolved. The
architecture must not promise exactly-once side effects across arbitrary remote services.
Grant validity controls whether an attempt is authorized; outcome reconciliation determines
whether its effect occurred.
Separate permissions for separate decisions
Research, source access, skill invocation, proposal creation, testing, acceptance,
publication, and identity administration are separately grantable operations. A standing
policy can combine the ones appropriate for a workflow. The existence of a test result or a
signed proposal does not itself authorize acceptance or release.
An owner may preauthorize a dream to accept a bounded class of memory corrections or
skill changes. That permission needs explicit scope and an acceptance rule. Authority to
change controller keys, recovery policy, credential ownership, or the issuer's own limits
requires a distinct administrative grant. A worker cannot create that authority by revising
its instructions.
7 Communication within and between Souls
Bob as the normal external endpoint
External participants normally address Bob's Soul identity. Bob's endpoint authenticates the
peer, applies admission policy, and routes the task to permitted internal members. The
response is attributable to Bob, with internal contributors retained in the appropriate audit
scope. External callers do not need to track Bob's current process names, harness versions,
or worker topology.
Bob's outbound authority controls which peer may receive which task and data. The
recipient separately controls its own execution, tools, and provider use. Alice's permission
to request work from Bob does not authorize use of Bob's credentials. Bob's ability to send
material does not grant Alice additional rights in her environment. Both parties must admit
the collaboration under their applicable policies.



<!-- page 13 -->

Agent Identity and Delegated Authority
Draft 0.1   |   13
Instructions carried in peer messages are authenticated requests from that peer. They do
not become owner directives simply because the peer is known or the channel is encrypted.
Forwarded content retains the identity of its source and its classification. Requests to widen
scope return to the authority permitted to make that decision.
Exposed specialists
Bob can deliberately expose a logical capability such as code review or an internal agent
such as reviewer. The endpoint binding identifies Bob, the exposed capability, permitted
callers and operations, routing authority, validity, and revocation rules. The address should
survive ordinary replacement of the underlying runtime. The serving workload proves that it
currently holds the delegated endpoint authority.
Direct delivery can connect a peer to the specialist without passing every payload through a
central router. The specialist still requires admission, scope checks, disclosure controls, and
an attributable action record. The direct route must not create an unrestricted entrance to
Bob's other members, memory, tools, or credentials. Further delegation is disabled unless
the grant permits it.
If several endpoints can issue responses for one task, the task contract must identify which
responses are proposals and which can finalize an external commitment. Cancellation,
duplicate delivery, and competing workers need a consistent task authority. This paper
defines who may perform those transitions; the communications paper will define their
message and delivery semantics.
Remote members
A worker executing on another host can be a member of Bob only after enrollment under
Bob's controller and the declared remote execution profile. It receives a separate
installation or workload identity and bounded grants. Merely calling an external agent a
specialist does not enroll it as Bob.
Remote membership also changes the trust and data-disclosure boundary. The owner must
accept the remote host's enforcement assumptions and the provider destinations it may
use. When those assumptions cannot be verified or are unsuitable, the participant should
be treated as an external collaborator with a narrower exchange. A logical Soul boundary is
not proof that all of its plaintext stays on one machine.
Conversation participation authority
Permission to communicate needs a participation policy, especially on third-party platforms.
A Soul may be allowed to answer a question without being allowed to initiate unrelated
conversations, repeatedly follow up, mention additional people, or continue a thread
indefinitely. The grant should distinguish listening, replying, initiating, escalating, and
finalizing, and it should bind the permitted account, conversation, recipients, and disclosure
scope.
Quiet, chatty, and goal oriented are proposed presets for this policy. They are independent
of the model's reasoning effort. Quiet favors replies when addressed and necessary
updates. Chatty permits more conversational contributions within the same bounded
authority. Goal oriented favors exchanges that advance an explicit task and closes or waits



<!-- page 14 -->

Agent Identity and Delegated Authority
Draft 0.1   |   14
when its completion condition is met. Each preset needs concrete limits on initiation,
frequency, messages, elapsed participation, unanswered follow-ups, and aggregate cost.
An authorized purpose can include bounded social conversation. The policy need not turn
every exchange into a work task. Account, platform, and task-wide caps also apply so
starting another thread cannot reset the Soul's overall limits.
A decision model can maintain a structured account of the conversation's purpose,
requested outcome, unresolved questions, commitments, and progress. It can recommend
reply, ask, wait, hand off, or close. Inferred purpose must be labeled with evidence and
uncertainty; it cannot authorize a new objective, new recipient, or increased privilege. The
trusted communication service enforces hard limits and stop rules independently of the
model's recommendation.
Limits apply to Bob across all participating harnesses, including delegated subagents. Four
workers must not each receive a fresh allowance to continue the same thread. The service
checks conversation state before sending, suppresses duplicate or circular agent
exchanges, respects a participant's request to stop, and requires an authorized reopening
event after closure. A new relevant message can trigger reconsideration within policy; the
model should not generate endless self-triggered continuations.
Waiting records the event or condition that can justify reconsideration. Bob's own message
or its platform echo cannot alone trigger another reply. Repeated acknowledgments and
paraphrases do not count as meaningful progress. Closure can happen locally without
sending a final message; a closing message consumes the same permission and budget as
any other send. Quiet mode still permits reports required by the authorized task, such as a
material failure or completion notice.
The communications paper will define these presets, state transitions, decision inputs, and
platform mappings. The identity contract supplies the authenticated speaker, delegated
participation scope, shared budget, and attributable decision record. A change to a preset
cannot silently expand a previously granted right to contact people or disclose information.
8 Attribution and evidence
Action records
Each consequential action should have a structured receipt created or corroborated by the
enforcing service. It records the initiating request, authorizing decision, represented Soul,
executing member and runtime, credential binding, effective policy, target, operation, and
observed result. Sensitive values can be represented by protected references and digests
when full disclosure is unnecessary.
The receipt distinguishes an authenticated originator from a claimed upstream originator. A
peer may truthfully or falsely report that another person requested work. The authenticated
forwarding peer can be recorded as the source of that assertion, but the upstream request
becomes verified authority only through an accepted request or delegation chain.
The record distinguishes what was requested from what was attempted and what the
external service confirmed. A tool returning success, a worker declaring success, and a
separately observed side effect are different evidence. The receipt should identify its



<!-- page 15 -->

Agent Identity and Delegated Authority
Draft 0.1   |   15
evidence source and uncertainty. A signed receipt authenticates its issuer and contents; it
does not prove that every assertion in the contents is correct.
Attribution field Example in a proposed coding workflow
Originator the owner requests a change, or Alice sends an admitted task
Authorizer Bob's owner-approved policy permits a bounded repository change
Represented identity Bob's stable Soul identifier
Contributor Bob's coding member develops the patch; a reviewer assesses it
Executor A specific admitted runtime or commit service performs the operation
Credential binding Bob's declared access to the intended repository and App installation
External actor The actual bot or account identity reported by GitHub
Artifact attribution The author, committer, and relevant contribution metadata in the commit
Execution conditions Resolved harness, adapter, model/provider, tools, and effective permissions
Result evidence Commit identifier, service response, retained check results, and unresolved effects
The table describes an example, not an account configuration that this paper has created. If
the orchestrator performs the commit, the record names the orchestrator as executor while
preserving the members' contributions and Bob's Soul identity. No invented public bot
account is required for the model.
The repository's accepted ADR-0815 selects Soul co-author attribution for its GitHub
publication path while retaining the App as author and API actor and GitHub as committer
and signer. The general receipt model preserves that path-specific decision. It does not
require every service to display Bob as its native authenticated actor. [R5]
Provenance and retention
Provenance links actions to source versions, proposals, decisions, and resulting artifacts.
W3C PROV-DM distinguishes entities, activities, agents, attribution, and delegation
relationships, providing a useful vocabulary for a portable representation. The Soul format
can preserve those relationships without requiring one graph database. [R13]
The authoritative audit service should restrict writes independently of ordinary agent
content. Hash chains or signed checkpoints can make changes detectable relative to a
retained checkpoint. They cannot establish that an unobserved event was logged or that a
compromised issuer told the truth. Retention policy must state which records exist, which
were intentionally excluded from an export, and which evidence is unavailable.
Public attribution should disclose only what the recipient needs. Internal member names,
owner account identifiers, private task details, and full delegation histories may remain



<!-- page 16 -->

Agent Identity and Delegated Authority
Draft 0.1   |   16
protected. An authorized verifier can inspect additional evidence through bounded access.
Redaction must preserve a statement of what can and cannot be independently verified.
9 Identity through change and recovery
Lifecycle operations
An operation on a package must state what happens to identity and active authority. The
same archive can support backup, transfer, or template distribution, but those uses have
different enrollment requirements. A recipient should not have to infer the intended
operation from a filename.
Operation Soul identity Authority treatment
Rename or replace a
harness Preserve
Record new display or execution
binding; issue fresh runtime authority
as needed
Rotate an operational
key Preserve
Authenticate the transition and retire
the old binding under the status
policy
Instantiate a template Create new
Enroll a new controller relationship
and local credentials; retain publisher
provenance
Fork a continuing life Create new with parent lineage
Establish new active authority;
preserve historical authorship and
source restrictions
Restore a backup Preserve intended subject
Revalidate current control state and
enrollment; do not restore expired or
revoked grants
Transfer to another
host Preserve
Enroll the destination and retire or
fence the former installation
according to the profile
Add an intentional
replica Preserve
Enroll a distinct installation with an
explicit concurrency and conflict
policy
Change controller Preserve when the transition authorizes continuity Replace the control relationship and review account bindings, grants, and peer trust
Retire the Soul Preserve a historical tombstone
End new operational authority; retain
permitted historical verification
material
Internal member identifiers are qualified by the Soul identifier. Runtime credentials
additionally bind the installation and execution. A member's display name can be reused,
but a retired member identifier must not silently assign its old grants to a new worker.
Reassigning a continuing logical role is an explicit event with new execution bindings.



<!-- page 17 -->

Agent Identity and Delegated Authority
Draft 0.1   |   17
Template instantiation and forks preserve provenance of inherited artifacts. If changing an
identifier changes signed package bytes, the new instance receives a new revision. The
publisher's signature continues to authenticate the original template. Historical
contributions remain attributed to their original participants rather than being rewritten as
work performed by the new Soul.
Transfer and concurrent copies
The initial deployment profile should support one active installation authority for a Soul. A
transfer records the source state, prepares the destination, verifies its enrollment and
credential bindings, and makes an explicit authority transition. The transition should be
recoverable after interruption without creating an unnoticed second writer.
Preventing concurrent use requires enforcement by the services that accept actions. A new
installation epoch can fence an older one at the broker. An exclusive lease works only
where its validity is checked. Tokens already issued to downstream services can remain
usable until those services revoke or expire them. The transfer receipt must state the
cutover, any overlap window, and the remaining authority that could not be withdrawn
immediately.
Copy detection on one host cannot prove that another copy is absent elsewhere. Likewise, a
signed transfer statement cannot stop a disconnected host that still holds independently
usable credentials. Stronger guarantees need a shared authority or resource-side fencing
and compatible credential lifetimes. The format should report unsupported guarantees
clearly rather than treating a successful copy as exclusive control.
Intentional replicas use separate installation keys and defined write scopes. The policy must
identify exclusive operations, conflict handling, task ownership, and shared budgets. During
a network partition, the implementation follows an explicit availability policy. It must not
promise both immediate global revocation and unrestricted offline authority. The first
profile can defer active replicas while preserving the identifiers needed to add them later.
Recovery and status freshness
Recovery depends on an authority established before the loss: a protected recovery key, an
enrolled controller recovery process, or another specified trust mechanism. The recovery
process rebinds current authority, advances the appropriate epoch, and preserves the Soul
identifier and audit history. An archive with an identifier and self-signed keys is insufficient
evidence of continuity when the prior trust binding has been lost.
If no accepted recovery basis remains, the implementation can preserve accessible
historical content and create a new identity with a disclosed lineage claim. It cannot
honestly claim authenticated continuity with the former Bob. Separately, encrypted life may
remain inaccessible if all data-decryption recovery paths are lost. Identity recovery and
data recovery need independent, tested arrangements.
Every verifier needs a status-freshness contract: which operations require an online check,
how long cached authority may be used, and which operations are permitted offline. Offline
grants have bounded validity and cannot promise immediate knowledge of remote
revocation. OAuth introspection's security discussion describes the corresponding exposure
introduced by caching authorization status. [R17]



<!-- page 18 -->

Agent Identity and Delegated Authority
Draft 0.1   |   18
Clock rollback, restoration of an old verifier cache, and loss of the last trusted control
checkpoint must not silently extend authority. A profile can use protected monotonic state,
online revalidation, or another documented mechanism. If it cannot establish freshness
after recovery, it withholds operations requiring that assurance until trust is reestablished.
Historical signature verification uses the key status and evidence applicable to the event. A
later revocation does not automatically rewrite every earlier event as invalid. Conversely, a
compromised key cannot establish a trustworthy historical signing time merely by including
an old timestamp. Receipts must state what temporal and status evidence supports the
conclusion.
10 Knowledge dreaming and containment
Identity in accumulated learning
Local retrieval and the knowledge graph let Bob's members use accepted experience across
harnesses. Identity records make that learning attributable: the source Soul, contributing
member, original evidence, transformation, acceptance decision, and affected revision can
be retained. A claim from another Soul should remain an external claim until Bob's
knowledge policy accepts its intended use.
Protected primitives and non-curated sources remain encrypted at rest and accessible
through the broker's scoped tools. Decryption authority and agent-readable projections
require an actual enforcement boundary. Permission to query a summary does not
authorize raw source disclosure. A memory write does not become a standing instruction
merely because a model generated it or another worker repeated it.
Source restrictions follow relevant derivatives, including summaries, embeddings, graph
assertions, task artifacts, and messages. Provider choice is part of the disclosure decision.
Local storage does not imply that selected material stays local when an execution sends it
to a remote model. The broker or equivalent enforcement service controls the permitted
destination; a model's preference cannot widen it.
Once permitted plaintext reaches a recipient, the system cannot guarantee that the
recipient forgets it. Revocation limits future access and controllable copies. Export selection
therefore needs to consider the full source and derivative relationship before a package is
shared.
Dreams as delegated work
A dream is an admitted workflow with an execution identity, source scope, budget, and
acceptance policy. It can use several members to inspect experience, test a skill, compare
routing choices, and propose corrections. Its record binds the selected evidence and
relevant authority baseline. A routine dream does not receive administrative authority
merely because it is maintaining the Soul.
Dreams can look for drift from current authorized intent, unexpected disclosure, repeated
boundary violations, misleading attribution, or use of an obsolete grant. They should
distinguish a quoted attack from adopted instructions and an unresolved suspicion from a



<!-- page 19 -->

Agent Identity and Delegated Authority
Draft 0.1   |   19
verified incident. An owner's valid change of objective must be evaluated against the
current decision rather than classified as misalignment with an old preference.
Accepted learning may improve a role assignment or skill without changing the Soul
identity. Changes to delegation policy, controller bindings, trusted keys, credential
ownership, or recovery arrangements follow their own administrative authority. A dream
may prepare a reviewable proposal when permitted, but successful evaluation alone cannot
authorize that proposal's activation.
Quarantine as an enforced state
Quarantine targets an explicit scope such as a session, member, grant subtree, source
contribution, installation, or entire Soul. The supervisor and brokers deny newly prohibited
actions, reconsider queued work, and contain accessible projections under the configured
policy. A quarantined worker cannot clear its own status through ordinary memory or
configuration writes.
Evidence is retained with access restrictions and a reasoned finding. Diagnostic work
receives separate bounded authority. Release requires the designated review or acceptance
decision and, where needed, fresh runtime enrollment. Narrow containment is preferable
when evidence supports it; broader suspension can be a declared precaution when the
affected scope is uncertain.
Revocation cannot undo completed external effects. In-flight or ambiguous effects remain
recorded for reconciliation. Derived knowledge and downstream tasks may also need
review if they depended on the quarantined source. Active quarantine is current authority
state outside the rollback domain of package content. Export choices may omit private
diagnostic details but cannot clear an applicable restriction. A destination that cannot
establish the current status withholds affected activation.
11 Agent Stores and evaluation identity
An Agent Store distributes releases and publishes claims about them. The publisher,
evaluator, store operator, installing owner, and instantiated Soul are distinct identities. A
publisher signature authenticates a release under the recipient's trust policy. Installation
establishes a separate local control relationship and explicit execution authority.
The default product should be a reusable template with selected skills and curated
knowledge. Each installation receives a new Soul identity. A continuing-life transfer or
inherited-life fork must declare that operation and its data scope. A store cannot silently
transfer the original owner's account access or make itself a controller of the recipient's
private life.
Evaluation evidence binds the exact artifact digest, definition revision, exported knowledge
checkpoint, composition, execution profile, permissions, suite, evaluator, time, and
measured outcomes. The listing distinguishes publisher-produced evidence from
independent assessment. It also identifies incomplete runs, unavailable evidence, and
changes that make earlier results stale.



<!-- page 20 -->

Agent Identity and Delegated Authority
Draft 0.1   |   20
For a composite Soul, evaluations cover individual capabilities and the combined workflow.
A strong coding worker does not establish that task routing, handoffs, review, and external
communication behave correctly together. Participation tests should include the
communication preset, message budgets, closure behavior, duplicate suppression, and
resistance to conversations that repeatedly provoke another reply.
Routine dreams can produce local evaluation records. Publishing a selected report requires
a separate disclosure and publication grant. Private conversations, raw source evidence,
and quarantine material are not automatically sent to the store. Public evidence should use
the tested distributable candidate or clearly identify that it describes a private evolving
instance.
Reputation belongs to a defined subject and context. Template lineage can help a recipient
understand inherited provenance, but it does not transfer every performance or trust claim
to a new instance. A change of controller, composition, knowledge, or permissions can
materially change the basis on which another party trusts the same Soul identifier. The
listing should expose relevant changes without turning one score into a claim of universal
safety.
W3C Verifiable Credentials provides an issuer, holder, and verifier model for portable
claims. Its trust model leaves the verifier's decision about which issuers to trust for which
purposes outside the data model. An evaluation credential could use such a representation,
while the store and recipient still need an explicit interpretation of the test and its scope.
[R12]
12 Interoperability and implementation profiles
Reuse established mechanisms
The Soul architecture needs a common semantic model and concrete profiles. It should
reuse suitable authentication, workload identity, token, and provenance mechanisms while
specifying the additional Soul relationships. Naming several standards is insufficient to
make implementations interoperable; a profile must choose versions, claim mappings,
validation rules, and negative test vectors.
Mechanism Relevant foundation Required Soul-specific contract
DID Core
Subject and controller relationships
and purpose-qualified verification
methods
Identifier mapping, enrollment,
resolution, status freshness, and
selected method behavior
OAuth Token Exchange Subject and actor representation for delegated service access Effective grants, resource constraints, member binding, and acceptance authority
OAuth security
guidance
Audience restrictions, sender
binding, and replay considerations
Supported token profile, enforcement
placement, lifecycle, and restart
behavior
SPIFFE Workload identifiers and verifiable identity within a trust domain Mapping from a workload to an admitted Soul member and its separate permissions



<!-- page 21 -->

Agent Identity and Delegated Authority
Draft 0.1   |   21
Mechanism Relevant foundation Required Soul-specific contract
Verifiable Credentials Portable issuer statements that a verifier can assess Evaluation subject, evidence scope, disclosure policy, and issuer trust
W3C PROV Relationships among agents, activities, entities, and provenance Durable Soul records, access restrictions, and export semantics
SPIFFE identifies workloads within a trust domain and defines verifiable identity documents
issued under that domain's authority. That makes it relevant to remote or enterprise
executor enrollment. A deployment would still need to bind the workload to the correct Soul
and evaluate its grants. Being authenticated by a trusted workload issuer does not make
every workload an administrator of Bob. [R9]
A small local baseline
The first profile should support one owner-controlled host, one active installation authority
per Soul, and one or more admitted harness runtimes. A protected supervisor-to-broker
channel supplies caller identity. The broker maintains opaque grants, shared limits, current
status, and action receipts. Local enrollment anchors the Soul to the controller. No global
registry or distributed consensus service is required for this configuration.
The baseline should make identity and acceptance semantics portable even when native
session formats are not. The package records member roles and execution requirements;
the destination provisions compatible runtimes and enrolls fresh executions. A retained
transcript can be evidence without guaranteeing that another harness can resume it as an
identical native session.
Optional extensions
A remote execution profile adds workload enrollment, protected transport, remote-host
assumptions, and explicit data destinations. A peer collaboration profile adds external Soul
authentication and recipient admission. An exposed-specialist profile adds endpoint
delegation with equivalent enforcement. A coordinated-replica profile adds shared
authority, fencing, conflict handling, and partition behavior.
An implementation claims only the profiles it supports. If a required restriction cannot be
enforced, the operation is refused under that profile or the owner deliberately selects a
documented mode with different guarantees. Silent fallback to unrestricted shell access,
another credential, or a different provider would make the recorded authority misleading.
13 Existing contracts and the specification gap
The repository review for this draft used the current default branch head verified on 20
October 2026, commit 31619aaebbcfb19df92257851f6aed6ed93a326e. The following
observations describe that snapshot. Proposed requirements elsewhere in the paper do not
imply that these extensions have already shipped.
The public identity contract defines reusable entries, child-process record operations,
daemon routes, and wire formats. It expressly separates successful presence verification
from enrollment, authorization, and permission to mutate. The document also retains a Still



<!-- page 22 -->

Agent Identity and Delegated Authority
Draft 0.1   |   22
landing section, so it is evidence of an evolving contract rather than proof that every
planned extraction step is complete. [R1]
The current communications vouch token includes an audience, account, Agent ID, parent,
issue and expiry times, and nonce. Its declared audience is agent-comms and its lifetime is
bounded to five minutes. That is an existing integration mechanism. Its claim shape does
not independently describe all of the persistent Soul, member, runtime, session, and
delegated-operation relationships proposed here. A migration must define their mapping
rather than reinterpret the existing parent field by assumption. [R14]
The delegation ledger implements exact, single-use approval for named GitHub operations:
issue comments, issue state changes, and review requests. It binds a Soul, operation digest,
expiry, and presence approval, and it consumes the approval before execution. Approved
grants are held in memory and disappear on restart. This is useful precedent for action-
bound authority, while general member delegation and standing grants require additional
contracts. [R2]
The keyd protocol separates daemon policy from retained keys and uses purpose-specific
grants and presence assertions. Its documented spent-nonce cache is in memory, so a
restart permits reuse of an already spent grant until that grant expires. The new profile
must state its own replay and restart guarantee explicitly; it cannot inherit a claim of
durable replay prevention from the existing format. [R4]
Credential documentation identifies cooperative confinement limits and some best-effort
mint receipts. Owner-statement documentation distinguishes signature validity from trusted
owner approval and describes supported challenge paths. Separately, the owner-decision
trust-record document explicitly labels that infrastructure disabled and the future
installation ceremony unbuilt. These are materially different readiness states and should
remain separate in planning. [R3] [R15] [R16]
The next specification work is therefore a set of explicit extensions: stable composite
membership, qualified identities, caller-bound grants, current authority state, data-
destination constraints, direct endpoint delegation, lifecycle cutover, and evidence covering
the complete composition. Existing wire formats, attribution decisions, and denial behavior
need compatibility fixtures and deliberate migrations.
14 Acceptance scenarios
These scenarios define proposed observable behavior for future implementations. They are
a conformance plan, not test results from a completed system. Each implementation should
identify the profile under test, the enforced boundary, the expected decision, and the
retained evidence.
Scenario Required observable result
1 Rename Bob and replace its
coding harness
Soul identity and historical attribution persist; new execution
bindings are recorded
2 Run Bob with one harness and
then four
The same identity model works; members have qualified identities
and shared policy limits



<!-- page 23 -->

Agent Identity and Delegated Authority
Draft 0.1   |   23
Scenario Required observable result
3 Copy Bob's identifier into an
unrelated process Authentication fails without valid enrollment and caller binding
4 Reuse worker names in two
Souls A grant to one Soul's member never authorizes the other
5 Retire a worker and create
another with the same display
name
Old grants remain invalid; new membership and runtime authority
are required
6 Run named subagents with
indistinguishable credentials
The host reports their shared security boundary and does not claim
separate isolation
7 Present a package signature as
a runtime grant
Verification rejects the wrong purpose or audience; no authority is
acquired
8 Expand resources or expiry in a
child grant
Delegation is refused unless a separately authorized issuer grants
the expansion
9 Fan out work to several
members
All children consume the originating task's aggregate budget and
concurrency limits
10 Change a symlink or target
after authorization Execution remains bound to the authorized object or is refused
11 Copy a grant to another caller
or service Caller binding or audience validation rejects its use
12 Restart a service after a grant
is spent
Behavior matches the declared replay profile; no stronger
guarantee is advertised
13 Revoke a parent while work is
queued
Descendants and queued actions are reconsidered under the
current status policy
14 Use an unapproved provider
for protected knowledge
Disclosure is blocked or the profile is reported unavailable before
exposure
15 Send an internal finding that
claims owner approval The finding cannot replace the required authenticated decision
16 Expose Bob's reviewer directly
to Alice
Only the delegated capability is reachable; unrelated memory and
credentials remain outside scope
17 Request external work without
recipient admission
The peer's local operations remain unauthorized until its own policy
admits them
18 Let four harnesses reply to
one third-party thread
One Soul-level participation policy and shared message budget
govern the thread
19 Recommend continuing after
a conversation is closed
Sending is denied until an authorized reopening event; the decision
model cannot override the stop rule
20 Restore a snapshot containing
revoked grants or old trust state Content may restore; obsolete authority does not reactivate
21 Transfer while the former
installation still runs
Cutover and fencing are enforced where supported; remaining
token validity and overlap are disclosed



<!-- page 24 -->

Agent Identity and Delegated Authority
Draft 0.1   |   24
Scenario Required observable result
22 Start an undeclared second
copy
The copy receives no implicit active-writer authority; declared
replicas follow their separate policy
23 Instantiate a template twice or
fork a life
New identities are created; original signatures and contributions
remain historical provenance
24 Recover with valid and
missing recovery authority
Valid recovery records continuity and new bindings; missing
authority leaves continuity unestablished
25 Roll back a clock or cached
status
Expired or stale authority is not silently extended; required
freshness is reestablished
26 Let a routine dream alter its
controller or grant issuer
Proposal access does not authorize activation of administrative
changes
27 Quarantine a member with an
uncertain external operation
Future prohibited actions stop; evidence and unresolved effects
remain available for reconciliation
28 Publish evaluations for a
different composition or
permission set
The listing distinguishes the tested conditions and cannot present
unqualified coverage
29 Let two chatty Souls exchange
repeated acknowledgments
Enforced follow-up, no-progress, and message limits stop the
exchange without relying on either model to volunteer silence
30 Transfer a quarantined Soul
with private diagnostics omitted
The applicable restriction persists; absent diagnostic details do not
establish clearance
31 Lose contact with a remote
member until its lease expires
Protected operations under that lease are refused; the host does not
claim the remote process stopped
32 Backdate a new receipt using
a compromised key
The claimed timestamp is insufficient to prove pre-compromise
signing; temporal assurance is reported accurately
15 Decisions and implementation path
The recommended first implementation uses one active local authority per Soul, opaque
local grants, trusted runtime admission, protected credential and source access, explicit
external messaging grants, and structured receipts. It supports several harnesses without
requiring distributed infrastructure. The following decisions are still needed before this draft
becomes a wire-level specification.
Decision Proposed direction
Identifier and existing Agent ID
mapping
Preserve current identities through an explicit compatibility
mapping; define member and runtime scopes separately
Control descriptor and authority
status
Version the schemas, transition policy, freshness requirements, and
rollback protection
Grant constraints Start with a small checkable language and deny unsupported critical restrictions
Authentication and serialization Select concrete maintained profiles, algorithm policy, canonicalization where needed, and negative vectors



<!-- page 25 -->

Agent Identity and Delegated Authority
Draft 0.1   |   25
Decision Proposed direction
Runtime isolation Publish capabilities and limitations for each host mode and native harness integration
Transfer and recovery Define durable cutover, downstream-token limits, recovery authority, and interruption handling
Conversation participation Share grant semantics and aggregate limits; define presets and decision logic in the communications paper
Store attestations Bind exact release and execution conditions, evaluator identity, disclosure policy, and stale-result rules
Implementation should begin with a shared glossary and fixtures that distinguish Soul,
member, installation, runtime, and session identities. The next increment should register
multiple local harnesses and enforce caller-bound access to protected operations, including
a deliberately hostile worker that tries to bypass the broker. A third increment should
exercise delegation, shared budgets, purpose-qualified signatures, restart behavior, and
revocation under concurrency.
Transfer, restore, key rotation, and recovery should then be tested before portable
authority is offered as a product guarantee. Peer communication and exposed specialists
can follow once both parties' admission and disclosure checks are defined. Routine dreams
and store publication should consume the same identity and receipt contracts, with
evaluations against the assembled release and its advertised permissions.
The companion communications paper should carry forward a concrete conversation
record: authorized purpose, evidence for inferred purpose, participants and roles,
unresolved questions, commitments, preset, message and time budgets, last meaningful
progress, current disposition, and permitted reopening events. A decision model can advise
the next conversational action. The communication service owns the enforceable send and
stop rules. This allows Bob to reason deeply while remaining quiet, participate socially
within a chatty preset, or stop promptly when a goal has been reached.



<!-- page 26 -->

Agent Identity and Delegated Authority
Draft 0.1   |   26
References
Repository references are pinned to the reviewed commit. Standards references identify their published
documents or official specification pages. The architectural contracts and acceptance scenarios in this
draft are proposals informed by these sources and the design discussion.
[R1] qwts. Identity public contract.
Repository / docs/identity-contract.md
[R2] qwts. Delegation grants implementation.
Repository / delegation-grants.mjs
[R3] qwts. Soul credentials.
Repository / docs/soul-credentials.md
[R4] qwts. Keyd grant owner presence and trust bootstrap protocol.
Repository / docs/keyd-protocol.md
[R5] qwts. ADR 0815 The Soul is a Git co author.
Repository / docs/decisions/ADR-0815-the-soul-is-a-git-co-author.md
[R6] W3C. Decentralized Identifiers DID Core version 1.0. Recommendation 19 July 2022.
www.w3.org/TR/2022/REC-did-core-20220719/
[R7] IETF. RFC 8693 OAuth 2.0 Token Exchange. January 2020.
www.rfc-editor.org/rfc/rfc8693
[R8] IETF. RFC 9700 Best Current Practice for OAuth 2.0 Security. January 2025.
www.rfc-editor.org/rfc/rfc9700
[R9] SPIFFE. SPIFFE Identity and Verifiable Identity Document.
SPIFFE / Identity and Verifiable Identity Document
[R10] GitHub. Authenticating as a GitHub App installation.
GitHub Docs / Authenticate as an App installation
[R11] Git. Git commit documentation.
git-scm.com/docs/git-commit
[R12] W3C. Verifiable Credentials Data Model version 2.0. Recommendation 15 May 2025.
www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/
[R13] W3C. PROV DM The PROV Data Model. Recommendation 30 April 2013.
www.w3.org/TR/prov-dm/
[R14] qwts. Soul token implementation.
Repository / identity/vouch.mjs
[R15] qwts. Owner statements.
Repository / docs/owner-statements.md
[R16] qwts. Owner decision trust records disabled.
Repository / docs/owner-decision-trust.md
[R17] IETF. RFC 7662 OAuth 2.0 Token Introspection. October 2015.
www.rfc-editor.org/rfc/rfc7662
