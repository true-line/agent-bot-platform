---
Status: Frozen
Doc-Type: paper
Owner: product-owner
Last-Reviewed: 2026-11-05
---

# Create Agent Watchtower Whitepaper


> Converted from `Create Agent Watchtower Whitepaper.pdf` (7 pages) with scripts/pdf2md.py — PDF text extraction is best-effort; curate before treating as normative. The original PDF is authoritative.


<!-- page 1 -->

You said:
Worked for 14m 24s
ChatGPT said:
Created Agent Watchtower — A Little Snitch for Agents, version 0.1: a 16-page white paper with
approximately 6,100 words, an architecture diagram, a worked scenario, implementation acceptance
criteria, and 15 primary references.
PDF for reading: agent_watchtower_white_paper_v0_1.pdf
Editable Word document: agent_watchtower_white_paper_v0_1.docx
ZIP containing both: agent_watchtower_white_paper_v0_1.zip
The central argument
The paper makes your expectation of the provider explicit:
That gives “trusted skill” a substantive meaning. The provider identifies the resources the skill depends
on, evaluates them for their intended use, publishes verifiable assurance, and maintains a way to
update or withdraw that assurance.
For example, if a trusted provider supplies a development setup skill that depends on a third-party
installation guide and script, the providerʼs assurance should identify those dependencies and cover
their use. The owner should be able to understand that relationship before approving the skill.
The proposed firewall then checks whether the actual resource and requested action still satisfy the
conditions of the approval.
Want to create a white paper discussing creating the Little Snitch
for agents.  Solving a problem with too restrictive web approvals
and approving for less safe website when the contents change of a
remote link for example in untrusted skills.  Even trusted skills may
refer to 3rd party untrusted websites though.  So trusted skills or
primitives should mean the peocider like doe example Apple
assures that the 3rd party links are safe and vouches foe them.
A provider-assured skill carries responsibility for its declared operational dependencies,
including those hosted by third parties.



<!-- page 2 -->

How it reduces repetitive approvals
The design preserves useful standing permissions while checking for changes that matter:
A changed page does not automatically need another dialog. A change that invalidates assurance
or expands authority needs renewed evaluation. That distinction is essential to making this usable.
Little Snitch provides a relevant foundation: its connection alerts create reusable rules, and its Internet
Access Policy lets developers explain the purpose of connections through metadata associated with a
properly signed application. The paper extends those ideas to agent identity, skill versions, dependency
assurance, and permitted actions.
What “vouching for a third party” would require
The paper proposes a signed Resource Assurance Statement that records:
Who is making the assurance, and which signing authority they use.
What is covered, including the skill release and specific dependency versions or content
digests.
What use was reviewed, such as reference material, installation instructions, or executable
code.
Which further dependencies are included, and where coverage ends.
What evaluation was performed, under which review policy and runtime assumptions.
Situation Proposed behavior
The same approved skill uses the same endorsed
dependency within its existing permissions
Proceed without another prompt.
A public reference page changes, and the task already
permits reading it as external data
Continue under the existing reading policy.
A provider publishes a newly reviewed data snapshot
within an approved data stream
Verify the new assurance and continue if the existing
rule covers it.
An accepted skillʼs instructions, executable
dependencies, or requested capabilities change
Stage the change for acceptance.
A familiar page introduces an uncovered script or
requests a private-file upload
Hold those operations and explain the specific change.
A provider withdraws assurance for an artifact Invalidate dependent decisions and prevent further
covered execution.
Overview+2




<!-- page 3 -->

How long the assurance remains valid, and how it can be withdrawn.
This creates a meaningful distinction between publisher verified and provider assured. A valid
signature establishes evidence about origin and integrity; evaluating whether the content is appropriate
requires an additional claim and trust policy. Sigstoreʼs documented security model makes this
limitation explicit.
Your Apple example is included as a hypothetical assurance program: Apple, or another accepted
provider, could explicitly endorse third-party dependencies used by certified agent skills. The paper
distinguishes that proposed responsibility from Appleʼs current documented Gatekeeper checks, which
concern developer identity, notarization against known malicious content, and software integrity.
How it handles a link whose contents change
The paperʼs strongest technical requirement is verify and deliver the same representation.
Checking a URL, declaring it acceptable, and then letting the agent fetch it independently leaves a gap:
the second request may receive different content. The proposed broker captures the resource, verifies
the applicable assurance, and supplies that exact object to the agent or execution environment.
This builds on the integrity principle used by W3C Subresource Integrity, where an expected digest
binds a reference to particular fetched bytes. The proposed agent system adds handling for extracted
text, rendered pages, authenticated responses, and nested dependencies.
The paper also addresses cases where exact advance endorsement is impractical. A personalized
webpage or live API can operate under a constrained service contract, with runtime checks on its
requests, responses, and downstream actions. Its changing contents remain external data.
The worked example
The main scenario follows an approved environment setup skill:
1. The provider endorses a third-party guide and a particular installer.
2. The owner permits that installer to run inside a designated sandbox.
3. Repeated runs proceed quietly while the relevant conditions remain valid.
4. The guide later introduces another script and asks for an environment-file upload.
5. Watchtower detects that the new script lacks the old dependency assurance and that the upload
exceeds the existing grant.
6. The agent can continue with an eligible approved snapshot, inspect the changed guide under a
reading policy, or present the specific new operation for review.
7. A subsequent provider endorsement of the new script supplies new evidence. The upload still
requires its own applicable authorization.
Sigstore
Apple Support
w3.org




