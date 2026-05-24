import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Architect - AI System Design Engine",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23666cc'/><path d='M30 70 L50 20 L70 70Z' fill='none' stroke='white' stroke-width='6' stroke-linejoin='round'/><line x1='25' y1='75' x2='75' y2='75' stroke='white' stroke-width='5' stroke-linecap='round'/></svg>",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #111118 50%, #0d0d14 100%);
    }

    .main > .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    .header-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.25rem;
    }
    .header-icon {
        width: 36px;
        height: 36px;
        flex-shrink: 0;
    }
    .header-icon svg { width: 100%; height: 100%; }
    .header-title {
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #f0f0f5 0%, #8888cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #6666aa;
        font-size: 0.95rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    .stTextArea textarea {
        background-color: #12121e !important;
        color: #e0e0f0 !important;
        border: 1px solid #2a2a45 !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
        transition: border-color 0.2s;
    }
    .stTextArea textarea:focus {
        border-color: #5555cc !important;
        box-shadow: 0 0 0 3px rgba(85, 85, 204, 0.15) !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #4444aa 0%, #6666cc 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.625rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(68, 68, 170, 0.3) !important;
    }
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 30px rgba(68, 68, 170, 0.45) !important;
        background: linear-gradient(135deg, #5555bb 0%, #7777dd 100%) !important;
    }
    .stButton button:active { transform: translateY(0) !important; }
    .stButton button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    .agent-section {
        background: #12121e;
        border-radius: 12px;
        margin: 1.5rem 0;
        overflow: hidden;
    }

    .agent-section .bar {
        height: 3px;
    }
    .agent-section .bar.purple { background: #6666cc; }
    .agent-section .bar.blue  { background: #4499dd; }
    .agent-section .bar.green { background: #44bb88; }

    .agent-section .head {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #1e1e35;
    }
    .agent-section .head .label {
        font-weight: 700;
        font-size: 0.95rem;
        color: #e0e0f0;
        letter-spacing: -0.01em;
    }
    .agent-section .head .sub {
        color: #6666aa;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .agent-section .head .tag {
        margin-left: auto;
        background: #1a1a2e;
        color: #8888bb;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid #2a2a45;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .agent-section .body {
        padding: 1.5rem;
    }
    .agent-section hr {
        border-color: #2a2a45;
        margin: 1.5rem 0;
    }
    .agent-section h3 {
        color: #9999dd !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
    }
    .agent-section h4 {
        color: #bbbbee !important;
        font-weight: 600 !important;
    }
    .agent-section strong { color: #ccccee; }
    .agent-section p {
        color: #c0c0d0;
        line-height: 1.7;
    }
    .agent-section li {
        color: #b0b0c8;
        line-height: 1.7;
    }
    .agent-section code {
        background: #1a1a2e;
        color: #aaaaff;
        padding: 0.15em 0.4em;
        border-radius: 4px;
        font-size: 0.85em;
    }
    .agent-section pre {
        background: #0e0e1a !important;
        border: 1px solid #2a2a45;
        border-radius: 8px;
        padding: 1rem !important;
        overflow-x: auto;
        font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'SF Mono', 'Menlo', 'Consolas', monospace !important;
        font-size: 0.8rem !important;
        line-height: 1.35 !important;
        white-space: pre !important;
        tab-size: 2;
    }
    .agent-section pre code {
        background: none;
        padding: 0;
        font-family: inherit !important;
        font-size: inherit !important;
    }
    .agent-section table {
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
    }
    .agent-section th {
        background: #1a1a2e;
        color: #9999dd;
        font-weight: 600;
        padding: 0.625rem 1rem;
        border: 1px solid #2a2a45;
        text-align: left;
    }
    .agent-section td {
        color: #c0c0d0;
        padding: 0.5rem 1rem;
        border: 1px solid #2a2a45;
    }

    .footer {
        text-align: center;
        color: #3a3a5a;
        font-size: 0.75rem;
        padding: 3rem 0 1rem 0;
        letter-spacing: 0.03em;
    }

    section[data-testid="stSidebar"] {
        background: #0e0e16;
        border-right: 1px solid #1e1e35;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #8888cc;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    section[data-testid="stSidebar"] p, li {
        color: #8888aa;
        font-size: 0.85rem;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #2a2a45;
        margin: 1.5rem 0;
    }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .sidebar-logo svg {
        width: 28px;
        height: 28px;
        flex-shrink: 0;
    }
    .sidebar-logo span {
        font-weight: 700;
        font-size: 1.1rem;
        color: #e0e0f0;
        letter-spacing: -0.01em;
    }

    .pipe-card {
        background: #12121e;
        border: 1px solid #2a2a45;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .pipe-card .num {
        width: 22px;
        height: 22px;
        border-radius: 6px;
        background: #1a1a2e;
        border: 1px solid #2a2a45;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: #6666cc;
        flex-shrink: 0;
    }
    .pipe-card .info .name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #d0d0e8;
    }
    .pipe-card .info .desc {
        font-size: 0.7rem;
        color: #6666aa;
        margin-top: 1px;
    }

    .stack-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0;
    }
    .stack-row .key {
        color: #8888aa;
        font-size: 0.8rem;
        font-weight: 500;
        min-width: 52px;
    }
    .stack-row .val {
        color: #c0c0d8;
        font-size: 0.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

AGENTS_META = [
    {"num": "1", "role": "Principal Tech Consultant", "short": "Consultant", "tag": "STACK", "color": "purple",
     "desc": "Technology selection and architecture style"},
    {"num": "2", "role": "Lead Systems Architect", "short": "Architect", "tag": "DESIGN", "color": "blue",
     "desc": "Database schema, API spec, data flow"},
    {"num": "3", "role": "Senior Security Engineer", "short": "Security", "tag": "AUDIT", "color": "green",
     "desc": "Threat model, vulnerability assessment"},
]

with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo">'
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="100" height="100" rx="20" fill="#6666cc"/>'
        '<path d="M30 70 L50 20 L70 70Z" fill="none" stroke="white" stroke-width="6" stroke-linejoin="round"/>'
        '<line x1="25" y1="75" x2="75" y2="75" stroke="white" stroke-width="5" stroke-linecap="round"/>'
        '</svg><span>Architect v1.0</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color: #6666aa; font-size: 0.8rem; margin: 0 0 1.5rem 0;">'
        'Multi-agent system design engine</p>',
        unsafe_allow_html=True,
    )

    st.markdown("### Pipeline")
    for a in AGENTS_META:
        st.markdown(
            f'<div class="pipe-card">'
            f'<div class="num">{a["num"]}</div>'
            f'<div class="info"><div class="name">{a["short"]}</div><div class="desc">{a["desc"]}</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Stack")
    st.markdown(
        '<div class="stack-row"><span class="key">LLM</span><span class="val">Llama 3.3 70B</span></div>'
        '<div class="stack-row"><span class="key">Host</span><span class="val">Groq Cloud</span></div>'
        '<div class="stack-row"><span class="key">Orch</span><span class="val">CrewAI</span></div>'
        '<div class="stack-row"><span class="key">API</span><span class="val">FastAPI</span></div>'
        '<div class="stack-row"><span class="key">UI</span><span class="val">Streamlit</span></div>',
        unsafe_allow_html=True,
    )

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(
        '<div class="header-row">'
        '<div class="header-icon">'
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        '<rect width="100" height="100" rx="20" fill="#6666cc"/>'
        '<path d="M30 70 L50 20 L70 70Z" fill="none" stroke="white" stroke-width="6" stroke-linejoin="round"/>'
        '<line x1="25" y1="75" x2="75" y2="75" stroke="white" stroke-width="5" stroke-linecap="round"/>'
        '</svg></div>'
        '<span class="header-title">Architect</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<p class="subtitle">Autonomous System Design Engine</p>', unsafe_allow_html=True)

with col2:
    st.markdown(
        '<div style="text-align:right; padding-top: 1.25rem;">'
        '<span style="background: #1a1a2e; color: #6666cc; padding: 0.3rem 0.75rem; '
        'border-radius: 20px; font-size: 0.75rem; font-weight: 600; border: 1px solid #2a2a45;">'
        '<svg viewBox="0 0 8 8" width="7" height="7" style="margin-right: 4px; vertical-align: middle;">'
        '<circle cx="4" cy="4" r="3" fill="#44cc88"/></svg>'
        'ONLINE</span></div>',
        unsafe_allow_html=True,
    )

project_idea = st.text_area(
    "System Objectives",
    placeholder="e.g. A micro-loan platform for medical professionals to finance equipment purchases...",
    height=140,
)

col_a, col_b, col_c = st.columns([2, 1, 2])
with col_b:
    generate = st.button("Generate Blueprint", use_container_width=True, type="primary")

if generate:
    if not project_idea:
        st.warning("Please describe your system requirements first.")
    else:
        placeholder = st.empty()

        with placeholder.container():
            st.markdown(
                '<div class="status-box">'
                '<div class="agent"><span class="dot active"></span> Principal Tech Consultant - selecting technology stack...</div>'
                '<div class="agent"><span class="dot"></span> Lead Systems Architect - designing schema and API...</div>'
                '<div class="agent"><span class="dot"></span> Senior Security Engineer - auditing for vulnerabilities...</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        try:
            start = time.time()
            response = requests.get(
                f"http://localhost:8000/build?project_idea={project_idea}",
                timeout=120,
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                data = response.json()
                placeholder.empty()

                st.markdown(
                    f'<div style="display:flex; justify-content:space-between; align-items:center; margin: 0.5rem 0 1.5rem 0;">'
                    f'<span style="color: #44cc88; font-size: 0.85rem; font-weight: 600;">'
                    f'<svg viewBox="0 0 16 16" width="14" height="14" style="margin-right: 4px; vertical-align: middle;">'
                    f'<path d="M13.5 4.5L6 12L2.5 8.5" fill="none" stroke="#44cc88" stroke-width="2" '
                    f'stroke-linecap="round" stroke-linejoin="round"/></svg>'
                    f'Blueprint generated in {elapsed:.1f}s</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                for i, agent_out in enumerate(data["agents_output"]):
                    meta = AGENTS_META[i]
                    st.markdown(
                        f'<div class="agent-section">'
                        f'<div class="bar {meta["color"]}"></div>'
                        f'<div class="head">'
                        f'<div class="label">{meta["role"]}</div>'
                        f'<div class="sub">Agent {meta["num"]} of 3</div>'
                        f'<div class="tag">{meta["tag"]}</div>'
                        f'</div>'
                        f'<div class="body">'
                        f'{agent_out["output"]}'
                        f'</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                placeholder.empty()
                st.error(f"Backend returned status {response.status_code}")

        except requests.exceptions.ConnectionError:
            placeholder.empty()
            st.error("Could not connect to the backend. Make sure `uvicorn main:app` is running on port 8000.")
        except requests.exceptions.Timeout:
            placeholder.empty()
            st.error("Request timed out. The LLM agents may be taking too long.")
        except Exception as e:
            placeholder.empty()
            st.error(f"Unexpected error: {e}")

st.markdown('<div class="footer">Architect Engine &middot; Powered by CrewAI + Groq</div>', unsafe_allow_html=True)
