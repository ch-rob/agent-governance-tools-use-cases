# Tested in Python 3.14.4
# From: https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/38-approval-workflows.md
# Preconditions: pip install agent-governance-toolkit[full]

# An agent governance setup where high-risk actions 
#   (large transfers, data exports, admin operations) pause execution
#   and wait for human approval before proceeding.

from agentmesh.governance import (
    govern, CallbackApproval, ApprovalDecision, GovernanceDenied,
)

def process_transfer(action, amount, to_account):
    print(f"  💰 Transferring ${amount} to {to_account}")
    return {"transferred": True, "amount": amount}

# Approval logic — in production, this would call Slack/Teams/Jira
def my_approval_logic(request):
    print(f"\n  🔔 APPROVAL NEEDED")
    print(f"     Rule: {request.rule_name}")
    print(f"     Action: {request.action}")
    print(f"     Approvers: {', '.join(request.approvers)}")

    # Auto-approve for demo (in production: call external service)
    if request.action == "transfer":
        return ApprovalDecision(
            approved=True,
            approver="treasury-ops@company.com",
            reason="Within daily limit",
        )
    return ApprovalDecision(approved=False, approver="system", reason="Unknown action type")

handler = CallbackApproval(my_approval_logic, timeout_seconds=300)

safe_transfer = govern(
    process_transfer,
    policy="Policies/E4-financial-approval-policy.yaml",
    approval_handler=handler,
)

# This triggers the approval flow
result = safe_transfer(action="transfer", amount=5000, to_account="ACC-789")
print(f"Result: {result}")

# Check the log to see what happened
print(f"Log Entries...")
for entry in safe_transfer.audit_log.query(event_type="approval_decision"):
    print(f"  {entry.action} → {entry.outcome}")
    print(f"    Approver: {entry.data['approver']}")
    print(f"    Reason: {entry.data['reason']}")