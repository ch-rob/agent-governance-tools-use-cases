# Agent Governance Toolkit — Examples

Worked Python examples implementing select use cases from the [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) tutorials.

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

## License

[MIT](LICENSE)
