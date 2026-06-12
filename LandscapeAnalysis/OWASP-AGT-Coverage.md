# OWASP Agentic Top 10 — AGT Coverage Summary

How the Agent Governance Toolkit (AGT) addresses each risk in the [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).

> **Source:** [microsoft/agent-governance-toolkit — OWASP-COMPLIANCE.md](https://github.com/microsoft/agent-governance-toolkit/blob/main/agent-governance-python/agent-compliance/docs/OWASP-COMPLIANCE.md)

**Coverage: 10 / 10** — full coverage achieved with AI-BOM v2.0 closing the supply chain gap.

---

## Coverage at a Glance

| ID | Risk | AGT Component |
|----|------|---------------|
| ASI-01 | Agent Goal Hijack | Agent OS — Policy Engine |
| ASI-02 | Tool Misuse & Exploitation | Agent OS — Capability Sandboxing |
| ASI-03 | Identity & Privilege Abuse | AgentMesh — DID Identity & Trust Scoring |
| ASI-04 | Agentic Supply Chain Vulnerabilities | AgentMesh — AI-BOM |
| ASI-05 | Unexpected Code Execution | Agent Runtime — Execution Rings |
| ASI-06 | Memory & Context Poisoning | Agent OS — VFS Policies + CMVK Verification |
| ASI-07 | Insecure Inter-Agent Communication | AgentMesh — IATP + Encrypted Channels |
| ASI-08 | Cascading Agent Failures | Agent SRE — Circuit Breakers + SLOs |
| ASI-09 | Human-Agent Trust Exploitation | Agent OS — Approval Workflows |
| ASI-10 | Rogue Agents | Agent Runtime — Kill Switch + Ring Isolation |

---

## Detail by Risk

### ASI-01: Agent Goal Hijack
**Risk:** Attackers manipulate the agent's objectives via indirect prompt injection or poisoned inputs.

**AGT mitigation:** The Agent OS policy engine intercepts every agent action at the kernel level before it reaches any tool. Unauthorized goal changes are blocked deterministically — not probabilistically.

- Policy modes: `strict` (deny-by-default), `permissive`, `audit`
- Action interception via kernel-level syscall abstraction
- MCP Governance Proxy enforces policy on MCP tool calls

---

### ASI-02: Tool Misuse & Exploitation
**Risk:** An agent's authorized tools are abused in unintended ways (e.g., data exfiltration via read operations).

**AGT mitigation:** Capability-based security grants agents specific, scoped permissions — not blanket tool access. Inputs are sanitized for injection patterns before reaching tools.

- Explicit capability grants: `read`, `write`, `execute`, `network`
- Built-in strict mode blocks `run_shell`, `execute_command`, `eval`
- Command injection detection and shell metacharacter blocking
- `verify_code_safety` MCP tool checks generated code before execution

---

### ASI-03: Identity & Privilege Abuse
**Risk:** Agents escalate privileges by abusing identities or inheriting excessive credentials.

**AGT mitigation:** Zero-trust identity via Decentralized Identifiers (DIDs). Every agent has a cryptographic identity with scoped capabilities. Trust is earned through behavior, not assumed.

- `did:agentmesh:{agentId}:{fingerprint}` with Ed25519 key pairs
- Trust tiers: Untrusted → Provisional → Trusted → Verified
- Delegation chains enforce narrowing (child capabilities ≤ parent capabilities)
- Challenge-response handshake for mutual authentication
- Trust decay — scores degrade over time without positive behavioral signals

---

### ASI-04: Agentic Supply Chain Vulnerabilities
**Risk:** Vulnerabilities in third-party tools, plugins, agent registries, or runtime dependencies.

**AGT mitigation:** AI-BOM (AI Bill of Materials) v2.0 tracks the complete AI supply chain — model provenance, dataset lineage, weights versioning, and software dependencies — with cryptographic signing.

- Model provenance: base model ancestry, fine-tuning history, training cutoff dates
- Dataset tracking: RAG sources, evaluation benchmarks, PII status, bias assessment, consent
- Weights versioning: SHA-256 hashes, quantization records, LoRA adapter metadata, SLSA build provenance
- SPDX-aligned package tracking with CI security scanning

---

### ASI-05: Unexpected Code Execution
**Risk:** Agents trigger remote code execution through tools, interpreters, or APIs.

**AGT mitigation:** CPU ring-inspired execution isolation confines agents to privilege tiers with resource limits. Agents can be terminated instantly.

- Execution Rings (Ring 0–3): kernel → trusted → standard → untrusted
- Per-execution CPU, memory, and time limits
- Kill switch for instant agent termination
- Saga compensation for automatic rollback on failure

---

### ASI-06: Memory & Context Poisoning
**Risk:** Persistent memory or long-running context is poisoned with malicious instructions.

**AGT mitigation:** Policy-controlled virtual filesystem (VFS) for agent memory with multi-model claim verification to detect poisoned context.

- VFS memory policies: `vfs://{agent_id}/mem/*` with per-agent access control
- Policy-protected context paths are read-only
- CMVK (Cross-Model Verification Kernel) validates claims across multiple models
- Prompt injection detection blocks `ignore previous instructions`-style patterns
- PII detection and redaction in agent context

---

### ASI-07: Insecure Inter-Agent Communication
**Risk:** Agents collaborate without adequate authentication, confidentiality, or validation.

**AGT mitigation:** IATP (Inter-Agent Trust Protocol) provides a purpose-built secure communication layer with cryptographic attestation on every message.

- IATP sign/verify: cryptographic trust attestations for every inter-agent message
- All inter-agent communication is encrypted
- Trust score evaluated before communication is established
- Ongoing reputation tracking with decay and penalty signals
- Mutual authentication via challenge-response

---

### ASI-08: Cascading Agent Failures
**Risk:** An initial error or compromise triggers compound failures across chained agents.

**AGT mitigation:** Agent SRE provides production-grade reliability engineering designed specifically for agent fleets.

- Circuit breakers automatically isolate failing agents before failures propagate
- Cascading failure detection monitors dependency chains
- SLOs (Service Level Objectives) with quantified error budgets per agent
- Canary deploys for gradual rollout of agent changes
- OpenTelemetry integration for distributed tracing across multi-agent workflows

---

### ASI-09: Human-Agent Trust Exploitation
**Risk:** Attackers leverage misplaced user trust in agent autonomy to authorize dangerous actions.

**AGT mitigation:** Approval workflows require explicit human confirmation for high-risk actions before they execute — enforced at the policy layer, not the prompt layer.

- Configurable human-in-the-loop for sensitive operations
- Automatic risk classification: `critical`, `high`, `medium`, `low`
- Quorum logic: critical actions can require multiple approvals
- Approval requests expire to prevent stale authorizations
- `require_approval` is a first-class policy rule action

---

### ASI-10: Rogue Agents
**Risk:** Agents operating outside their defined scope due to configuration drift, reprogramming, or emergent misbehavior.

**AGT mitigation:** Runtime behavioral monitoring with instant kill capability, combined with AgentMesh trust decay that degrades the score of misbehaving agents.

- Ring isolation confines rogue agents — they cannot escalate privilege
- Kill switch for immediate termination on detected rogue behavior
- Trust score decay on failures and anomaly signals
- Merkle-chained audit logs provide cryptographic proof of agent action history
- Shapley-value fault attribution identifies which agent in a chain caused a failure

---

## Cross-Cutting Principle: Least Agency

The OWASP Agentic Top 10 emphasizes **Least Agency** as a foundational design principle: agents should be granted the minimum capabilities, permissions, and autonomy necessary to complete their tasks. AGT enforces this at every layer:

| Layer | Enforcement |
|-------|-------------|
| Agent OS | Deny-by-default policy engine; each capability must be explicitly granted |
| AgentMesh | DID identity with scoped capabilities; delegation requires narrowing (child ≤ parent) |
| Agent Runtime | Execution rings enforce privilege tiers; untrusted agents run in Ring 3 |
| Agent SRE | Resource limits and error budgets cap agent impact radius |
| Agent Compliance | Governance policies audit capability grants against the Least Agency principle |

---

## Install Coverage Map

```
pip install agent-governance-toolkit[full]
```

| Package | Risks Covered |
|---------|--------------|
| `agent-os-kernel` | ASI-01, ASI-02, ASI-06, ASI-09 |
| `agentmesh-platform` | ASI-03, ASI-04, ASI-07, ASI-10 |
| `agentmesh-runtime` | ASI-05, ASI-10 |
| `agent-sre` | ASI-08 |

---

## Alignment with Other Frameworks

| Framework | Coverage |
|-----------|----------|
| OWASP Agentic Top 10 (2026) | 10/10 |
| NIST AI RMF | Govern, Map, Measure, Manage functions |
| EU AI Act | Risk classification, audit trails, human oversight |
| Singapore MGF for Agentic AI | Zero-trust, accountability, oversight layers |
