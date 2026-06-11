# Tested in Python 3.14.4
# From: https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/24-cost-and-token-budgets.md
# Preconditions: 
#       pip install agent-governance-toolkit[full]
#       pip install agent-os-kernel
# Concept: The kernel owns the budget; agents cannot exceed it
#   The TokenBudgetTracker provides per-agent token tracking with configurable 
#       warning thresholds and callbacks.
#   The TokenBudgetTracker can read its default max_tokens from a GovernancePolicy
#   The ContextScheduler is a kernel-level primitive that allocates context windows to agents, 
#       enforces the 90/10 lookup/reasoning split, and emits signals when budgets are crossed.
#       The total token pool is across all agents in a session, so they must coordinate and prioritize their usage.



from agent_os.integrations.token_budget import TokenBudgetTracker
from agent_os.context_budget import (
    ContextScheduler, ContextPriority, AgentSignal, BudgetExceeded,
)

# ── Configuration ──
SESSION_BUDGET = 100_000
AGENT_ID = "research-agent"

# ── Set up budget tracking ──
tracker = TokenBudgetTracker(
    max_tokens=SESSION_BUDGET,
    warning_threshold=0.8,
    on_warning=lambda aid, s: print(
        f"⚠️  {aid} at {s.percentage:.0%} ({s.used:,}/{s.limit:,} tokens)"
    ),
)

scheduler = ContextScheduler(
    total_budget=SESSION_BUDGET,
    lookup_ratio=0.90,
    warn_threshold=0.85,
)

# Register signal handlers
scheduler.on_signal(AgentSignal.SIGWARN,
    lambda aid, sig: print(f"⚠️  Context warning for {aid}"))
scheduler.on_signal(AgentSignal.SIGSTOP,
    lambda aid, sig: print(f"🛑 Context budget exceeded for {aid}"))

# ── Simulate research tasks ──
tasks = [
    ("Analyse Q1 earnings",     ContextPriority.HIGH,   15_000, 3_000),
    ("Summarise competitor reports", ContextPriority.NORMAL, 20_000, 5_000),
    ("Extract key metrics",     ContextPriority.NORMAL, 10_000, 2_000),
    ("Generate final report",   ContextPriority.HIGH,   25_000, 8_000),
    ("Deep-dive appendix",      ContextPriority.LOW,    20_000, 5_000),
]

for task_name, priority, lookup_tok, reasoning_tok in tasks:
    # Check budget
    status = tracker.check_budget(AGENT_ID)
    if status.is_exceeded:
        print(f"\n🛑 Budget exceeded — skipping '{task_name}'")
        break

    print(f"\n📋 Task: {task_name}")
    pct = status.percentage
    bar_width = 20
    filled = int(bar_width * pct)
    bar = "█" * filled + "░" * (bar_width - filled)
    print(f"   Budget: [{bar}] {pct:.0%} ({status.used:,}/{status.limit:,})")

    # Allocate context
    window = scheduler.allocate(AGENT_ID, task_name, priority)
    print(f"   Allocated: {window.total:,} tokens "
          f"(lookup: {window.lookup_budget:,}, reasoning: {window.reasoning_budget:,})")

    # Record usage
    try:
        scheduler.record_usage(AGENT_ID, lookup_tok, reasoning_tok)
    except BudgetExceeded:
        print(f"   🛑 Context window exceeded")

    scheduler.release(AGENT_ID)

    # Track against session budget
    tracker.record_usage(AGENT_ID, lookup_tok, reasoning_tok)
    status = tracker.get_usage(AGENT_ID)
    print(f"   Used: {status.used:,} / {status.limit:,} "
          f"({status.percentage:.0%})")

# ── Final summary ──
print(f"\n{'='*50}")
print(f"Session summary for {AGENT_ID}:")
final = tracker.get_usage(AGENT_ID)
print(f"  Total used:    {final.used:,} tokens")
print(f"  Remaining:     {final.remaining:,} tokens")
print(f"  Utilisation:   {final.percentage:.0%}")
print(f"  Warning:       {final.is_warning}")
print(f"  Exceeded:      {final.is_exceeded}")