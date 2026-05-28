USE CASE 1 — Conversational EKS Observability Assistant

Goal:

Ask natural language questions about:
- EKS health
- logs
- metrics
- pods
- namespaces
- deployments
- alerts
- app health
# Use Case 1 - Conversational EKS Observability Assistant

## Goal

Ask natural language questions about:

- EKS health
- logs
- metrics
- pods
- namespaces
- deployments
- alerts
- app health

### Example Questions

- How many nodes are running?
- Which pod consumed most memory in last 5 mins?
- Any CrashLoopBackOff pods?
- Is healthcare-app healthy?
- Show payment-api errors from last 2 mins

## 1. Final Architecture (AWS + Bedrock Native)

```text
                          ┌────────────────────┐
                          │   User / DevOps    │
                          │ Slack / Web UI     │
                          └─────────┬──────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ API Layer            │
                         │ FastAPI / Lambda     │
                         └─────────┬────────────┘
                                   │
                                   ▼
                      ┌─────────────────────────┐
                      │ Amazon Bedrock          │
                      │ Claude Sonnet           │
                      │ (Reasoning + Tool Use)  │
                      └─────────┬───────────────┘
                                │
                   Tool Calling / Function Calling
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼

┌────────────────┐   ┌──────────────────┐   ┌───────────────────┐
│ OpenSearch/ELK │   │ Prometheus       │   │ Kubernetes API    │
│ Logs + Alerts  │   │ Metrics          │   │ Cluster State     │
└────────────────┘   └──────────────────┘   └───────────────────┘
        │                       │                        │
        ▼                       ▼                        ▼
   App Logs              CPU / RAM / IO          Pods / Nodes /
   Error Logs            Restart Metrics         Events / Deployments

                                │
                                ▼
                    AI-generated response
```

## 2. Core Idea

The most important concept:

Bedrock does not directly read Kubernetes.

Instead:

- Bedrock = reasoning layer
- Tools/APIs = data providers

Bedrock:

- understands prompt
- decides what data is needed
- calls tools
- summarizes findings

## 3. Core Components Required

### A) Amazon EKS

Already available.

Contains:

- healthcare application
- deployments
- services
- ingress
- workloads

### B) EFK / OpenSearch

Already available.

Stores:

- container logs
- app logs
- ingress logs
- error logs
- alerts

Recommended index fields:

```json
{
  "timestamp": "...",
  "namespace": "healthcare",
  "pod": "patient-api-xyz",
  "container": "backend",
  "severity": "ERROR",
  "message": "DB timeout",
  "node": "ip-10-0-0-12"
}
```

Very important for AI reasoning.

### C) Prometheus

Already available.

Provides:

- CPU usage
- memory usage
- pod restarts
- network metrics
- node health

### D) kube-state-metrics

Already available.

Provides:

- pod states
- deployment states
- node conditions
- replica status

Critical for cluster health understanding.

### E) Kubernetes API Access

Your backend must access:

- pods
- nodes
- events
- deployments
- namespaces

Usually via:

- Python Kubernetes client
- EKS IAM auth

### F) Amazon Bedrock

This is the AI brain.

Recommended model:

| Model | Purpose |
| --- | --- |
| Claude Sonnet | Best overall |
| Claude Opus | advanced reasoning |
| Nova Pro | AWS-native alternative |

Bedrock will:

- understand prompts
- call tools
- analyze telemetry
- summarize incidents

### G) Backend API Layer

Recommended:

- FastAPI
- Lambda
- ECS service

Purpose:

- receive prompts
- expose tools
- interact with Bedrock
- call Prometheus/OpenSearch/K8s APIs

This is your AI orchestration layer.

## 4. Required Tool Functions

Your Bedrock agent/tools should expose:

### Logs Tool

Queries ELK/OpenSearch.

Example:

```python
search_logs(
    namespace="healthcare",
    severity="ERROR",
    time_range="5m"
)
```

### Metrics Tool

Queries Prometheus.

Example:

```python
get_top_memory_pods()
get_high_cpu_nodes()
get_restart_counts()
```

### Kubernetes Tool

Queries K8s API.

Example:

```python
get_pod_status()
get_cluster_nodes()
get_events()
```

### Alert Tool

Queries alerts.

Example:

```python
get_recent_alerts()
```

## 5. How Bedrock Works Here

Example prompt:

Which pod consumed most memory in last 5 mins?

### Internal Flow

#### Step 1 - Bedrock understands intent

