"""
Cynbit AI Pre-Sales & Solution Architecture Copilot
Technical Assessment Proof of Concept for AI/ML Engineer Intern
Applicant: Sanjit Chaudhary | Company: Cynbit Technologies Pvt. Ltd., Jaipur
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

from core.kb import (
    CYNBIT_COMPANY_INFO,
    CYNBIT_STACK_CATALOG,
    PROPRIETARY_SAAS_PATTERNS,
    COMMERCIAL_METRICS
)
from core.presets import CLIENT_PRESETS
from core.pipeline import PreSalesPipeline, ArchitectureProposal

# Page Configuration
st.set_page_config(
    page_title="Cynbit AI Pre-Sales Copilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Cynbit Branding
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .cynbit-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #0F172A 50%, #090D16 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 28px 36px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }
    
    .brand-badge {
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #38BDF8;
        margin: 4px 0;
    }
    
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
    }
    
    .tech-pill {
        background: #0F172A;
        color: #E2E8F0;
        border: 1px solid #334155;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin: 4px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


def render_mermaid(code: str, height: int = 420):
    """Renders Mermaid diagram with dark theme using CDN."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'dark',
                themeVariables: {{
                    primaryColor: '#3B82F6',
                    primaryTextColor: '#F8FAFC',
                    primaryBorderColor: '#60A5FA',
                    lineColor: '#94A3B8',
                    secondaryColor: '#8B5CF6',
                    tertiaryColor: '#0EA5E9'
                }}
            }});
        </script>
        <style>
            body {{
                background-color: transparent;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }}
            .mermaid {{
                width: 100%;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
        {code}
        </div>
    </body>
    </html>
    """
    components.html(html_content, height=height, scrolling=True)


# Sidebar Configuration
with st.sidebar:
    st.image("https://cynbit.in/logo.svg", width=160)
    st.markdown("### ⚡ Pre-Sales AI Engine")
    st.caption("Engineered for Cynbit Solutions Architects")
    
    st.divider()
    
    st.markdown("#### ⚙️ Engine Settings")
    api_key_input = st.text_input(
        "LLM API Key (Optional)",
        type="password",
        help="Supports Groq (gsk_...) or OpenAI (sk-...). If left blank, the app uses Cynbit's high-fidelity Heuristic Engine."
    )
    
    if api_key_input:
        st.success("🟢 Live LLM API Connected")
    else:
        st.info("⚡ Heuristic Semantic Mode Active (100% Offline & Instant)")
        
    st.divider()
    
    st.markdown("#### 👤 Candidate Details")
    st.markdown("**Applicant:** Sanjit Chaudhary")
    st.markdown("**Role:** AI/ML Engineer Intern")
    st.markdown("**Company:** Cynbit Technologies")
    st.markdown("**Headquarters:** Jaipur, Rajasthan")
    st.markdown(f"**Website:** [cynbit.in]({CYNBIT_COMPANY_INFO['website']})")
    
    st.divider()
    st.caption("© 2026 Cynbit Technologies. Engineered for Optimism.")


# Top Banner
st.markdown("""
<div class="cynbit-header">
    <div class="brand-badge">Cynbit Technologies — Internal Pre-Sales Tool</div>
    <h1 style="color: #FFFFFF; font-size: 32px; font-weight: 800; margin: 0 0 8px 0;">
        ⚡ AI Pre-Sales & Solution Architecture Copilot
    </h1>
    <p style="color: #94A3B8; font-size: 15px; margin: 0; line-height: 1.5;">
        Transform messy, unstructured client briefs into production-ready system architecture blueprints, 
        accurate sprint milestones, and client-ready commercial proposals in seconds.
    </p>
</div>
""", unsafe_allow_html=True)


# Main Tabs
tab_demo, tab_kb, tab_report1, tab_report2 = st.tabs([
    "🚀 Copilot Interactive Demo",
    "🏛️ Cynbit Knowledge Base",
    "📄 AI Opportunity Report",
    "🛠️ Technical Approach Report"
])


# ==========================================
# TAB 1: COPILOT DEMO
# ==========================================
with tab_demo:
    col_input, col_ctrl = st.columns([7, 3])
    
    with col_input:
        st.markdown("#### 1. Client Discovery Brief")
        
        # Preset selection
        selected_preset_key = st.selectbox(
            "Select an Inbound Discovery Preset (or choose 'Custom' to write your own):",
            ["Custom (Enter your own brief)"] + list(CLIENT_PRESETS.keys())
        )
        
        if selected_preset_key != "Custom (Enter your own brief)":
            preset = CLIENT_PRESETS[selected_preset_key]
            default_client = preset["client_name"]
            default_industry = preset["industry"]
            default_brief = preset["brief"]
        else:
            default_client = "NovaHealth Diagnostics"
            default_industry = "Healthcare & Telemedicine"
            default_brief = (
                "We need an AI-driven remote patient diagnostics platform. "
                "Patients upload lab reports and radiology images via mobile web. "
                "We need an automated OCR and medical vision extraction agent, a real-time doctor consultation "
                "video room with automated meeting summaries, and a HIPAA-compliant encrypted patient record database."
            )
            
        client_name = st.text_input("Prospective Client Name:", value=default_client)
        industry_input = st.text_input("Client Industry / Domain:", value=default_industry)
        brief_input = st.text_area(
            "Unstructured Client Problem Brief & Requirements:",
            value=default_brief,
            height=180
        )
        
    with col_ctrl:
        st.markdown("#### 2. Scope & Target Parameters")
        target_weeks = st.slider("Target Delivery Timeline (Weeks):", min_value=4, max_value=16, value=8, step=2)
        budget_override = st.number_input(
            "Target Budget Override (USD, 0 for auto):",
            min_value=0,
            max_value=150000,
            value=0,
            step=2500
        )
        
        st.markdown("#### 3. Execution Trigger")
        generate_clicked = st.button("⚡ Generate Architecture & Proposal", type="primary", use_container_width=True)
        
    # Execution
    if generate_clicked:
        with st.spinner("Analyzing requirements, selecting Cynbit stack, and generating architecture..."):
            pipeline = PreSalesPipeline(api_key=api_key_input)
            b_override = budget_override if budget_override > 0 else None
            proposal: ArchitectureProposal = pipeline.analyze_and_generate(
                client_name=client_name,
                brief=brief_input,
                industry=industry_input,
                budget_override=b_override,
                timeline_weeks_override=target_weeks
            )
            st.session_state["active_proposal"] = proposal
            st.success("✅ Solution Architecture & Commercial Proposal successfully synthesized!")

    # Display Results if available
    if "active_proposal" in st.session_state:
        p: ArchitectureProposal = st.session_state["active_proposal"]
        
        st.divider()
        st.markdown(f"### 🎯 Results for: `{p.client_name}` ({p.industry})")
        
        # Key Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Timeline</div>
                <div class="metric-value">{p.total_weeks} Wks</div>
                <div class="metric-label">{p.total_weeks // 2} Sprints</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Engineering Effort</div>
                <div class="metric-value">{p.total_hours} hrs</div>
                <div class="metric-label">Cross-functional Team</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Estimated Investment</div>
                <div class="metric-value">${p.budget_usd:,}</div>
                <div class="metric-label">USD (Net of Taxes)</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">INR Equivalent</div>
                <div class="metric-value">₹{p.budget_inr:,}</div>
                <div class="metric-label">@ ₹85 / USD FX</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        
        # Sub-tabs for Proposal Details
        prop_tab1, prop_tab2, prop_tab3, prop_tab4 = st.tabs([
            "📊 System Architecture Diagram",
            "🧩 Component & Stack Breakdown",
            "📅 Sprint Breakdown (WBS)",
            "📄 Client-Ready Proposal (Markdown)"
        ])
        
        with prop_tab1:
            st.markdown("#### System Topology & Flowchart (Interactive Mermaid.js)")
            render_mermaid(p.mermaid_diagram, height=450)
            with st.expander("View Raw Mermaid Syntax"):
                st.code(p.mermaid_diagram, language="mermaid")
                
        with prop_tab2:
            st.markdown("#### Recommended Cynbit Stack & Component Mapping")
            for comp in p.components:
                with st.container():
                    c_col1, c_col2 = st.columns([3, 7])
                    with c_col1:
                        st.markdown(f"**{comp.layer}**")
                        st.caption(f"Component: `{comp.component_name}`")
                        st.markdown(f"<span class='tech-pill'>{comp.technology}</span>", unsafe_allow_html=True)
                    with c_col2:
                        st.markdown(f"**Architectural Rationale:**")
                        st.write(comp.rationale)
                    st.divider()
                    
            st.markdown("#### Technology Palette Allocation")
            for cat, items in p.tech_stack.items():
                pills = " ".join([f"<span class='tech-pill'>{i}</span>" for i in items])
                st.markdown(f"**{cat}:** {pills}", unsafe_allow_html=True)

        with prop_tab3:
            st.markdown("#### Work Breakdown Structure (2-Week Sprints)")
            for s in p.sprints:
                with st.expander(f"Sprint {s.sprint_number}: {s.title} ({s.weeks})", expanded=True):
                    for m in s.milestones:
                        st.markdown(f"- ✅ {m}")
                        
            st.markdown("#### Resource Team Allocation")
            for tm in p.team_members:
                st.markdown(f"- **{tm['role']}** ({tm['fte']}): {tm['tasks']}")
                
        with prop_tab4:
            st.markdown("#### Generated Client Proposal Document")
            st.download_button(
                label="📥 Download Proposal as Markdown (.md)",
                data=p.full_markdown_proposal,
                file_name=f"Cynbit_Proposal_{p.client_name.replace(' ', '_')}.md",
                mime="text/markdown",
                type="primary"
            )
            st.markdown(p.full_markdown_proposal)


# ==========================================
# TAB 2: CYNBIT KNOWLEDGE BASE
# ==========================================
with tab_kb:
    st.markdown("### 🏛️ Cynbit Technologies Knowledge Base")
    st.caption("Grounded in public architecture and service offerings from https://www.cynbit.in")
    
    col_kb1, col_kb2 = st.columns(2)
    with col_kb1:
        st.markdown("#### 💼 Foundational Services Hub")
        for cat, items in CYNBIT_STACK_CATALOG.items():
            with st.expander(f"Pillar: {cat}", expanded=True):
                for item in items:
                    st.markdown(f"- `{item}`")
                    
    with col_kb2:
        st.markdown("#### 🚀 Proprietary SaaS Suite & Blueprint Patterns")
        for key, saas in PROPRIETARY_SAAS_PATTERNS.items():
            with st.expander(f"Platform: {saas['title']} ({saas['category']})", expanded=True):
                st.write(saas["description"])
                st.markdown("**Reference Architecture Stack:**")
                st.write(", ".join([f"`{s}`" for s in saas["recommended_stack"]]))

        st.markdown("#### 🌟 Social & EdTech Footprint")
        st.markdown("- **BitElevate:** Unstructured learning and engineering mentorship ecosystem certifying 1000+ architects.")
        st.markdown("- **Manav Seva Trust:** Empowering rural education with computer teaching and tech-enabled community growth.")


# ==========================================
# TAB 3: DELIVERABLE 1 - AI OPPORTUNITY REPORT
# ==========================================
with tab_report1:
    report1_path = os.path.join(os.path.dirname(__file__), "docs", "AI_OPPORTUNITY_REPORT.md")
    if os.path.exists(report1_path):
        with open(report1_path, "r", encoding="utf-8") as f:
            content1 = f.read()
        st.download_button(
            label="📥 Download AI Opportunity Report (.md)",
            data=content1,
            file_name="AI_OPPORTUNITY_REPORT_CYNBIT.md",
            mime="text/markdown"
        )
        st.markdown(content1)
    else:
        st.error("AI_OPPORTUNITY_REPORT.md file not found in docs/")


# ==========================================
# TAB 4: DELIVERABLE 3 - TECHNICAL APPROACH REPORT
# ==========================================
with tab_report2:
    report2_path = os.path.join(os.path.dirname(__file__), "docs", "TECHNICAL_APPROACH.md")
    if os.path.exists(report2_path):
        with open(report2_path, "r", encoding="utf-8") as f:
            content2 = f.read()
        st.download_button(
            label="📥 Download Technical Approach Report (.md)",
            data=content2,
            file_name="TECHNICAL_APPROACH_CYNBIT.md",
            mime="text/markdown"
        )
        st.markdown(content2)
    else:
        st.error("TECHNICAL_APPROACH.md file not found in docs/")


# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 13px; padding: 20px 0;">
    <b>Applicant / Submission:</b> Sanjit Chaudhary &bull; 
    <b>Position:</b> AI/ML Engineer Intern &bull; 
    <b>Target Company:</b> Cynbit Technologies Pvt. Ltd., Jaipur &bull; 
    <b>Submission Window:</b> October 2026
</div>
""", unsafe_allow_html=True)
