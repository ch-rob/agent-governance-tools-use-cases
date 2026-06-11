# Tested in Python 3.14.4
# From: https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/02-trust-and-identity.md
# Preconditions: pip install agent-governance-toolkit[full]

# Every agent gets a did:mesh:* identifier bound to an Ed25519 key pair, 
#   a human sponsor for accountability, a trust score that reflects their reputation and behavior 
#   that decay over time without positive behavioral evidence, and short-lived credentials (15-minute TTL)
#   that auto-rotate and can be revoked instantly.

# The registry would be backed by a secure, decentralized store in production (as seen in the flow below), 
#   but for this example it's just an in-memory dict. 
#   The governance toolkit provides a built-in registry implementation, 
#   but you can also implement your own (e.g. on top of a database or blockchain) 
#   by subclassing agentmesh.registry.BaseRegistry and passing an instance to AgentIdentity.create().

# Agent (client)                       Registry/Auth Service            Protected API
# ---------------------------------------------------------------------------------------------
# 1. create() → registers DID -------> stores DID + approved abilities
# 2. issue credential ---------------> signs credential (JWT/token)
#                                      bound to that DID + abilities only
# 3. calls API with Bearer token -----------------------------------> 4. validate token
#                                                                     check DID in registry
#                                                                     check trust score ≥ threshold
#                                                                     check capability matches
#                                                                     check resource scope
#                                                                     -> allow or deny

from agentmesh import AgentIdentity, RiskScorer

# Create an agent with a human sponsor
agent = AgentIdentity.create(
    name="DataProcessor",
    sponsor="alice@company.com",
    capabilities=["read:data", "write:reports"],
    organization="Analytics",
)

print(agent.did)          # did:mesh:a1b2c3d4e5f6...
print(agent.public_key)   # Base64-encoded Ed25519 public key
print(agent.status)       # "active"

# Check the agent's risk score (0-1000, higher = safer)
scorer = RiskScorer()
score = scorer.get_score(str(agent.did))

print(score.total_score)  # 500 (default starting score)
print(score.risk_level)   # "medium"