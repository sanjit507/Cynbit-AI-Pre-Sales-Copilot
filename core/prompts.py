"""
System Prompts and Few-Shot Templates for Cynbit Pre-Sales Copilot
"""

CYNBIT_COPILOT_SYSTEM_PROMPT = """You are the Principal Solutions Architect at Cynbit Technologies (Jaipur, India - https://www.cynbit.in).
Your motto is "The Optimistic Architect: The speed of a startup, the rigor of an enterprise."
Your objective is to ingest a prospective client's unstructured business requirements and synthesize an enterprise-grade technical solution architecture, technology stack mapping, sprint breakdown, and commercial proposal.

You must strictly ground your technology choices in Cynbit's validated capabilities:
- Frontend: Next.js 14/15 App Router, React 19, TypeScript, TailwindCSS, Flutter
- Backend: Python (FastAPI), Go, Rust, Node.js/NestJS
- AI/ML & Agents: LangGraph, LlamaIndex, OpenAI GPT-4o, Claude 3.5 Sonnet, Llama 3.3, Gemini 1.5, Whisper/ElevenLabs
- Databases: PostgreSQL (Supabase/Neon), Redis, Qdrant/Pinecone Vector DB
- Cloud & DevOps: AWS (ECS, Lambda, S3, Cognito), Azure, Docker, Kubernetes, GitHub Actions CI/CD
- Reference Products: Cynbit Studio (EdTech code lab), TenantEase (PropTech SaaS), Revio (Reputation & Sentiment AI)

Always maintain an authoritative, structured, highly professional tone.
Generate valid, self-contained Mermaid.js diagram syntax (graph TD).
"""

PROPOSAL_TEMPLATE = """# Technical Solution Architecture & Project Proposal
**Client Name:** {client_name}  
**Prepared By:** Cynbit Technologies Pvt. Ltd., Jaipur, India  
**Lead Solutions Architect:** AI Solutions Architecture Group  
**Date:** {date_str}  
**Target Delivery Window:** {timeline_weeks} Weeks ({num_sprints} Sprints)  

---

## 1. Executive Summary & Problem Understanding
{executive_summary}

---

## 2. Recommended Solution Architecture
{architecture_description}

### 2.1 System Architecture Flowchart
```mermaid
{mermaid_code}
```

---

## 3. Recommended Cynbit Technology Stack
{tech_stack_breakdown}

---

## 4. Work Breakdown Structure (WBS) & Sprint Schedule
{sprint_breakdown}

---

## 5. Team Composition & Resource Allocation
{team_allocation}

---

## 6. Commercials & Investment Summary
- **Total Development Sprints:** {num_sprints} Sprints ({timeline_weeks} Weeks)
- **Estimated Engineering Effort:** ~{total_hours} Billable Hours
- **Estimated Project Investment:** ${budget_usd:,} USD (₹{budget_inr:,} INR)
- **Warranty & Post-Launch Support:** 30 Days Included SLA with 99.9% uptime commitment

---

## 7. Why Cynbit Technologies?
- **Startup Speed, Enterprise Rigor:** Rapid modular delivery with zero-trust architectural security.
- **Production AI Expertise:** Proven track record building autonomous agents and proprietary platforms like *Revio*, *TenantEase*, and *Cynbit Studio*.
- **Direct Executive Collaboration:** Weekly sprint demos and milestone-based transparent governance.
"""
