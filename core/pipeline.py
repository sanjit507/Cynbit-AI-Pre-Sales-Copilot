"""
Core Pipeline Engine: Ingestion, Architecture Synthesis, Estimation & Proposal Generation
Full Google Gemini AI Integration with Deterministic Fallback.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    generated_by: str = "Cynbit Blueprint Engine"


class PreSalesPipeline:
    def __init__(self, engine_mode: str = "gemini"):
        self.engine_mode = engine_mode
        self.gemini_api_key = (
            os.getenv("GEMINI_API_KEY") or 
            os.getenv("GOOGLE_API_KEY") or 
            ""
        ).strip()

    def has_valid_gemini_key(self) -> bool:
        return bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here")

    def analyze_and_generate(
        self,
        client_name: str,
        brief: str,
        industry: Optional[str] = None,
        budget_override: Optional[int] = None,
        timeline_weeks_override: Optional[int] = None,
        force_engine: Optional[str] = None
    ) -> ArchitectureProposal:
        """
        Executes multi-stage reasoning to generate full architecture and proposal.
        """
        engine_to_use = force_engine or self.engine_mode
        detected_domain = self._detect_domain(brief, industry)

        # If user selected Gemini and a key is available in .env
        if engine_to_use == "gemini" and self.has_valid_gemini_key():
            try:
                return self._generate_with_gemini(
                    client_name=client_name,
                    brief=brief,
                    domain=detected_domain,
                    budget_override=budget_override,
                    timeline_override=timeline_weeks_override
                )
            except Exception as e:
                print(f"[Gemini API Notice] API execution failed: {e}. Falling back to Blueprint Engine.")

        # Fallback / Rule engine
        return self._generate_with_heuristics(
            client_name=client_name,
            brief=brief,
            domain=detected_domain,
            budget_override=budget_override,
            timeline_override=timeline_weeks_override
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
        elif any(w in text for w in ["wordpress", "woocommerce", "shopify", "cms", "ecommerce", "store", "shop"]):
            return "E-Commerce & Digital Commerce"
        elif any(w in text for w in ["review", "reputation", "feedback", "rating", "google review"]):
            return "Reputation & Sentiment SaaS"
        else:
            return specified_industry or "Enterprise Custom Software & AI"

    def _generate_with_gemini(
        self,
        client_name: str,
        brief: str,
        domain: str,
        budget_override: Optional[int],
        timeline_override: Optional[int]
    ) -> ArchitectureProposal:
        """
        Direct integration with Google Gemini AI API.
        Generates full architecture, Mermaid diagram, and proposal tailored to any custom client request.
        """
        # Try gemini-1.5-flash or gemini-2.0-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        target_weeks = timeline_override or 8
        target_sprints = max(2, target_weeks // 2)
        target_hours = target_weeks * 45
        target_budget_usd = budget_override or (target_hours * COMMERCIAL_METRICS["blended_hourly_rate_usd"])
        target_budget_inr = target_budget_usd * COMMERCIAL_METRICS["inr_fx_rate"]
        today_str = datetime.now().strftime("%B %d, %Y")

        system_instruction = f"""
