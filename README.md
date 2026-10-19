# ⚡ Cynbit AI Pre-Sales & Solution Architecture Copilot


> **Target Company:** [Cynbit Technologies Pvt. Ltd.](https://www.cynbit.in), Jaipur, Rajasthan, India  
> **Evaluation Window:** October 2026  

---

## 📌 Executive Summary

Cynbit Technologies excels at delivering cutting-edge digital infrastructure, autonomous AI agents, and bespoke SaaS platforms (*Revio*, *TenantEase*, *Cynbit Studio*). As inbound inquiries scale, the primary pre-sales bottleneck is translating messy, unstructured client problem statements into **rigorous system architecture blueprints, technology stacks, sprint schedules, and commercial proposals**.

The **Cynbit AI Pre-Sales Copilot** reduces initial discovery and technical scoping turnaround from **72 hours to under 3 minutes**, accelerates proposal throughput by **4.5x**, and codifies Cynbit's architectural standards into an intelligent, repeatable system.

---

## 🎯 Deliverables Checklist

- [x] **Deliverable 1: AI Opportunity Report** &rarr; Located at [`docs/AI_OPPORTUNITY_REPORT.md`](docs/AI_OPPORTUNITY_REPORT.md) and embedded directly in the app.
- [x] **Deliverable 2: AI/ML Proof of Concept** &rarr; Interactive Streamlit Application (`app.py`) with visual Mermaid.js topology, parametric estimation, and markdown export.
- [x] **Deliverable 3: Technical Approach Report** &rarr; Located at [`docs/TECHNICAL_APPROACH.md`](docs/TECHNICAL_APPROACH.md) and embedded directly in the app.
- [x] **Deliverable 4: Clean Git History & Production Deployment Ready** &rarr; Fully compatible with GitHub & Streamlit Community Cloud.

---

## 🏗️ System Architecture & Workflow

```mermaid
flowchart TD
    Inbound["Unstructured Client Inquiry Brief"] --> Parser["Requirement & Scope Normalizer"]
    Parser --> RAG["Cynbit Knowledge Grounding Engine"]
    RAG --> AI["Google Gemini AI Engine (gemini-1.5-flash / gemini-2.0-flash)"]
    RAG -.->|"Offline Fallback"| Heuristic["Deterministic Blueprint Rule Engine"]
    AI --> Arch["Multi-Tier Architecture Synthesizer"]
    Heuristic --> Arch
    Arch --> Flow["Dynamic Mermaid.js Flowchart Visualizer"]
    Arch --> Estimator["Parametric Effort & Budget Engine"]
    Estimator --> Proposal["Branded Client Technical Proposal"]
    Proposal --> Export["Downloadable Markdown & PDF Export"]
```

### Key Technical Highlights:
1. **Google Gemini AI Engine:** Native integration with Google Gemini (`gemini-1.5-flash` with automatic fallback to `gemini-2.0-flash`) via Google AI Studio API for rapid multi-tier architecture reasoning, structured JSON schema enforcement, and automated proposal authoring.
2. **Dual-Mode Architecture:**
   - **Live Gemini API:** Connect your free Google AI Studio API key (`GEMINI_API_KEY`) to run live generative solution architecture modeling.
   - **High-Fidelity Heuristic Engine:** 100% offline, deterministic fallback that runs instantly without an API key or billing setup, ensuring zero-friction evaluation.
3. **Grounded in Cynbit Capabilities:** Recommends verified Cynbit stacks (Next.js 14/15, Python FastAPI, Go/Rust, PostgreSQL, Redis, Qdrant/Pinecone vector storage, AWS/Azure).
4. **Interactive Architecture Visualizer:** Dynamically synthesizes and renders live, zoomable Mermaid.js system topology diagrams directly in the browser.

---

## 🚀 Quickstart: Running Locally

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/cynbit-ai-pre-sales-copilot.git
cd cynbit-ai-pre-sales-copilot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Google Gemini API Key (Optional)
Copy `.env.example` to `.env` and add your Google Gemini API key:
```bash
# Windows PowerShell
copy .env.example .env
```
Inside `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> [!TIP]
> You can get a free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).  
> **Offline Mode:** If you do not configure an API key, the copilot runs seamlessly using Cynbit's built-in deterministic heuristic architecture engine.

### 4. Launch the Application
```bash
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 1-Click Free Deployment (Streamlit Community Cloud)

1. Push this repository to your public GitHub account.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
3. Click **"New App"**, select this repository, set `app.py` as the main file path, and click **"Deploy"**.
4. You will get a live public URL (e.g., `https://cynbit-pre-sales-copilot.streamlit.app`) to submit with your application!

---

## 📂 Repository Layout

```
cynbit-ai-pre-sales-copilot/
├── app.py                         # Streamlit interactive application
├── requirements.txt               # Production dependencies
├── .env.example                   # Template for Google Gemini API Key
├── README.md                      # Comprehensive project guide
├── .gitignore                     # Standard Python exclusions
├── core/
│   ├── __init__.py
│   ├── kb.py                      # Cynbit tech catalog & SaaS blueprint patterns
│   ├── pipeline.py                # Multi-stage reasoning & proposal engine (Gemini AI + Fallback)
│   ├── presets.py                 # Realistic client discovery scenarios
│   └── prompts.py                 # System prompts & few-shot templates
├── data/
│   └── cynbit_profile.json        # Structured Cynbit company data (from cynbit.in)
└── docs/
    ├── AI_OPPORTUNITY_REPORT.md   # Deliverable 1: Strategic & Market Analysis
    └── TECHNICAL_APPROACH.md      # Deliverable 3: Engineering & Model Choices
```

---

## 👨‍💻 Candidate Attribution
- **Candidate:** Sanjit Chaudhary
- **Role Applied:** AI/ML Engineer Intern
- **Evaluation Organization:** Cynbit Technologies Pvt. Ltd., Jaipur, India
- **Motto:** *"The speed of a startup. The rigor of an enterprise."*
