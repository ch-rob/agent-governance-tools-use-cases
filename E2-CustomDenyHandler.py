from agentmesh.governance import govern

def send_email(to, subject, body):
    return {"sent": True, "to": to}

safe_send = govern(
    send_email,
    policy="""
apiVersion: governance.toolkit/v1
name: email-send-policy
agents: ["*"]
default_action: allow
rules:
  - name: block-you
    condition: "to.value == 'you'"
    action: deny
    description: "Not allowed to send emails to you"
    priority: 100
""",
    on_deny=lambda decision: {
        "sent": False,
        "blocked_by": decision.matched_rule,
        "reason": decision.reason,
    },
)

# If denied, returns the dict instead of raising
result = safe_send(to="you", subject="Q3 Revenue", body="...")
# Result: {'sent': False, 'blocked_by': 'block-you', 'reason': 'Not allowed to send emails to you'}

if not result["sent"]:
    print(f"Email blocked: {result['reason']} (rule: {result['blocked_by']})")