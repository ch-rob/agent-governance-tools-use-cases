# Agent Governance Toolkit — Examples

Worked Python examples implementing select use cases from the [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) tutorials.

## About the Agent Governance Toolkit

The [Agent Governance Toolkit (AGT)](https://github.com/microsoft/agent-governance-toolkit) is a Microsoft open-source project that provides policy enforcement, zero-trust identity, execution sandboxing, and reliability engineering for autonomous AI agents — covering all 10 categories of the OWASP Agentic AI Top 10.

**The core problem it solves:** AI agents call tools, query databases, send emails, and delegate to other agents autonomously. Standard IAM and OAuth scopes control *which services* an agent can reach, but not *what it does once connected*. Prompt-level safety instructions are probabilistic — adversarial attacks achieve near-100% success rates against frontier models. AGT enforces governance at the application middleware layer in deterministic code, making disallowed actions structurally impossible rather than merely discouraged.

**Key layers:**

| Layer | What it provides |
|-------|-----------------|
| **Policy Engine** | YAML/OPA/Cedar rules evaluated on every tool call; fail-closed by default |
| **Identity & Trust** | Cryptographic agent DIDs (Ed25519), SPIFFE/SVID workload identity, continuous 0–1000 trust scoring |
| **Credentials** | Short-lived 15-minute tokens scoped to specific capabilities, with auto-rotation and instant revocation |
| **Human-in-the-Loop** | Approval workflows for high-risk actions before they execute |
| **Audit Log** | Tamper-evident Merkle-chained record of every decision |
| **Token Budgets** | Per-agent and session-level context/cost controls |
| **Observability** | Distributed tracing and hypervisor-level execution audit |

**One-line integration** — wrap any existing tool function:

```python
from agentmesh.governance import govern
safe_tool = govern(my_tool, policy="policy.yaml")
```

AGT supports Python, TypeScript, .NET, Go, and Rust, with adapters for LangChain, AutoGen, CrewAI, Semantic Kernel, OpenAI Agents SDK, and more.

## Prerequisites

```bash
pip install agent-governance-toolkit[full]
pip install agent-hypervisor   # E5 only
pip install agent-os-kernel    # E6 only
```

Tested with **Python 3.14**.

## Examples

| File | Topic | Source Tutorial |
|------|-------|-----------------|
| [E1-GovernedDBQuery.py](E1-GovernedDBQuery.py) | Wrapping a tool with `govern()` to enforce policies on database queries | [36 — Govern Quickstart](https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/36-govern-quickstart.md) |
| [E2-CustomDenyHandler.py](E2-CustomDenyHandler.py) | Custom deny handler — intercept and respond to policy violations | [36 — Govern Quickstart](https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/36-govern-quickstart.md) |
| [E3-TrustAndIdentity.py](E3-TrustAndIdentity.py) | Cryptographic agent identity (DIDs, Ed25519 keys) and dynamic trust scoring | [02 — Trust and Identity](https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/02-trust-and-identity.md) |
| [E4-HumanInTheLoop.py](E4-HumanInTheLoop.py) | Human-in-the-loop approval workflows for high-risk agent actions | [38 — Approval Workflows](https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/38-approval-workflows.md) |
| [E5-Observability.py](E5-Observability.py) | Observability and distributed tracing for agent operations | [13 — Observability and Tracing](https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/13-observability-and-tracing.md) |
| [E6-TokenBudgets.py](E6-TokenBudgets.py) | Token budget tracking and context scheduling across agents | [24 — Cost and Token Budgets](https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/24-cost-and-token-budgets.md) |

Supporting policy files are in the [Policies/](Policies/) directory.

## Other Interesting Features

See [OtherInterestingFeatures.md](OtherInterestingFeatures.md) for additional tutorials worth exploring — framework integrations (OpenAI, Anthropic, LangChain), prompt injection detection, and MCP security gateways.

## Landscape Comparison

If you're evaluating AGT against other tooling, the [LandscapeAnalysis/](LandscapeAnalysis/) folder contains comparison documents worth reading before committing to a direction:

- [OtherFrameworks.md](LandscapeAnalysis/OtherFrameworks.md) — comparison with other agent governance and safety frameworks
- [Agent365Comparison.md](LandscapeAnalysis/Agent365Comparison.md) — how AGT relates to Microsoft 365 / Copilot agent tooling

These documents cover where AGT fits, what it overlaps with, and where alternative or complementary tools may be a better choice for your use case.

## License

[MIT](LICENSE)
