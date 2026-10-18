"""
Core Pipeline Engine: Ingestion, Architecture Synthesis, Estimation & Proposal Generation
Supports both Live LLM APIs (Groq, OpenAI, Gemini) and an Intelligent Deterministic Fallback.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field

from core.kb import (
    CYNBIT_COMPANY_INFO,
    CYNBIT_STACK_CATALOG,
    PROPRIETARY_SAAS_PATTERNS,
    COMMERCIAL_METRICS
)
from core.prompts import CYNBIT_COPILOT_SYSTEM_PROMPT, PROPOSAL_TEMPLATE


class ArchitecturalComponent(BaseModel):
    layer: str
    component_name: str
    technology: str
    rationale: str


class SprintPlan(BaseModel):
    sprint_number: int
    title: str
    weeks: str
    milestones: List[str]


class ArchitectureProposal(BaseModel):
    client_name: str
    industry: str
    project_title: str
    executive_summary: str
    architecture_overview: str
    mermaid_diagram: str
    components: List[ArchitecturalComponent]
    tech_stack: Dict[str, List[str]]
    sprints: List[SprintPlan]
    total_weeks: int
    total_hours: int
    budget_usd: int
    budget_inr: int
    team_members: List[Dict[str, Any]]
    full_markdown_proposal: str


class PreSalesPipeline:
    def __init__(self, api_key: Optional[str] = None, provider: str = "auto"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.provider = provider

    def analyze_and_generate(
        self,
        client_name: str,
        brief: str,
        industry: Optional[str] = None,
        budget_override: Optional[int] = None,
        timeline_weeks_override: Optional[int] = None
    ) -> ArchitectureProposal:
        """
        Executes multi-stage reasoning to generate full architecture and proposal.
        """
        # Determine domain and key drivers from brief
        detected_domain = self._detect_domain(brief, industry)
        
        # If API key is provided and valid format, attempt live generation
        if self.api_key and len(self.api_key.strip()) > 10:
            try:
                return self._generate_with_llm(
                    client_name, brief, detected_domain, budget_override, timeline_weeks_override
                )
            except Exception as e:
                # Graceful fallback to heuristic engine on API failure
                print(f"LLM API Call failed ({e}), falling back to Heuristic Engine.")

        # Default / Fallback: Intelligent Semantic Heuristic Engine
        return self._generate_with_heuristics(
            client_name, brief, detected_domain, budget_override, timeline_weeks_override
        )

    def _detect_domain(self, brief: str, specified_industry: Optional[str]) -> str:
        text = (brief + " " + (specified_industry or "")).lower()
        if any(w in text for w in ["clinic", "patient", "doctor", "health", "dental", "medical", "hospital"]):
            return "Healthcare & Clinics"
        elif any(w in text for w in ["tenant", "property", "rent", "real estate", "building", "lease", "estate"]):
            return "PropTech & Real Estate"
        elif any(w in text for w in ["invoice", "procurement", "logistics", "freight", "cargo", "erp", "supply chain"]):
            return "Enterprise Logistics & FinTech"
        elif any(w in text for w in ["code", "student", "academy", "learning", "course", "exam", "education", "edtech"]):
            return "EdTech & Developer Platforms"
        elif any(w in text for w in ["review", "reputation", "feedback", "rating", "google review"]):
            return "Reputation & Sentiment SaaS"
        else:
            return specified_industry or "Enterprise SaaS & AI Automation"

    def _generate_with_heuristics(
        self,
        client_name: str,
        brief: str,
        domain: str,
        budget_override: Optional[int] = None,
        timeline_override: Optional[int] = None
    ) -> ArchitectureProposal:
        """
        High-precision deterministic engine generating verified Cynbit architecture.
        """
        today_str = datetime.now().strftime("%B %d, %Y")
        text_lower = brief.lower()

        # Domain specific tailoring
        if domain == "Healthcare & Clinics":
            project_title = f"{client_name} Omnichannel AI Healthcare & Review Ecosystem"
            reference_pattern = "Revio + Autonomous Voice AI Agent"
            fe_tech = ["Next.js 14 App Router", "React 19", "TailwindCSS", "Flutter (Patient App)"]
            be_tech = ["Python (FastAPI Async)", "Celery / Redis Queues", "Twilio / Deepgram Voice API"]
            ai_tech = ["LangGraph Multi-Agent Workflows", "OpenAI GPT-4o Realtime", "Llama 3.3 Sentiment Engine"]
            db_tech = ["PostgreSQL 16 (AWS RDS)", "Qdrant Vector DB", "Redis Caching"]
            cloud_tech = ["AWS ECS Fargate", "AWS S3 HIPAA Encrypted", "Zero-Trust JWT Auth"]
            base_weeks = 8
            base_hours = 380

            mermaid_code = """graph TD
    subgraph ClientLayer [Client & Patient Touchpoints]
        PatientWeb[Patient Portal Next.js / Mobile]
        PhoneCall[Inbound Phone Calls - PSTN]
        GMB[Google Business Reviews]
    end

    subgraph GatewayLayer [API & Ingestion Gateway]
        APIGateway[Cloudflare CDN & API Gateway]
        VoiceGateway[Twilio + Deepgram Audio Stream]
        ReviewWebhook[Review Ingestion Webhook]
    end

    subgraph CoreServices [Cynbit Scalable Microservices]
        BookingAPI[FastAPI Booking & Calendar Engine]
        ReputationEngine[Revio Sentiment & Crisis Service]
        VoiceAgent[Autonomous Healthcare Voice Agent]
    end

    subgraph StorageLayer [Persistent & Vector Storage]
        Postgres[(PostgreSQL RDS - Patient Records)]
        QdrantDB[(Qdrant Vector Store - Clinical FAQs)]
        RedisCache[(Redis Cache & Task Queue)]
    end

    PatientWeb --> APIGateway
    PhoneCall --> VoiceGateway
    GMB --> ReviewWebhook

    VoiceGateway --> VoiceAgent
    APIGateway --> BookingAPI
    ReviewWebhook --> ReputationEngine

    VoiceAgent --> QdrantDB
    VoiceAgent --> BookingAPI
    BookingAPI --> Postgres
    ReputationEngine --> Postgres
    BookingAPI --> RedisCache
    ReputationEngine --> RedisCache"""

        elif domain == "PropTech & Real Estate":
            project_title = f"{client_name} Intelligent Property, Tenant & Rent Automation"
            reference_pattern = "TenantEase Architecture Blueprint"
            fe_tech = ["Next.js 15 App Router", "TypeScript", "TailwindCSS", "Mobile Responsive PWA"]
            be_tech = ["Python (FastAPI)", "Celery Distributed Workers", "WhatsApp Cloud API"]
            ai_tech = ["Cognitive Document AI (OCR)", "LayoutLM & GPT-4o Vision for Lease Parsing"]
            db_tech = ["PostgreSQL 16 (Supabase / AWS RDS)", "Redis Caching"]
            cloud_tech = ["AWS ECS Fargate", "AWS S3 Secure Vault", "GitHub Actions CI/CD"]
            base_weeks = 8
            base_hours = 340

            mermaid_code = """graph TD
    subgraph Users [User Portals]
        Landlord[Property Manager Dashboard]
        Tenant[Tenant Self-Service Portal]
    end

    subgraph Ingestion [Ingestion & Processing]
        API[FastAPI Gateway]
        DocAI[Document OCR & Lease Extraction Engine]
        MsgQueue[Celery + Redis Worker Queue]
    end

    subgraph BusinessLogic [Core Application Logic]
        RentEngine[Automated Rent & Billing Engine]
        LeaseEngine[Lease & KYC Verification Service]
        WhatsAppBot[Automated WhatsApp Rent Chaser]
    end

    subgraph Data [Storage Layer]
        DB[(PostgreSQL Primary DB)]
        S3Vault[(AWS S3 Encrypted Lease Docs)]
        Cache[(Redis Payment Cache)]
    end

    Landlord --> API
    Tenant --> API
    API --> DocAI
    API --> MsgQueue
    DocAI --> S3Vault
    DocAI --> LeaseEngine
    MsgQueue --> RentEngine
    MsgQueue --> WhatsAppBot
    RentEngine --> DB
    RentEngine --> Cache
    LeaseEngine --> DB"""

        elif domain == "Enterprise Logistics & FinTech":
            project_title = f"{client_name} Cognitive Document Processing & SAP 3-Way Matching Engine"
            reference_pattern = "Cynbit LLM Cognitive Automation Suite"
            fe_tech = ["Next.js 14 Dashboard", "React 19", "TailwindCSS", "Ag-Grid Enterprise"]
            be_tech = ["Python (FastAPI)", "Go (High-Throughput File Ingestion)", "Celery Cluster"]
            ai_tech = ["Multi-Modal Document Parsing", "Fine-Tuned Llama 3.3 for Line-Item Extraction", "Anomaly Detection"]
            db_tech = ["PostgreSQL 16", "Qdrant Vector DB", "Redis Cluster"]
            cloud_tech = ["AWS ECS / EKS", "AWS S3 Document Lake", "SAP RFC / REST Connector"]
            base_weeks = 10
            base_hours = 460

            mermaid_code = """graph TD
    subgraph InboundDocs [Inbound Multichannel Ingestion]
        CarrierEmail[Carrier Emails & PDF Attachments]
        VendorPortal[Vendor Web Upload Next.js]
        FTPStream[Legacy SFTP Stream]
    end

    subgraph Pipeline [Cognitive Extraction Pipeline]
        IngestService[Go Ingestion Worker]
        DocProcessor[Multi-Modal LayoutLM + LLM OCR]
        AnomalyDetector[Anomaly & Duplicate Detection Agent]
    end

    subgraph Matching [3-Way Matching & ERP Integration]
        SAPBridge[SAP ERP Connector - RFC/REST]
        ExceptionUI[Human-in-the-Loop Review Dashboard]
    end

    subgraph Storage [Enterprise Storage & Audit]
        DocStore[(AWS S3 Versioned Document Store)]
        Postgres[(PostgreSQL Audit & Extraction Ledger)]
        VectorDB[(Qdrant Vector Index)]
    end

    CarrierEmail --> IngestService
    VendorPortal --> IngestService
    FTPStream --> IngestService

    IngestService --> DocProcessor
    DocProcessor --> DocStore
    DocProcessor --> AnomalyDetector
    AnomalyDetector --> SAPBridge
    AnomalyDetector --> ExceptionUI
    SAPBridge --> Postgres
    ExceptionUI --> Postgres"""

        elif domain == "EdTech & Developer Platforms":
            project_title = f"{client_name} Sandboxed AI Code Evaluation & Skill Radar Lab"
            reference_pattern = "Cynbit Studio Architecture Blueprint"
            fe_tech = ["Next.js 15 App Router", "Monaco Code Editor", "TailwindCSS", "Chart.js / Radar Engine"]
            be_tech = ["Python (FastAPI)", "Docker Sandbox Daemon (Isolated Execution)", "gRPC"]
            ai_tech = ["AST Parser + Claude 3.5 Sonnet / Gemini 1.5", "AI Mock Interview Agent"]
            db_tech = ["PostgreSQL 16 (Neon / Supabase)", "Redis Leaderboards", "pgvector"]
            cloud_tech = ["AWS ECS Fargate", "Zero-Trust Linux Container Sandboxing", "CloudWatch"]
            base_weeks = 8
            base_hours = 360

            mermaid_code = """graph TD
    subgraph StudentUI [Student Learning Environment]
        CodeIDE[Monaco Code Editor & Terminal UI]
        InterviewBot[AI Mock Interview Companion]
        RadarView[Skill Radar & Progress Dashboard]
    end

    subgraph SecurityGate [Security & Execution Gateway]
        Gateway[FastAPI Security & Auth Gateway]
        SandboxDaemon[Isolated Docker Execution Sandbox]
    end

    subgraph EvaluationCore [Intelligent Evaluation Engine]
        OutputVerifier[Unit Test & Edge Case Verifier]
        LLMReviewer[Semantic Code Quality & Complexity Reviewer]
        SkillEngine[Adaptive XP & Skill Graph Calculator]
    end

    subgraph Persistence [State & Analytics]
        UserDB[(PostgreSQL Student Profiles)]
        LeaderboardCache[(Redis Cache & Live Leaderboard)]
    end

    CodeIDE --> Gateway
    InterviewBot --> Gateway
    Gateway --> SandboxDaemon
    SandboxDaemon --> OutputVerifier
    OutputVerifier --> LLMReviewer
    LLMReviewer --> SkillEngine
    SkillEngine --> UserDB
    SkillEngine --> LeaderboardCache
    LeaderboardCache --> RadarView"""

        else:
            project_title = f"{client_name} Autonomous AI Transformation Platform"
            reference_pattern = "Cynbit Autonomous Agent Suite"
            fe_tech = ["Next.js 14 App Router", "React 19", "TailwindCSS", "TypeScript"]
            be_tech = ["Python (FastAPI)", "Redis Queues", "Async Worker Cluster"]
            ai_tech = ["LangGraph Multi-Agent Engine", "OpenAI GPT-4o / Claude 3.5", "RAG Pipeline"]
            db_tech = ["PostgreSQL 16", "Qdrant Vector Database", "Redis Cache"]
            cloud_tech = ["AWS ECS Fargate", "AWS S3", "Docker", "GitHub Actions"]
            base_weeks = 8
            base_hours = 360

            mermaid_code = """graph TD
    subgraph ClientTier [Frontend Presentation]
        WebUI[Next.js 14 Modern Web Dashboard]
        MobileWeb[Responsive Mobile App]
    end

    subgraph ServiceTier [Cynbit Backend Services]
        Gateway[API Gateway & Rate Limiter]
        CoreEngine[FastAPI Business Logic]
        AgentCluster[Autonomous AI Agent Cluster]
    end

    subgraph DataTier [Storage & Caching]
        Postgres[(PostgreSQL Primary Store)]
        VectorStore[(Qdrant Vector DB)]
        Redis[(Redis Cache)]
    end

    WebUI --> Gateway
    MobileWeb --> Gateway
    Gateway --> CoreEngine
    CoreEngine --> AgentCluster
    AgentCluster --> VectorStore
    CoreEngine --> Postgres
    CoreEngine --> Redis"""

        # Overrides & calculations
        total_weeks = timeline_override or base_weeks
        total_sprints = max(2, total_weeks // 2)
        total_hours = (total_weeks * 45) if not timeline_override else (timeline_override * 45)
        
        rate_usd = COMMERCIAL_METRICS["blended_hourly_rate_usd"]
        fx_inr = COMMERCIAL_METRICS["inr_fx_rate"]
        
        calculated_budget_usd = budget_override or (total_hours * rate_usd)
        calculated_budget_inr = calculated_budget_usd * fx_inr

        # Sprints breakdown
        sprints_list = [
            SprintPlan(
                sprint_number=1,
                title="Foundation, Architecture & Data Contracts",
                weeks="Weeks 1 - 2",
                milestones=[
                    "Finalize technical specifications and OpenAPI contracts",
                    "Setup GitHub CI/CD pipelines and AWS/Azure cloud environments",
                    "Initialize Next.js frontend framework and database schemas"
                ]
            ),
            SprintPlan(
                sprint_number=2,
                title="Core Backend APIs & Data Ingestion",
                weeks="Weeks 3 - 4",
                milestones=[
                    "Implement FastAPI microservices and authentication layer",
                    "Deploy PostgreSQL relational models and Redis caching layer",
                    "Build initial data ingestion connectors and validation pipelines"
                ]
            ),
            SprintPlan(
                sprint_number=3,
                title="AI Agent Workflows & Cognitive Pipeline",
                weeks="Weeks 5 - 6",
                milestones=[
                    "Integrate LLM reasoning pipelines and vector retrieval",
                    "Implement automated agents and task execution workers",
                    "Connect frontend interfaces with backend streaming APIs"
                ]
            ),
            SprintPlan(
                sprint_number=4,
                title="Integration, Security Hardening & Client Testing",
                weeks="Weeks 7 - 8",
                milestones=[
                    "End-to-end integration testing and performance benchmarking",
                    "Zero-trust security audit, rate limiting, and role-based permissions",
                    "Conduct User Acceptance Testing (UAT) and staging deployment"
                ]
            )
        ]

        if total_sprints > 4:
            sprints_list.append(
                SprintPlan(
                    sprint_number=5,
                    title="Scale Optimization, Production Launch & Handoff",
                    weeks=f"Weeks 9 - {total_weeks}",
                    milestones=[
                        "Production cutover to AWS ECS with auto-scaling",
                        "Setup Datadog / CloudWatch monitoring and alert triggers",
                        "Executive stakeholder walkthrough, technical documentation & SLA sign-off"
                    ]
                )
            )

        # Team allocation
        team_members = [
            {"role": "Principal Solutions Architect", "fte": "0.25 FTE", "tasks": "System architecture, security design, milestone reviews"},
            {"role": "Senior AI / ML Engineer", "fte": "1.00 FTE", "tasks": "Agentic workflows, prompt tuning, vector search, LLM integrations"},
            {"role": "Senior Full-Stack Engineer", "fte": "2.00 FTE", "tasks": "Next.js UI, FastAPI endpoints, database performance, caching"},
            {"role": "QA & Cloud DevOps Engineer", "fte": "0.50 FTE", "tasks": "Docker orchestration, CI/CD pipelines, load testing, security"}
        ]

        # Components breakdown
        components = [
            ArchitecturalComponent(
                layer="Presentation Layer",
                component_name="Enterprise Web Application",
                technology=fe_tech[0],
                rationale="Provides blazing-fast server-side rendering, SEO readiness, and reactive client dashboards."
            ),
            ArchitecturalComponent(
                layer="API & Application Layer",
                component_name="Asynchronous Microservices",
                technology=be_tech[0],
                rationale="High-throughput Python asyncio backend with native Pydantic typing and instant OpenAPI docs."
            ),
            ArchitecturalComponent(
                layer="Cognitive Intelligence Layer",
                component_name="Autonomous Reasoning Engine",
                technology=ai_tech[0],
                rationale="Executes multi-step decision logic, semantic extraction, and structured output parsing."
            ),
            ArchitecturalComponent(
                layer="Data & Caching Layer",
                component_name="Relational & Vector Hybrid DB",
                technology=f"{db_tech[0]} + {db_tech[1]}",
                rationale="Ensures ACID compliance for operational records combined with sub-millisecond semantic search."
            ),
            ArchitecturalComponent(
                layer="Cloud & Security Layer",
                component_name="Scalable Container Infrastructure",
                technology=cloud_tech[0],
                rationale="Zero-server maintenance container orchestration with automated horizontal auto-scaling."
            )
        ]

        tech_stack = {
            "Frontend": fe_tech,
            "Backend & APIs": be_tech,
            "AI / ML & Agents": ai_tech,
            "Databases & Storage": db_tech,
            "DevOps & Security": cloud_tech
        }

        # Executive summary text
        executive_summary = (
            f"{client_name} operates in the {domain} sector with a clear opportunity to modernize its operations "
            f"through custom AI automation and resilient digital architecture. Based on the client brief, the primary "
            f"operational pain points involve manual coordination bottlenecks, slow response cycles, and decentralized data. "
            f"Cynbit Technologies recommends architecting a high-performance, modular system drawing directly from our "
            f"proven enterprise blueprints (specifically leveraging patterns from {reference_pattern}). This solution "
            f"delivers automated intelligence, end-to-end auditability, and immediate cost savings while scaling seamlessly."
        )

        architecture_description = (
            f"The proposed architecture employs a decoupled 4-tier topology: (1) A reactive Next.js presentation layer, "
            f"(2) A secure API Gateway and FastAPI service mesh, (3) An autonomous AI reasoning and vector search engine, "
            f"and (4) A high-performance PostgreSQL and Redis storage backbone hosted on AWS. "
            f"The architecture is engineered for 99.9% availability, zero-trust role-based access, and sub-second response times."
        )

        # Build sprint markdown
        sprint_md = ""
        for s in sprints_list:
            sprint_md += f"### Sprint {s.sprint_number}: {s.title} ({s.weeks})\n"
            for m in s.milestones:
                sprint_md += f"- [ ] {m}\n"
            sprint_md += "\n"

        # Build tech stack markdown
        stack_md = ""
        for cat, items in tech_stack.items():
            stack_md += f"- **{cat}:** {', '.join(items)}\n"

        # Build team markdown
        team_md = ""
        for tm in team_members:
            team_md += f"- **{tm['role']} ({tm['fte']}):** {tm['tasks']}\n"

        # Render full markdown proposal
        full_proposal = PROPOSAL_TEMPLATE.format(
            client_name=client_name,
            date_str=today_str,
            timeline_weeks=total_weeks,
            num_sprints=total_sprints,
            executive_summary=executive_summary,
            architecture_description=architecture_description,
            mermaid_code=mermaid_code,
            tech_stack_breakdown=stack_md,
            sprint_breakdown=sprint_md,
            team_allocation=team_md,
            total_hours=total_hours,
            budget_usd=calculated_budget_usd,
            budget_inr=calculated_budget_inr
        )

        return ArchitectureProposal(
            client_name=client_name,
            industry=domain,
            project_title=project_title,
            executive_summary=executive_summary,
            architecture_overview=architecture_description,
            mermaid_diagram=mermaid_code,
            components=components,
            tech_stack=tech_stack,
            sprints=sprints_list,
            total_weeks=total_weeks,
            total_hours=total_hours,
            budget_usd=calculated_budget_usd,
            budget_inr=calculated_budget_inr,
            team_members=team_members,
            full_markdown_proposal=full_proposal
        )

    def _generate_with_llm(
        self,
        client_name: str,
        brief: str,
        domain: str,
        budget_override: Optional[int],
        timeline_override: Optional[int]
    ) -> ArchitectureProposal:
        """
        Calls live LLM provider (OpenAI or Groq compatible endpoint) using standard requests.
        """
        import requests

        is_groq = self.api_key.startswith("gsk_")
        url = "https://api.groq.com/openai/v1/chat/completions" if is_groq else "https://api.openai.com/v1/chat/completions"
        model_name = "llama-3.3-70b-versatile" if is_groq else "gpt-4o-mini"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        user_prompt = f"""
