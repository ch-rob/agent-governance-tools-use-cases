# Tested in Python 3.14.4
# From: https://github.com/microsoft/agent-governance-toolkit/blob/main/docs/tutorials/13-observability-and-tracing.md
# Preconditions: 
#       pip install agent-governance-toolkit[full]
#       pip install agent-hypervisor

# The Agent Hypervisor observability module provides four composable primitives
# ┌────────────────────────────────────────────────────────────┐
# │                    HypervisorEventBus                      │
# │   Append-only structured event store with pub/sub          │
# │   40+ typed events · session/agent/time indexes            │
# ├──────────────────────┬─────────────────────────────────────┤
# │  RingMetricsCollector│       SagaSpanExporter              │
# │  Subscribes to ring  │       Subscribes to saga            │
# │  events → Prometheus │       events → OTel spans           │
# │  counters & gauges   │       with SpanSink protocol        │
# ├──────────────────────┴─────────────────────────────────────┤
# │                     CausalTraceId                          │
# │   Hierarchical trace/span IDs for multi-agent causality    │
# │   Format: {trace_id}/{span_id}[/{parent_span_id}]          │
# └────────────────────────────────────────────────────────────┘

# OpenTelemetry support for distributed tracing, 
#   allowing you to track agent actions across systems 
#   and visualize them in tools like Azure Monitor or Prometheus + Grafana


from hypervisor.observability import (
    HypervisorEventBus,
    HypervisorEvent,
    EventType,
    CausalTraceId,
)

print(f"################## Emit and Query Events ##################")

# 1. Create the event bus — the central nervous system
#       an append-only event log with built-in indexing and pub/sub. 
#       Every component in the hypervisor emits events here — 
#       ring transitions, saga steps, security incidents, audit records, and more.
bus = HypervisorEventBus()

# 2. Create a causal trace for this workflow
rootTrace = CausalTraceId()
print(f"Trace started: {rootTrace.full_id}")
# e.g. "a1b2c3d4e5f6/01234567"

# 3. Emit a structured event
bus.emit(HypervisorEvent(
    event_type=EventType.SESSION_CREATED,
    session_id="session-001",
    agent_did="did:mesh:data-analyst",
    causal_trace_id=rootTrace.full_id,
    payload={"model": "gpt-4o", "ring": 3},
))

# 4. Query it back
events = bus.query_by_session("session-001")
print(f"Events for session-001: {len(events)}")   # 1
print(events[0].to_dict())

print(f"################## Subscribe to Events ##################")

# Type-specific subscriber — only ring breaches
def on_breach(event: HypervisorEvent) -> None:
    print(f"🚨 BREACH: agent={event.agent_did} payload={event.payload}")

bus.subscribe(event_type=EventType.RING_BREACH_DETECTED, handler=on_breach)

# Wildcard subscriber — receives ALL events
bus.subscribe(event_type=None, handler=lambda e: print(f"[audit] {e.event_type.value}"))

# This triggers both subscribers
bus.emit(HypervisorEvent(
    event_type=EventType.RING_BREACH_DETECTED,
    agent_did="did:mesh:rogue-bot",
    session_id="session-001",
    payload={"attempted_tool": "shell_exec", "ring": 3},
))

print(f"################## Creating Traces ##################")

# CausalTraceId: Hierarchical Trace IDs
#   Format: {trace_id}/{span_id}[/{parent_span_id}]
#       trace_id — 12-char hex, shared across the entire trace tree
#       span_id — 8-char hex, unique to this span
#       parent_span_id — 8-char hex, present only for non-root spans

from hypervisor.observability import CausalTraceId

# Root trace — generated automatically
print(f" root.full_id           {rootTrace.full_id}")        # "a1b2c3d4e5f6/01234567"
print(f" root.depth             {rootTrace.depth}")          # 0
print(f" root.parent_span_id    {rootTrace.parent_span_id}") # None

# Child span — same trace, new span, parent linked
child = rootTrace.child()
print(f" child.full_id           {child.full_id}")        # "a1b2c3d4e5f6/89abcdef/01234567s"
print(f" child.depth             {child.depth}")          # 1
print(f" child.parent_span_id    {child.parent_span_id}") # "01234567" (root's span_id)

# Sibling span — parallel work at the same depth
sibling = child.sibling()
print(f" sibling.full_id           {sibling.full_id}")        # "a1b2c3d4e5f6/b57b984e/01234567"
print(f" sibling.depth           {sibling.depth}")              # 1 (same as child)
print(f" sibling.parent_span_id {sibling.parent_span_id}")      # "01234567" (same parent)
print(f" sibling.span_id        {sibling.span_id}")             # new unique ID

# Deep nesting — each child() increments depth
grandchild = child.child()
print(f" grandchild.full_id           {grandchild.full_id}")        
print(f" grandchild.depth           {grandchild.depth}")  # 2
print(f" grandchild.parent_span_id {grandchild.parent_span_id}") 
print(f" grandchild.span_id        {grandchild.span_id}")        