You are the Principal Solutions Architect at Cynbit Technologies (https://www.cynbit.in), Jaipur, India.
Your motto: "The Optimistic Architect: The speed of a startup, the rigor of an enterprise."
You must analyze the client's problem brief and generate a complete, structured technical solution.

Ground your architecture in modern production technologies that Cynbit uses:
- Modern Web/Mobile: Next.js 14/15, React 19, TypeScript, TailwindCSS, Flutter, or Headless WordPress/Shopify if requested.
- Scalable Backends: Python (FastAPI), Go, Rust, Node.js.
- AI & Automation: LangGraph, LlamaIndex, OpenAI GPT-4o, Claude 3.5, Google Gemini, Document AI, AI Voice Agents.
- Data Layer: PostgreSQL 16 (AWS RDS/Supabase), Redis Caching, Qdrant / Pinecone Vector Store.
- Cloud & Security: AWS (ECS, Lambda, S3, CloudFront), Azure, Docker, Zero-Trust OAuth2.

CRITICAL MERMAID RULES:
- Always wrap ALL node labels in double quotes: NodeID["Label Text"]
- Never use the ampersand character (&) inside any Mermaid label. Always spell out "and" instead.
- For subgraph titles, use: subgraph ID ["Title Text"]
- For database cylinder nodes, use: DB[("Database Name")]

You MUST respond strictly with valid JSON (no surrounding markdown code blocks, just pure JSON).
The JSON MUST follow this exact schema:
{{
  "project_title": "String",
  "executive_summary": "String (2-3 paragraphs explaining client's pain points and Cynbit's strategic solution)",
  "architecture_overview": "String (comprehensive technical explanation of the layers)",
  "mermaid_diagram": "graph TD\\n... (valid Mermaid.js flowchart code without backticks)",
  "components": [
    {{
      "layer": "Presentation Layer / API Gateway / Core Logic / AI Engine / Database",
      "component_name": "String",
      "technology": "String",
      "rationale": "String"
    }}
  ],
  "tech_stack": {{
    "Frontend": ["item1", "item2"],
    "Backend & APIs": ["item1", "item2"],
    "AI / ML & Agents": ["item1", "item2"],
    "Databases & Storage": ["item1", "item2"],
    "DevOps & Security": ["item1", "item2"]
  }},
  "sprints": [
    {{
      "sprint_number": 1,
      "title": "String",
      "weeks": "Weeks 1 - 2",
      "milestones": ["Milestone 1", "Milestone 2", "Milestone 3"]
    }}
  ],
  "team_members": [
    {{
      "role": "Principal Solutions Architect",
      "fte": "0.25 FTE",
      "tasks": "Architecture design and security audit"
    }},
    {{
      "role": "Senior AI / Full-Stack Engineer",
      "fte": "2.00 FTE",
      "tasks": "Implementation of APIs and UI"
    }}
  ]
}}
"""

        user_content = f"""
CLIENT SPECIFICATIONS:
- Client Name: {client_name}
- Industry: {domain}
- Target Timeline: {target_weeks} Weeks ({target_sprints} Sprints)
- Target Investment: ${target_budget_usd:,} USD (₹{target_budget_inr:,} INR)
- Client Brief & Requirements:
{brief}

Synthesize a production-ready solution now in valid JSON format.
"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_instruction + "\n\n" + user_content}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 3500,
                "responseMimeType": "application/json"
            }
        }

        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, headers=headers, json=payload, timeout=35)
        
        # If model error or rate limit, retry with gemini-2.0-flash
        if resp.status_code != 200:
            url_fallback = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_api_key}"
            resp = requests.post(url_fallback, headers=headers, json=payload, timeout=35)

        resp.raise_for_status()
        resp_json = resp.json()
        raw_output = resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Clean JSON if wrapped in markdown
        cleaned_json = raw_output
        if cleaned_json.startswith("```json"):
            cleaned_json = cleaned_json[7:]
        if cleaned_json.endswith("```"):
            cleaned_json = cleaned_json[:-3]
        cleaned_json = cleaned_json.strip()

        data = json.loads(cleaned_json)

        # Parse components
        components_list = []
        for c in data.get("components", []):
            components_list.append(
                ArchitecturalComponent(
                    layer=c.get("layer", "Application Layer"),
                    component_name=c.get("component_name", "Core Service"),
                    technology=c.get("technology", "Python / Next.js"),
                    rationale=c.get("rationale", "Scalable performance")
                )
            )

        # Parse sprints
        sprints_list = []
        for s in data.get("sprints", []):
            sprints_list.append(
                SprintPlan(
                    sprint_number=s.get("sprint_number", 1),
                    title=s.get("title", "Development Sprint"),
                    weeks=s.get("weeks", "Weeks 1 - 2"),
                    milestones=s.get("milestones", ["Implementation and testing"])
                )
            )

        # Build sprint markdown
        sprint_md = ""
        for s in sprints_list:
            sprint_md += f"### Sprint {s.sprint_number}: {s.title} ({s.weeks})\n"
            for m in s.milestones:
                sprint_md += f"- [ ] {m}\n"
            sprint_md += "\n"

        # Build tech stack markdown
        tech_stack = data.get("tech_stack", CYNBIT_STACK_CATALOG)
        stack_md = ""
        for cat, items in tech_stack.items():
            stack_md += f"- **{cat}:** {', '.join(items)}\n"

        # Build team markdown
        team_members = data.get("team_members", [
            {"role": "Principal Solutions Architect", "fte": "0.25 FTE", "tasks": "Architecture & Security"},
            {"role": "Senior Full-Stack Engineer", "fte": "2.00 FTE", "tasks": "Application Development"}
        ])
        team_md = ""
        for tm in team_members:
            team_md += f"- **{tm['role']} ({tm['fte']}):** {tm['tasks']}\n"

        mermaid_raw = data.get("mermaid_diagram", "graph TD\n    Client[Client App] --> Gateway[API Gateway]\n    Gateway --> CoreAPI[Backend Service]\n    CoreAPI --> DB[(Database)]")
        # Strip code blocks or quotes
        mermaid_clean = re.sub(r"^```(?:mermaid)?\s*", "", mermaid_raw.strip(), flags=re.IGNORECASE)
        mermaid_clean = re.sub(r"\s*```$", "", mermaid_clean.strip())
        mermaid_clean = mermaid_clean.strip()
        if not (mermaid_clean.startswith("graph") or mermaid_clean.startswith("flowchart")):
            mermaid_clean = "graph TD\n    " + mermaid_clean
        # Sanitize ampersands inside labels - Mermaid.js breaks on unescaped &
        mermaid_clean = re.sub(r'(?<=\[)([^\]]*?)&([^\]]*?)(?=\])', lambda m: m.group(1) + 'and' + m.group(2), mermaid_clean)
        mermaid_clean = re.sub(r'(?<=\[")([^"]*?)&([^"]*?)(?="\])', lambda m: m.group(1) + 'and' + m.group(2), mermaid_clean)
        mermaid_code = mermaid_clean

        full_proposal = PROPOSAL_TEMPLATE.format(
            client_name=client_name,
            date_str=today_str,
            timeline_weeks=target_weeks,
            num_sprints=len(sprints_list) or target_sprints,
            executive_summary=data.get("executive_summary", "Custom technical solution crafted by Cynbit."),
            architecture_description=data.get("architecture_overview", "Decoupled multi-tier enterprise architecture."),
            mermaid_code=mermaid_code,
            tech_stack_breakdown=stack_md,
            sprint_breakdown=sprint_md,
            team_allocation=team_md,
            total_hours=target_hours,
            budget_usd=target_budget_usd,
            budget_inr=target_budget_inr
        )

        return ArchitectureProposal(
            client_name=client_name,
            industry=domain,
            project_title=data.get("project_title", f"{client_name} Custom Solution Architecture"),
            executive_summary=data.get("executive_summary", ""),
            architecture_overview=data.get("architecture_overview", ""),
            mermaid_diagram=mermaid_code,
            components=components_list,
            tech_stack=tech_stack,
            sprints=sprints_list,
            total_weeks=target_weeks,
            total_hours=target_hours,
            budget_usd=target_budget_usd,
            budget_inr=target_budget_inr,
            team_members=team_members,
            full_markdown_proposal=full_proposal,
            generated_by="Google Gemini AI (Live Model)"
        )

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
    subgraph ClientLayer ["Client and Patient Touchpoints"]
        PatientWeb["Patient Portal - Next.js / Mobile"]
        PhoneCall["Inbound Phone Calls - PSTN"]
        GMB["Google Business Reviews"]
    end

    subgraph GatewayLayer ["API and Ingestion Gateway"]
        APIGateway["Cloudflare CDN and API Gateway"]
        VoiceGateway["Twilio + Deepgram Audio Stream"]
        ReviewWebhook["Review Ingestion Webhook"]
    end

    subgraph CoreServices ["Cynbit Scalable Microservices"]
        BookingAPI["FastAPI Booking and Calendar Engine"]
        ReputationEngine["Revio Sentiment and Crisis Service"]
        VoiceAgent["Autonomous Healthcare Voice Agent"]
    end

    subgraph StorageLayer ["Persistent and Vector Storage"]
        Postgres[("PostgreSQL RDS - Patient Records")]
        QdrantDB[("Qdrant Vector Store - Clinical FAQs")]
        RedisCache[("Redis Cache and Task Queue")]
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
    subgraph Users ["User Portals"]
        Landlord["Property Manager Dashboard"]
        Tenant["Tenant Self-Service Portal"]
    end

    subgraph Ingestion ["Ingestion and Processing"]
        API["FastAPI Gateway"]
        DocAI["Document OCR and Lease Extraction Engine"]
        MsgQueue["Celery + Redis Worker Queue"]
    end

    subgraph BusinessLogic ["Core Application Logic"]
        RentEngine["Automated Rent and Billing Engine"]
        LeaseEngine["Lease and KYC Verification Service"]
        WhatsAppBot["Automated WhatsApp Rent Chaser"]
    end

    subgraph Data ["Storage Layer"]
        DB[("PostgreSQL Primary DB")]
        S3Vault[("AWS S3 Encrypted Lease Docs")]
        Cache[("Redis Payment Cache")]
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

        elif domain == "E-Commerce & Digital Commerce":
            project_title = f"{client_name} High-Performance Headless E-Commerce & AI Shopping Platform"
            reference_pattern = "Cynbit High-Scale Headless Commerce Architecture"
            fe_tech = ["Next.js 15 (Storefront App Router)", "TailwindCSS", "Framer Motion", "PWA Support"]
            be_tech = ["Headless WordPress / WooCommerce CMS API", "Python FastAPI (Middleware & Inventory)", "Redis Caching"]
            ai_tech = ["AI Conversational Shopping Assistant", "Semantic Product Recommendation Engine (Qdrant)"]
            db_tech = ["PostgreSQL 16 (Orders & Customers)", "MySQL (WordPress CMS)", "Redis (Cart & Session)"]
            cloud_tech = ["AWS CloudFront CDN", "AWS ECS Fargate (API)", "AWS RDS", "Razorpay / Stripe Gateway"]
            base_weeks = 6
            base_hours = 270

            mermaid_code = """graph TD
    subgraph CustomerTouchpoints ["Customer Experience"]
        Browser["Modern Next.js 15 Storefront"]
        MobilePWA["Mobile Progressive Web App"]
        AIChat["AI Product Recommendation Chat"]
    end

    subgraph GatewayLayer ["Edge and Security Layer"]
        CloudFront["AWS CloudFront Edge CDN"]
        RateLimiter["FastAPI API Gateway and JWT Auth"]
    end

    subgraph ServiceMesh ["Decoupled Backend Services"]
        WPCMS["Headless WordPress and WooCommerce Core"]
        InventoryAPI["FastAPI Inventory and Order Microservice"]
        AIAgent["Conversational Shopping and Stylist Bot"]
        PaymentGateway["Razorpay / Stripe Webhook Listener"]
    end

    subgraph DataTier ["Scalable Storage and Cache"]
        Postgres[("PostgreSQL Orders and Customer DB")]
        RedisCache[("Redis Distributed Cart Cache")]
        VectorDB[("Qdrant Product Embeddings Store")]
    end

    Browser --> CloudFront
    MobilePWA --> CloudFront
    CloudFront --> RateLimiter

    RateLimiter --> WPCMS
    RateLimiter --> InventoryAPI
    RateLimiter --> AIAgent
    RateLimiter --> PaymentGateway

    AIAgent --> VectorDB
    InventoryAPI --> Postgres
    InventoryAPI --> RedisCache
    PaymentGateway --> Postgres"""

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
    subgraph InboundDocs ["Inbound Multichannel Ingestion"]
        CarrierEmail["Carrier Emails and PDF Attachments"]
        VendorPortal["Vendor Web Upload - Next.js"]
        FTPStream["Legacy SFTP Stream"]
    end

    subgraph Pipeline ["Cognitive Extraction Pipeline"]
        IngestService["Go Ingestion Worker"]
        DocProcessor["Multi-Modal LayoutLM + LLM OCR"]
        AnomalyDetector["Anomaly and Duplicate Detection Agent"]
    end

    subgraph Matching ["3-Way Matching and ERP Integration"]
        SAPBridge["SAP ERP Connector - RFC/REST"]
        ExceptionUI["Human-in-the-Loop Review Dashboard"]
    end

    subgraph Storage ["Enterprise Storage and Audit"]
        DocStore[("AWS S3 Versioned Document Store")]
        Postgres[("PostgreSQL Audit and Extraction Ledger")]
        VectorDB[("Qdrant Vector Index")]
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
    subgraph StudentUI ["Student Learning Environment"]
        CodeIDE["Monaco Code Editor and Terminal UI"]
        InterviewBot["AI Mock Interview Companion"]
        RadarView["Skill Radar and Progress Dashboard"]
    end

    subgraph SecurityGate ["Security and Execution Gateway"]
        Gateway["FastAPI Security and Auth Gateway"]
        SandboxDaemon["Isolated Docker Execution Sandbox"]
    end

    subgraph EvaluationCore ["Intelligent Evaluation Engine"]
        OutputVerifier["Unit Test and Edge Case Verifier"]
        LLMReviewer["Semantic Code Quality and Complexity Reviewer"]
        SkillEngine["Adaptive XP and Skill Graph Calculator"]
    end

    subgraph Persistence ["State and Analytics"]
        UserDB[("PostgreSQL Student Profiles")]
        LeaderboardCache[("Redis Cache and Live Leaderboard")]
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
            project_title = f"{client_name} Enterprise Custom Software & AI System"
            reference_pattern = "Cynbit Autonomous Agent Suite"
            fe_tech = ["Next.js 14 App Router", "React 19", "TailwindCSS", "TypeScript"]
            be_tech = ["Python (FastAPI)", "Redis Queues", "Async Worker Cluster"]
            ai_tech = ["LangGraph Multi-Agent Engine", "OpenAI GPT-4o / Gemini 1.5", "RAG Pipeline"]
            db_tech = ["PostgreSQL 16", "Qdrant Vector Database", "Redis Cache"]
            cloud_tech = ["AWS ECS Fargate", "AWS S3", "Docker", "GitHub Actions"]
            base_weeks = 8
            base_hours = 360

            mermaid_code = """graph TD
    subgraph ClientTier ["Frontend Presentation"]
        WebUI["Next.js 14 Modern Web Dashboard"]
        MobileWeb["Responsive Mobile App"]
    end

    subgraph ServiceTier ["Cynbit Backend Services"]
        Gateway["API Gateway and Rate Limiter"]
        CoreEngine["FastAPI Business Logic"]
        AgentCluster["Autonomous AI Agent Cluster"]
    end

    subgraph DataTier ["Storage and Caching"]
        Postgres[("PostgreSQL Primary Store")]
        VectorStore[("Qdrant Vector DB")]
        Redis[("Redis Cache")]
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
        total_hours = total_weeks * 45
        
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
                    "Setup GitHub CI/CD pipelines and AWS cloud environments",
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

        team_members = [
            {"role": "Principal Solutions Architect", "fte": "0.25 FTE", "tasks": "System architecture, security design, milestone reviews"},
            {"role": "Senior AI / ML Engineer", "fte": "1.00 FTE", "tasks": "Agentic workflows, prompt tuning, vector search, LLM integrations"},
            {"role": "Senior Full-Stack Engineer", "fte": "2.00 FTE", "tasks": "Next.js UI, FastAPI endpoints, database performance, caching"},
            {"role": "QA & Cloud DevOps Engineer", "fte": "0.50 FTE", "tasks": "Docker orchestration, CI/CD pipelines, load testing, security"}
        ]

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

        executive_summary = (
            f"{client_name} operates in the {domain} sector with an opportunity to modernize its operations "
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

        sprint_md = ""
        for s in sprints_list:
            sprint_md += f"### Sprint {s.sprint_number}: {s.title} ({s.weeks})\n"
            for m in s.milestones:
                sprint_md += f"- [ ] {m}\n"
            sprint_md += "\n"

        stack_md = ""
        for cat, items in tech_stack.items():
            stack_md += f"- **{cat}:** {', '.join(items)}\n"

        team_md = ""
        for tm in team_members:
            team_md += f"- **{tm['role']} ({tm['fte']}):** {tm['tasks']}\n"

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
            full_markdown_proposal=full_proposal,
            generated_by="Cynbit Blueprint Engine (Rule Mode)"
        )