Client Name: {client_name}
Industry: {domain}
Client Problem Brief:
{brief}

Synthesize a comprehensive technical proposal. Ground in Cynbit's validated stack (Next.js, FastAPI, Rust/Go, LangGraph, Qdrant, PostgreSQL, AWS).
Return the proposal adhering strictly to this markdown structure:
1. Executive Summary
2. Recommended Architecture
3. Mermaid.js Flowchart (valid graph TD syntax)
4. Recommended Cynbit Tech Stack
5. Work Breakdown Structure (Sprints)
6. Commercials (Total Weeks: {timeline_override or 8}, Budget USD: {budget_override or 25000})
"""

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": CYNBIT_COPILOT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2500
        }

        response = requests.post(url, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        res_data = response.json()
        generated_text = res_data["choices"][0]["message"]["content"]

        # Parse mermaid diagram from output
        mermaid_match = re.search(r"```mermaid\n(.*?)\n```", generated_text, re.DOTALL)
        mermaid_code = mermaid_match.group(1).strip() if mermaid_match else "graph TD\nClient --> API --> Core --> DB"

        total_weeks = timeline_override or 8
        total_hours = total_weeks * 45
        budget_usd = budget_override or (total_hours * 45)
        budget_inr = budget_usd * 85

        return ArchitectureProposal(
            client_name=client_name,
            industry=domain,
            project_title=f"{client_name} AI Solution Architecture",
            executive_summary=f"Custom AI solution designed by Cynbit Technologies for {client_name}.",
            architecture_overview="Enterprise decoupled multi-tier architecture with autonomous AI capabilities.",
            mermaid_diagram=mermaid_code,
            components=[],
            tech_stack=CYNBIT_STACK_CATALOG,
            sprints=[],
            total_weeks=total_weeks,
            total_hours=total_hours,
            budget_usd=budget_usd,
            budget_inr=budget_inr,
            team_members=[],
            full_markdown_proposal=generated_text
        )
