# AI Incident Intelligence Platform (Corrected)

## Final Architecture with Clear RAG Flow

```text
                         ┌──────────────────────┐
                         │ Healthcare App (EKS) │
                         └──────────┬───────────┘
                                    │
                    Logs / Metrics / K8s Events
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼

┌────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ OpenSearch/ELK │      │ Prometheus       │      │ Kubernetes API   │
│ Logs + Alerts  │      │ Metrics          │      │ Events/Pods      │
└────────────────┘      └──────────────────┘      └──────────────────┘

                                    │
                                    ▼
                          AlertManager / Rules
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                                           ▼

       Slack Notification                           Jira Ticket

              │                                           │
              └──────────────────┬────────────────────────┘
                                 ▼

                  ┌──────────────────────────────┐
                  │ AI Incident Processor         │
                  │ FastAPI / Lambda / ECS       │
                  └──────────────┬───────────────┘
                                 │
                ┌────────────────┴─────────────────┐
                ▼                                  ▼

      REAL-TIME TOOL CALLING                 RAG PIPELINE
                │                                  │

   ┌────────────┼─────────────┐        ┌───────────┼────────────┐
   ▼            ▼             ▼        ▼           ▼            ▼

Logs Tool   Metrics Tool   K8s Tool   Jira Docs  Runbooks   RCA Docs
(OpenSearch)(Prometheus)   (K8s API)      │          │           │
                                           └────┬─────┴─────┬────┘
                                                ▼

                                   Bedrock Knowledge Base
                                                │
                                      Embeddings + Retrieval
                                                │
                                   OpenSearch Vector Store
                                                │
                                                ▼

                                 Retrieved Historical Context

                                                │
                         ┌──────────────────────┴──────────────────────┐
                         ▼                                             ▼

                Current Telemetry                         Historical Knowledge

                         └──────────────────────┬──────────────────────┘
                                                ▼

                                 Amazon Bedrock Claude Sonnet
                                     (Reasoning + RCA)

                                                │
                                                ▼

                              AI Incident Summary / RCA / Solution

                                                │
                       ┌────────────────────────┴─────────────────────┐
                       ▼                                              ▼

                 Slack AI Reply                               Jira AI Comment
```

## Now the RAG Flow Is Clear

Earlier architecture showed Bedrock KB. But this is the full internal RAG flow:

```text
Jira / Runbooks / RCA Docs
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Storage
        ↓
Semantic Retrieval
        ↓
Claude receives context
```

That is actual RAG.

## Where RAG Is Used During an Incident

Suppose: payment-api latency spike.

### Tool-Calling Side

Claude gets:

- current logs
- memory metrics
- pod restarts
- K8s events

This tells what is happening now.

### RAG Side

Claude retrieves:

- previous Jira tickets
- RCA docs
- internal fixes
- runbooks

This tells what happened historically.

### Both Together

Claude can now answer:

This resembles incident INC-4412 caused by Redis saturation.

That sentence comes from RAG retrieval, not tools.

## Very Important Understanding

### Tools

Handle live operational telemetry.

Examples:

- CPU
- RAM
- logs
- pod state
- alerts

### RAG

Handles organizational memory.

Examples:

- historical incidents
- Jira tickets
- SOPs
- runbooks
- previous RCA

## Why Both Are Needed

Without RAG, AI knows only the current issue.

Without tools, AI knows only historical knowledge.

Together, AI becomes an incident intelligence system.

## What Bedrock Knowledge Base Actually Does

Bedrock KB automatically handles:

- document ingestion
- chunking
- embedding generation
- vector indexing
- retrieval
- context injection

## Your Real RAG Sources

### Best Sources for Your System

| Source | Why Important |
| --- | --- |
| Jira tickets | previous incidents |
| RCA docs | historical causes |
| Runbooks | remediation steps |
| Slack incident summaries | operational context |
| Confluence | architecture knowledge |
| SOP docs | standard recovery |
| Deployment docs | infra changes |

## Where the Vector Database Exists

The real vector DB layer is OpenSearch Vector Store inside the architecture.

This stores:

- embeddings of Jira tickets
- embeddings of runbooks
- embeddings of RCA docs

## RAG Query Example

Current incident:

Redis timeout plus memory spike.

Claude retrieves semantically similar docs:

- INC-4412
- INC-8821
- Redis leak RCA

using vector similarity.

That is actual RAG retrieval.

## Why This Is Powerful

Now AI can do incident similarity search.

Example:

Have we seen similar issue before?

This is impossible with Prometheus, OpenSearch logs, and Kubernetes API alone.

RAG solves this.

## Final Mental Model

Tool-calling side: What is happening now?

RAG side: What happened historically?

Claude combines both:

```text
Current issue
+
Historical knowledge
+
Operational reasoning
=
AI RCA
```

## Why Your System Becomes Very Powerful

Because it can:

- investigate incidents
- correlate telemetry
- compare with historical incidents
- suggest known fixes
- summarize intelligently
- reduce MTTR

This is the real enterprise value.

## Final Recommended Stack for You

| Layer | Recommended Tech |
| --- | --- |
| Cluster | EKS |
| Logs | OpenSearch |
| Metrics | Prometheus |
| Alerts | AlertManager |
| Ticketing | Jira |
| Notifications | Slack |
| LLM | Bedrock Claude Sonnet |
| RAG | Bedrock Knowledge Base |
| Vector Store | OpenSearch Vector |
| Backend | FastAPI / ECS |
| Tool Layer | Python generic tools |

## Final Key Insight

Your final architecture is not an LLM chatbot.

It is an AI-powered operational intelligence platform where:

- Tools -> provide live telemetry
- RAG -> provides organizational memory
- Claude -> provides reasoning