Intent:

Need Prometheus memory metrics.

#### Step 2 - Tool call generated

Backend executes:

```promql
topk(5,
container_memory_working_set_bytes
)
```

#### Step 3 - Prometheus returns metrics

Example:

```json
[
  {
    "pod": "patient-api-6dd9",
    "memory": "2.1GB"
  }
]
```

#### Step 4 - Bedrock summarizes

Final response:

Top memory-consuming pod in last 5 minutes:

- patient-api-6dd9 -> 2.1GB

Namespace:

- healthcare

Possible concern:

Memory usage increased 37% compared to previous interval.

## 6. Implementation Idea (Very Important)

You do not start with RAG.

You start with tool-calling architecture.

This is the correct design.

Why?

- logs already searchable
- metrics already queryable
- K8s API already structured

You do not need embeddings initially.

## 7. Simple MVP Flow

### User Prompt

Is healthcare app having any issue?

### Bedrock Decides Required Tools

Calls:

- pod health tool
- recent error logs tool
- restart metrics tool
- K8s events tool

### Backend Gathers Data

From:

- Prometheus
- OpenSearch
- Kubernetes API

### Bedrock Reasons

Finds:

- restart spikes
- timeout logs
- high memory
- failing readiness probe

### Final Response

Healthcare app is partially degraded.

Issues detected:

- 2 patient-api pods restarted
- Memory usage exceeded 90%
- Readiness probe failures observed
- Database timeout errors in last 3 mins

Probable root cause:

Memory pressure causing request timeout cascade.

## 8. Recommended AWS Services

| Purpose | AWS Service |
| --- | --- |
| AI model | Bedrock Claude |
| Kubernetes | EKS |
| Metrics | AMP / Prometheus |
| Logs | OpenSearch |
| Alerts | CloudWatch/Slack |
| Backend | Lambda/Fargate |
| Secrets | Secrets Manager |
| Auth | IAM |
| API | API Gateway |

## 9. Minimum PromQL Queries You Need

### Top CPU Pods

```promql
topk(5,
sum(rate(container_cpu_usage_seconds_total[5m]))
by (pod)
)
```

### Top Memory Pods

```promql
topk(5,
container_memory_working_set_bytes
)
```

### Restarting Pods

```promql
increase(kube_pod_container_status_restarts_total[5m])
```

### Node Memory Pressure

```promql
kube_node_status_condition{
condition="MemoryPressure",
status="true"
}
```

## 10. Minimum OpenSearch Queries

### Recent Errors

```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"severity": "ERROR"}}
      ],
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-5m"
          }
        }
      }
    }
  }
}
```

## 11. Example Prompts Your System Should Support

### Cluster Health

- How many nodes are running?
- Any unhealthy nodes?
- Any pending pods?
- Any failed deployments?

### Metrics

- Which pod used most RAM?
- Top CPU consumers?
- Any pod above 90% memory?
- Show restart spikes.

### Logs

- Show auth-service errors.
- Any DB timeout logs?
- Summarize payment failures.

### Troubleshooting

- Why is patient-api restarting?
- Why is healthcare app slow?
- What changed before errors started?

## 12. Important Design Decision

Do not send all logs into Bedrock.

Instead:

```text
query -> filter -> summarize -> analyze
```

This is critical for:

- cost
- latency
- accuracy

## 13. Recommended Implementation Order

### Phase 1 (MVP)

Implement:

- Bedrock integration
- logs tool
- metrics tool
- K8s tool

Queries:

- node health
- pod health
- logs
- memory/cpu

### Phase 2

Add:

- summarization
- incident explanation
- RCA reasoning

### Phase 3

Add:

- autonomous investigation
- remediation suggestions
- Slack bot
- deployment correlation

## 14. Final Implementation Strategy

Your architecture should follow:

```text
Telemetry Sources
      ↓
Tool APIs
      ↓
Bedrock Claude
      ↓
Reasoning + Summarization
      ↓
Conversational Observability
```

Not:

```text
Raw Logs -> LLM
```

That architecture fails at scale.

## 15. Final Recommendation

For your setup specifically, best architecture:

```text
EKS
 ↓
EFK/OpenSearch + Prometheus
 ↓
FastAPI Tool Layer
 ↓
Amazon Bedrock Claude Sonnet
 ↓
Slack/Web ChatOps Assistant
```

This is:

- scalable
- enterprise-grade
- AWS-native
- production-ready
- extensible for future autonomous ops systems