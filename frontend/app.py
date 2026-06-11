# frontend/app.py

import os
import sys

# ─────────────────────────────────────────────
# PROJECT ROOT PATH — must come first so that
# all project-relative imports resolve correctly
# regardless of which directory Streamlit is
# launched from.
# ─────────────────────────────────────────────
sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# ─────────────────────────────────────────────
# STDLIB / THIRD-PARTY
# ─────────────────────────────────────────────
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# PROJECT IMPORTS  (safe now that path is set)
# ─────────────────────────────────────────────
from services.adk_runner import run_agent_sync
from auth.firebase_auth import ClinicalAuth
from agents.orchestrator import orchestrator_agent

# ─────────────────────────────────────────────
# ENV
# ─────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────
# STREAMLIT CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ClinicalOps AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
auth = ClinicalAuth()

if "user" not in st.session_state:
    st.session_state.user = None


# ─────────────────────────────────────────────
# AGENT EXECUTION
# ─────────────────────────────────────────────
def run_agent_query(agent, message: str) -> str:
    """Execute ADK agents on the persistent event loop (MCP stays alive)."""

    user_id = st.session_state.user.get("uid", "anonymous")

    session_id = (
        f"{user_id}_"
        f"{datetime.now().strftime('%H%M%S')}_"
        f"{id(agent)}"
    )

    return run_agent_sync(user_id, session_id, message, timeout=300)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔐 ClinicalOps AI")

    if not st.session_state.user:
        st.subheader("Login")

        token = st.text_input(
            "Firebase ID Token",
            type="password",
            value="demo_token",
        )

        if st.button("Sign In", type="primary", use_container_width=True):
            try:
                claims = auth.verify_token(token)
                st.session_state.user = {
                    "uid": claims.get("sub", "demo_user"),
                    "role": auth.get_user_role(claims),
                    "email": claims.get("email", "demo@clinicalops.local"),
                }
                st.success(f"Welcome {st.session_state.user['role']}")
                st.rerun()
            except Exception as e:
                st.error(f"Authentication failed: {e}")

    else:
        st.success(f"👤 {st.session_state.user['uid']}")
        st.caption(f"Role: {st.session_state.user['role']}")

        if st.button("Sign Out", use_container_width=True):
            st.session_state.user = None
            st.rerun()

        st.divider()
        st.caption("System Status")
        st.success("🟢 ADK Running")
        st.success("🟢 Orchestrator Active")
        st.success("🟢 MongoDB Connected")
        st.success("🟢 Vertex AI Enabled")


# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────
st.title("🏥 Clinical Operations Dashboard")

if not st.session_state.user:
    st.warning("Please sign in.")
    st.stop()


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(
    [
        "🟢 Eligibility Screening",
        "🟠 Adverse Event Triage",
        "🔵 Regulatory Draft",
    ]
)

# ── TAB 1 ─────────────────────────────────────
with tab1:
    st.header("Patient-Trial Eligibility Screening")

    col1, col2 = st.columns([2, 1])

    with col1:
        patient_id = st.text_input("Patient ID", "PAT-001")

        eligibility_query = st.text_area(
            "Screening Request",
            f"Screen patient {patient_id} against all active clinical trials "
            "using semantic vector matching.",
            height=140,
        )

    with col2:
        st.info(
            """
            Uses:
            - Vector Search
            - Vertex AI Embeddings
            - Semantic Matching
            """
        )

    if st.button("Run Screening", type="primary"):
        with st.spinner("🔍 Running orchestrated screening..."):
            result = run_agent_query(orchestrator_agent, eligibility_query)
            st.markdown("### 📊 Results")
            st.markdown(result)


# ── TAB 2 ─────────────────────────────────────
with tab2:
    st.header("Adverse Event Triage")

    patient_id_ae = st.text_input("Patient ID", "PAT-001", key="ae_pid")

    ae_description = st.text_area(
        "Event Description",
        "Patient developed severe rash after infusion.",
        height=140,
    )

    if st.button("Triage Event", type="primary"):
        with st.spinner("🚑 Running orchestrated AE triage..."):
            query = (
                f"Analyze and triage the following adverse event.\n\n"
                f"Patient ID: {patient_id_ae}\n\n"
                f"Event: {ae_description}\n\n"
                "Determine CTCAE grade, SAE status, and reporting obligation. "
                "Return professional markdown."
            )
            result = run_agent_query(orchestrator_agent, query)
            st.markdown("### 🚨 Triage Result")
            st.markdown(result)


# ── TAB 3 ─────────────────────────────────────
with tab3:
    st.header("ICH-Compliant Regulatory Drafting")

    document_type = st.selectbox(
        "Document Type",
        ["SAE Narrative (ICH E2A)", "ICF Summary"],
    )

    regulatory_context = st.text_area(
        "Clinical Context",
        "PAT-001, Grade 3 rash after infusion.",
        height=140,
    )

    if st.button("Generate Draft", type="primary"):
        with st.spinner("� Running orchestrated drafting..."):
            query = (
                f"Generate a professional {document_type}.\n\n"
                f"Context: {regulatory_context}\n\n"
                "Return sponsor-ready markdown."
            )
            result = run_agent_query(orchestrator_agent, query)
            st.markdown("### 📄 Generated Draft")
            st.markdown(result)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 Download Markdown",
                data=result,
                file_name=f"clinical_report_{timestamp}.md",
                mime="text/markdown",
            )


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
st.caption(
    "Powered by: Google ADK • ClinicalOps Orchestrator • "
    "MongoDB Atlas • MongoDB MCP • Vertex AI • Streamlit"
)
