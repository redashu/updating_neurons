# What is Agentic AI?

Agentic AI refers to AI systems that can autonomously plan, execute, and adapt tasks to achieve goals—like a "digital employee" that:

- Thinks step-by-step
- Makes decisions (within boundaries)
- Learns from feedback
- Collaborates with other AI/humans

## Key Difference vs. Traditional AI

| Traditional AI                        | Agentic AI                                 |
|----------------------------------------|--------------------------------------------|
| Follows fixed rules (e.g., chatbots)   | Adapts to new situations                   |
| Needs explicit instructions            | Plans its own approach                     |
| Single-task focused                    | Orchestrates multi-step workflows          |

**Example:**  
A customer support AI that doesn’t just answer FAQs but researches order history, negotiates solutions, and escalates complex cases—all without human intervention.

---

## Why Product Managers Should Care

Agentic AI unlocks:

### Complex Workflow Automation

**Use Case:** Automate refund processing by having AI:  
✅ Verify purchase history → ✅ Check return policy → ✅ Approve/deny → ✅ Notify customer

### Dynamic Problem-Solving

**Use Case:** An AI sales agent that:  
🔍 Analyzes lead behavior → 💡 Personalizes outreach → 📅 Schedules demos → 🔄 Adjusts strategy based on replies

### Reduced Human Toil

**Use Case:** IT helpdesk AI that:  
🔧 Diagnoses issues → 🛠️ Tries fixes (e.g., restart services) → 📞 Calls human only if stuck

---

## Key Components of Agentic AI

- **Autonomy:** Sets sub-goals (e.g., "Increase sign-ups" → "Run A/B tests on landing page")
- **Memory:** Retains context across interactions (e.g., remembers past customer complaints)
- **Tool Use:** Leverages APIs, databases, browsers (e.g., checks inventory before promising delivery)
- **Collaboration:** Works with other AIs/humans (e.g., hands off to live agent if user is angry)

---

## No-Code Example

Zapier + ChatGPT can create a basic agent that:

- Reads customer emails
- Classifies urgency
- Drafts replies (with human approval)

---

## PM Responsibilities for Agentic AI

- **Define Boundaries:**  
    "The AI can approve refunds up to $50 without human review."
- **Guardrails:**  
    "Never promise delivery dates—always check inventory first."
- **Evaluation Metrics:**  
    Success rate, number of human escalations, time-to-resolution

### Template for Specs

**Goal:** Reduce refund processing time by 50%  
**Actions:**
1. Verify purchase date + policy
2. Approve if <30 days AND not electronics
3. Flag exceptions to human

**Constraints:** Never approve >$100 without review

---

## Risks to Mitigate

- **Over-Autonomy:** Set clear "escalation thresholds"
- **Bias:** Audit decisions (e.g., "Does AI deny more refunds for certain demographics?")
- **User Trust:** Always disclose AI involvement (e.g., "AI Assistant is helping you")

---

## No-Code Tools to Experiment

- **AutoGen (Microsoft):** Visual agent builder
- **LangChain:** Connect LLMs to workflows
- **Zapier Interfaces:** Build AI agents with triggers/actions
