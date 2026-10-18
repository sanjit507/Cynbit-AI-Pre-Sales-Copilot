"""
Cynbit Knowledge Base & Architecture Standards
Grounded in https://www.cynbit.in verified capabilities.
"""
from typing import Dict, List, Any

CYNBIT_COMPANY_INFO = {
    "name": "Cynbit Technologies Pvt. Ltd.",
    "brand_motto": "The Optimistic Architect — Architecting the Future with AI Automation & Software Solutions",
    "location": "32/115 Pratap Nagar, Jaipur, Rajasthan, 302033, India",
    "website": "https://www.cynbit.in",
    "contact_email": "opportunities@cynbit.in",
    "phones": ["+91 89479 62667", "+91 78912 09777", "+91 83023 37367"],
}

CYNBIT_STACK_CATALOG: Dict[str, List[str]] = {
    "Frontend": [
        "Next.js 14/15 (App Router, Server Actions)",
        "React 19 & TypeScript",
        "TailwindCSS & Framer Motion",
        "Flutter (Cross-Platform Mobile iOS/Android)",
        "Shadcn/UI & Material Symbols"
    ],
    "Backend & APIs": [
        "Python (FastAPI, Asyncio, Pydantic)",
        "Go / Golang (High-Throughput Microservices)",
        "Rust (Low-Latency Native Compute)",
        "Node.js / NestJS (Enterprise Modular Backends)",
        "gRPC & GraphQL for Inter-service RPC"
    ],
    "AI / ML & Autonomous Agents": [
        "Autonomous Agent Frameworks (LangGraph, CrewAI)",
        "RAG Architectures (LlamaIndex, Hybrid BM25 + Dense Search)",
        "Foundation Models (OpenAI GPT-4o, Anthropic Claude 3.5, Google Gemini)",
        "Open-Weights LLMs (Llama 3.3 70B via vLLM / Groq)",
        "AI Voice & Speech (Whisper, ElevenLabs, Deepgram)",
        "Document AI & Vision (Tesseract OCR, LayoutLM, Multi-modal LLMs)"
    ],
    "Databases & Vector Stores": [
        "PostgreSQL 16 (Supabase, Neon, AWS RDS Aurora)",
        "Qdrant / Pinecone (HNSW Vector Indexing for RAG)",
        "Redis (Distributed Caching, Pub/Sub, Session Store)",
        "MongoDB (Document Storage & Dynamic Schemas)"
    ],
    "Cloud, DevOps & Security": [
        "AWS (ECS Fargate, Lambda, S3, CloudFront, Cognito)",
        "Microsoft Azure (Azure OpenAI Service, AKS, Blob)",
        "Docker Containerization & Kubernetes Orchestration",
        "Zero-Trust Architecture & OAuth2 / OpenID Connect",
        "CI/CD via GitHub Actions & Terraform (IaC)"
    ]
}

PROPRIETARY_SAAS_PATTERNS = {
    "cynbit_studio": {
        "title": "Cynbit Studio Pattern",
        "category": "EdTech & Code Evaluation",
        "description": "Adaptive learning paths, sandboxed code execution, AI code reviewer, gamified XP, and skill radar verification.",
        "recommended_stack": ["Next.js", "FastAPI", "Docker Sandboxes", "PostgreSQL", "Gemini 1.5 Pro", "Redis"]
    },
    "tenantease": {
        "title": "TenantEase Pattern",
        "category": "PropTech & Property Management",
        "description": "Multi-property unit tracking, automated WhatsApp/SMS rent chasing, KYC document vetting, and rent collection analytics.",
        "recommended_stack": ["Next.js", "FastAPI", "PostgreSQL", "Redis", "Document OCR", "AWS S3"]
    },
    "revio": {
        "title": "Revio Pattern",
        "category": "Reputation & Sentiment Intelligence",
        "description": "Multi-location Google/Meta review sync, aspect-based sentiment scoring, crisis detection, and automated AI responses.",
        "recommended_stack": ["Next.js", "Python FastAPI", "Celery / Redis", "Qdrant", "PostgreSQL", "Llama 3.3"]
    }
}

COMMERCIAL_METRICS = {
    "blended_hourly_rate_usd": 45,
    "inr_fx_rate": 85,
    "sprint_length_weeks": 2,
    "team_roles": {
        "solutions_architect": {"title": "Principal Solutions Architect", "fte": 0.25},
        "ai_engineer": {"title": "Senior AI/ML Engineer", "fte": 1.0},
        "fullstack_engineer": {"title": "Senior Full-Stack Engineer", "fte": 2.0},
        "qa_devops": {"title": "DevOps & QA Engineer", "fte": 0.5}
    }
}
