# AI Agent Governance Toolkit Landscape

## 🧭 The 4 Layers of Agent Governance

Most tools operate at different layers of the agent lifecycle:

| Layer | What it controls | Example tools |
|------|----------------|---------------|
| 1. Content | What the model says | Guardrails AI, NeMo Guardrails |
| 2. Evaluation | Behavior validation over time | LangSmith, Promptfoo, ASSERT |
| 3. Sandbox | Execution environment | E2B, Modal |
| 4. Action / Runtime | What the agent is allowed to do | AGT, APort |

👉 Production systems typically combine multiple layers for full coverage.

---

## 🧱 1. Runtime / Action Governance (Closest to AGT)

### APort
- Pre-tool-call authorization
- Policy-driven enforcement before execution
- Works across multiple frameworks

### Agent Control Specification (ACS)
- Portable policy-as-code specification
- Policies enforced at multiple interception points

### Emerging tools
- AgentGuardian
- Safiron
- PCAS

---

## 🧱 2. Guardrails (Content + Output Validation)

### LangChain Guardrails
- Middleware for PII detection and rule enforcement
- Supports deterministic and model-based validation

### Guardrails AI
- Structured output validation
- Validator-based system with community extensions

### NVIDIA NeMo Guardrails
- Conversational safety rails
- Flow control and jailbreak prevention

---

## 🧱 3. Audit / Trust / Cryptographic Governance

### asqav
- Quantum-safe signed audit trails
- Chains all agent actions for traceability

### AgentMint
- Lightweight signed receipts for actions
- Local-first governance approach

---

## 🧱 4. Evaluation / Testing Frameworks

### ASSERT
- Converts requirements into automated test suites
- Generates evaluation datasets and metrics

### Other tools
- LangSmith
- Braintrust
- Patronus AI
- Galileo
- Arize Phoenix
- Promptfoo

---

## 🧱 5. Sandbox / Execution Isolation

Examples:
- E2B
- Modal
- Google ADK sandbox
- ceLLMate

These tools limit blast radius and contain execution environments.

---

## 🏁 Practical Takeaways

### 1. No single tool solves governance

Categories include:
- Action-layer: AGT, APort
- Content guardrails: NeMo Guardrails, Guardrails AI
- Evaluation: LangSmith, Promptfoo
- Audit/compliance: asqav, AgentMint

### 2. Typical Production Architecture

```
Agent Framework
    ↓
Guardrails layer
    ↓
Runtime governance (AGT / APort)
    ↓
Sandbox layer
    ↓
Evaluation framework
    ↓
Control plane (Agent 365)
```

### 3. Key Insight

> The industry is converging on layered governance. Runtime action control remains the hardest unsolved problem, and AGT is one of the few tools targeting it directly.