<!-- page 4 -->

The approval can therefore explain what changed, which operation is held, what information would
leave, and who would receive it.
How it fits your Soul architecture
The proposal places durable trust preferences and provider selections with the Soul, while issuing
temporary capabilities to particular harness instances, sessions, and tasks.
That supports Bob using several harnesses without making one harnessʼs approval an unrestricted
permission for every sibling. It also covers delegation: a denied operation cannot become permitted
merely because another harness, MCP server, or Soul is asked to perform it.
Enforcement belongs in a protected host broker, with operating-system controls preventing alternate
routes around it. A decision model can explain changes and help classify ambiguous content, while the
broker retains authority over credentials, permissions, and consequential actions. Research such as
CaMeL supports this separation of model behavior from capability enforcement, within its stated
assumptions.
The paper treats reduced interruptions, resistance to unauthorized actions, and acceptable overhead
as evaluation goals. It includes concrete tests for changing dependencies, scanner cloaking,
credential-bearing redirects, cross-agent bypass attempts, provider outages, and revocation.
File availability note: The completed downloads are linked above. Persistent saving could not be
completed: automatic approval review initially rejected the save as an external upload requiring
permission. After I verified the destination as your own ChatGPT Library, the retry reached the service
but returned an access-denied error, HTTP 403.
You said:
ChatGPT said:
arxiv.org
Is this general the right approach or are white papers meow for
scientific and research only.
Yes. White papers are an appropriate format for what you're doing, and they're not limited
to scientific or academic research. In fact, the technology industry has a long history of using
white papers to introduce new architectures, protocols, security models, and technical
standards.
agent_watchtower_white_paper_v0_1.pdf
PDF
agent_watchtower_white_paper_v0_1.docx
Word



<!-- page 5 -->

I think your approach is appropriate, particularly because you're proposing an interconnected
architecture rather than documenting an existing product.
The important distinction is what you're claiming versus what you've demonstrated.
Different types of technical publications
Document Primary purpose Your use case
White paper Explain a problem, propose a solution,
establish technical rationale
Agent Watchtower, Soul, Identity,
Communications
Research paper Investigate hypotheses and present
reproducible evidence
Measuring whether Watchtower reduces
unsafe actions and approval fatigue
RFC Specify a design for technical review
and eventual implementation
Agent authorization and resource assurance
protocols
Technical
specification
Define precise, interoperable behavior Soul package format, trust manifests, signed
attestations
ADR Record an engineering decision and its
tradeoffs
Why permissions belong to the Soul rather
than a harness
Position paper Advocate a direction or principle Why agent ecosystems need provider
accountability
A white paper does not need an implementation, experimental results, or peer review to be
legitimate. It does need to distinguish established facts, proposed mechanisms, assumptions,
and expected benefits.
Examples from technology history
Several influential technical ideas were introduced or explained through white papers.
Bitcoin: A Peer-to-Peer Electronic Cash System — introduced a proposed electronic cash
architecture.
The Google File System — a research paper describing an implemented distributed storage
system.
The Ethereum Whitepaper — introduced a programmable blockchain platform.



<!-- page 6 -->

These aren't all the same publication category, but they demonstrate the distinction between
proposing an architecture and publishing research about an implemented system.
What I recommend for your agent architecture
I would organize your work as a coherent series of architectural white papers.
FOUNDATIONAL ARCHITECTURE
A Trustworthy Agent Ecosystem
Agent Soul
Persistent identity, life, state and portability
Agent Identity
Delegation, credentials and attribution
Agent Communications
Coordination, boundaries and messaging
Agent Watchtower
Authorization, provenance and resource assurance
Agent Stores
Distribution, attestation and provider accountability
Agent Harness
Runtime contracts, adapters and execution isolation
RFCs → Specifications → Reference implementations
Conformance suites, security evaluations and measured results
This gives you an opportunity to establish a consistent vocabulary and architectural direction
across multiple projects.
One improvement I'd make
For Agent Watchtower specifically, I'd clearly separate three categories of statements:
1. Established problem: Agents encounter prompt injection, untrusted remote content, and
authorization challenges. These can be supported by existing security research.
2. Proposed solution: Provider-backed resource assurance, content-aware authorization,
provenance tracking, and policy enforcement.
3. Unverified hypothesis: This architecture can reduce approval fatigue while improving
security relative to existing agent permission systems.
The third category eventually deserves empirical testing. Until then, it should be expressed as
an objective rather than a proven result.



<!-- page 7 -->

I'd also emphasize that a provider's endorsement is an accountable assurance claim, not
proof that the endorsed content is safe. That's an important distinction if you're eventually
proposing a standard.
My recommendation
Continue publishing architectural white papers, but establish a common template and
versioning convention. Each should include a problem statement, threat model where relevant,
proposed architecture, trust assumptions, interoperability, alternatives considered, limitations,
and validation criteria.
Then evolve mature designs into RFCs and specifications. You can publish research papers later
when you've developed reference implementations and have measurable results.
The white papers explain why the system should exist and how it could work. The
specifications define exactly how it must work. The research establishes whether it works
as intended.
That's a credible progression for what you're building with True-Line, and it doesn't require
presenting untested architectural proposals as scientific findings.
