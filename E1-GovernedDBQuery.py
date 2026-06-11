# Tested in Python 3.14.4
# From: https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/36-govern-quickstart.md
# Preconditions: pip install agent-governance-toolkit[full]

from agentmesh.governance import govern

def query_database(action="read", table="users", **filters):
    """Simulate a database query tool."""
    print(f"  Querying {table} ({action}) with filters: {filters}")
    return {"table": table, "action": action, "rows": 42}

# Create the governed version
safe_query = govern(query_database, policy="""
apiVersion: governance.toolkit/v1
name: db-access-policy
agents: ["*"]
default_action: allow
rules:
  - name: block-drop
    condition: "action.type == 'drop'"
    action: deny
    description: "DROP operations are never allowed"
    priority: 100

  - name: block-write-to-audit
    condition: "action.type == 'write' and table.value == 'audit_log'"
    action: deny
    description: "Audit log is append-only — no direct writes"
    priority: 100

  - name: require-approval-for-delete
    condition: "action.type == 'delete'"
    action: require_approval
    approvers: ["dba-team"]
    priority: 50
""")

# ✅ This works
result = safe_query(action="read", table="users", limit=10)
print(f"Result: {result}")

# ❌ This is denied
try:
    safe_query(action="drop", table="users")
except Exception as e:
    print(f"Blocked: {e}")