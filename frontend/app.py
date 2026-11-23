"""
=============================================================================
NEXOR - AI-Powered Document Intelligence Platform
Modern Motivo-Inspired Enterprise UI
=============================================================================
"""

import sys
from pathlib import Path
from datetime import datetime

# Ensure frontend root is in sys.path
FRONTEND_DIR = Path(__file__).resolve().parent
if str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))

import streamlit as st
from api import (
    check_backend,
    get_documents,
    get_document_id,
    get_document_name,
    upload_and_index,
    delete_document_api,
    ask_question,
    format_file_size,
    BACKEND_URL
)
from styles import get_css


# =========================================================
# APPLICATION SETUP
# =========================================================

st.set_page_config(
    page_title="NEXOR | Document Intelligence",
    page_icon="✳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Motivo Design System
st.markdown(get_css(), unsafe_allow_html=True)


# =========================================================
# SESSION STATE MANAGEMENT
# =========================================================

if "upload_results" not in st.session_state:
    st.session_state.upload_results = []

if "last_query_result" not in st.session_state:
    st.session_state.last_query_result = None

if "delete_success_message" not in st.session_state:
    st.session_state.delete_success_message = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "main_nav_radio" not in st.session_state:
    st.session_state.main_nav_radio = "Home / Overview"

if "target_chat_doc_id" not in st.session_state:
    st.session_state.target_chat_doc_id = None


def set_nav(page_name: str, target_doc_id=None):
    """Reliably navigate to any page via on_click callback before widgets instantiate."""
    st.session_state["main_nav_radio"] = page_name
    if target_doc_id is not None:
        st.session_state["target_chat_doc_id"] = target_doc_id


# =========================================================
# DATA FETCHING
# =========================================================

backend_info = check_backend()
documents = get_documents()

total_docs = len(documents)
indexed_docs = sum(1 for d in documents if d.get("status") == "processed")
coverage_pct = f"{(indexed_docs / total_docs * 100):.0f}%" if total_docs > 0 else "0%"


# =========================================================
# SIDEBAR (MOTIVO PRISTINE NAVIGATION)
# =========================================================

with st.sidebar:
    # Motivo Brand Logo
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem; padding-top: 0.25rem;">
            <div style="
                background: #E8F5F1;
                color: #0D7B70;
                width: 38px;
                height: 38px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.3rem;
                font-weight: 800;
                border: 1px solid #C4EADF;
            ">✳</div>
            <div>
                <div style="font-size: 1.3rem; font-weight: 800; color: #11181C; letter-spacing: -0.03em; line-height: 1;">nexor.</div>
                <div style="font-size: 0.72rem; color: #5F7377; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;">Document Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr style='margin: 1rem 0; border-color: #E4ECE9;'>", unsafe_allow_html=True)

    # Navigation menu
    nav_options = [
        "Home / Overview",
        "Documents Hub",
        "AI Chat Assistant"
    ]

    selected_nav = st.radio(
        "Navigation",
        nav_options,
        key="main_nav_radio",
        label_visibility="collapsed"
    )

    if "Home" in selected_nav:
        current_page = "Dashboard"
    elif "Documents" in selected_nav:
        current_page = "Documents"
    else:
        current_page = "AI Assistant"

    st.markdown("<hr style='margin: 1.25rem 0; border-color: #E4ECE9;'>", unsafe_allow_html=True)

    # Live Health Monitor Badge
    if backend_info["online"]:
        st.markdown(
            f"""
            <div style="
                background: #E8F5F1;
                border: 1px solid #C4EADF;
                border-radius: 12px;
                padding: 10px 12px;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center;">
                        <span class="pulse-dot-green"></span>
                        <span style="font-size: 0.82rem; font-weight: 700; color: #0D7B70;">System Online</span>
                    </div>
                    <span style="font-size: 0.72rem; color: #5F7377; font-family: var(--font-mono); font-weight: 600;">{backend_info['latency_ms']}ms</span>
                </div>
                <div style="font-size: 0.72rem; color: #5F7377; margin-top: 4px; font-family: var(--font-mono); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    {BACKEND_URL}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
                background: #FFF1F2;
                border: 1px solid #FECDD3;
                border-radius: 12px;
                padding: 10px 12px;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; align-items: center;">
                    <span class="pulse-dot-red"></span>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #BE123C;">Backend Offline</span>
                </div>
                <div style="font-size: 0.72rem; color: #5F7377; margin-top: 4px;">
                    Ensure FastAPI is running on port 8000
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Sidebar Storage Overview
    st.markdown(
        f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E4ECE9;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 1px 3px rgba(17, 24, 28, 0.04);
        ">
            <div style="font-size: 0.72rem; color: #5F7377; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">Workspace Index</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="font-size: 0.82rem; color: #5F7377;">Total Files</span>
                <span style="font-size: 0.85rem; font-weight: 700; color: #11181C;">{total_docs}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="font-size: 0.82rem; color: #5F7377;">FAISS Vectors</span>
                <span style="font-size: 0.85rem; font-weight: 700; color: #0D7B70;">{indexed_docs}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PAGE 1: MOTIVO-INSPIRED DASHBOARD
# =========================================================

if current_page == "Dashboard":

    # Hero Headline & Serendipitous Serif Italic Accent
    h_col1, h_col2 = st.columns([3, 1.2])

    with h_col1:
        st.markdown(
            """
            <div class="motivo-pill-badge" style="margin-top: 0.25rem;">
                <span class="badge-tag">NEW</span>
                <span>Neural RAG Engine now active</span>
                <span style="font-weight: 800;">&rarr;</span>
            </div>
            <h1 class="motivo-headline">
                Analyze smarter, together.<br>
                <span class="serif-italic">Achieve more.</span>
            </h1>
            <p class="motivo-subheadline">
                NEXOR is the intelligent document workspace that extracts, indexes,
                and retrieves deep contextual answers across your technical guides, contracts, and reports.
            </p>
            """,
            unsafe_allow_html=True
        )

        btn_c1, btn_c2, _ = st.columns([1.3, 1.3, 1.4])
        with btn_c1:
            st.button(
                "Upload Documents &rarr;",
                type="primary",
                use_container_width=True,
                key="hero_btn_upload",
                on_click=set_nav,
                args=("Documents Hub",)
            )
        with btn_c2:
            st.button(
                "Ask AI Assistant 💬",
                type="secondary",
                use_container_width=True,
                key="hero_btn_chat",
                on_click=set_nav,
                args=("AI Chat Assistant",)
            )

    with h_col2:
        # Top-right feature card (arrow removed as requested)
        st.markdown(
            """
            <div style="
                background: #FFFFFF;
                border: 1px solid #E4ECE9;
                border-radius: 20px;
                padding: 1.5rem;
                box-shadow: 0 4px 20px -2px rgba(13, 123, 112, 0.06);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 100%;
                text-align: left;
            ">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔮</div>
                <div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #11181C; margin-bottom: 0.4rem; line-height: 1.3;">
                        Everything your team needs, <span class="serif-italic">in perfect flow.</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #5F7377; line-height: 1.5;">
                        Multi-document semantic retrieval powered by Sentence Transformers & FAISS.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Motivo Metrics Ribbon Bar
    st.markdown(
        f"""
        <div class="motivo-metrics-ribbon">
            <div class="ribbon-item">
                <div class="ribbon-icon-circle" style="background: #E8F5F1; color: #0D7B70;">👥</div>
                <div>
                    <div class="ribbon-value">{total_docs}</div>
                    <div class="ribbon-label">Total Documents</div>
                </div>
            </div>
            <div class="ribbon-item">
                <div class="ribbon-icon-circle" style="background: #E0F2FE; color: #0284C7;">⚡</div>
                <div>
                    <div class="ribbon-value">{indexed_docs}</div>
                    <div class="ribbon-label">FAISS Vectors</div>
                </div>
            </div>
            <div class="ribbon-item">
                <div class="ribbon-icon-circle" style="background: #E8F5F1; color: #0D7B70;">📈</div>
                <div>
                    <div class="ribbon-value">{coverage_pct}</div>
                    <div class="ribbon-label">Knowledge Coverage</div>
                </div>
            </div>
            <div class="ribbon-item">
                <div class="ribbon-icon-circle" style="background: #F0FDF4; color: #16A34A;">🛡️</div>
                <div>
                    <div class="ribbon-value">FastAPI</div>
                    <div class="ribbon-label">RAG Backend Core</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Middle Two-Column Grid: Motivo Live Workspace Preview + Interactive Features Popover
    grid_col1, grid_col2 = st.columns([1.4, 1.3])

    with grid_col1:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <div style="font-size: 1.15rem; font-weight: 800; color: #11181C;">Good day, Explorer 👋</div>
                        <div style="font-size: 0.82rem; color: #5F7377;">Here is your live document intelligence overview.</div>
                    </div>
                    <span class="badge-mint">● Active Sync</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.metric(
                    label="Index Progress",
                    value=f"{indexed_docs} / {total_docs}",
                    delta=f"{coverage_pct} Searchable"
                )
            with m_col2:
                st.metric(
                    label="System Latency",
                    value=f"{backend_info.get('latency_ms', 0)} ms",
                    delta="Healthy" if backend_info["online"] else "Offline",
                    delta_color="normal" if backend_info["online"] else "inverse"
                )

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown(
                "<div style='font-size: 0.88rem; font-weight: 700; color: #11181C; margin-bottom: 8px;'>Recent Documents</div>",
                unsafe_allow_html=True
            )

            if not documents:
                st.info("No documents uploaded yet. Head over to the Documents Hub to add your first file!")
            else:
                for doc in documents[:3]:
                    d_id = get_document_id(doc)
                    d_name = get_document_name(doc)
                    d_type = doc.get("file_type", "txt").lower()
                    d_status = doc.get("status", "unknown")
                    d_badge = "badge-pdf" if d_type == "pdf" else ("badge-docx" if d_type == "docx" else "badge-txt")

                    r_col1, r_col2 = st.columns([3.5, 1.2])
                    with r_col1:
                        st.markdown(
                            f"""
                            <div style="display: flex; align-items: center; gap: 8px; padding: 6px 0;">
                                <span class="{d_badge}">{d_type.upper()}</span>
                                <span style="font-size: 0.88rem; font-weight: 600; color: #11181C;">{d_name}</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    with r_col2:
                        if d_status == "processed":
                            st.button(
                                "Query 💬",
                                key=f"dash_q_{d_id}",
                                use_container_width=True,
                                on_click=set_nav,
                                args=("AI Chat Assistant", d_id)
                            )

    with grid_col2:
        st.markdown(
            """
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0D7B70; margin-bottom: 4px;">Features</div>
                <div style="font-size: 1.55rem; font-weight: 800; color: #11181C; letter-spacing: -0.02em; line-height: 1.2;">
                    All the tools you need,<br>
                    <span class="serif-italic">beautifully connected.</span>
                </div>
                <div style="font-size: 0.84rem; color: #5F7377; margin-top: 6px; line-height: 1.5;">
                    Click any feature below to reveal detailed architectural and project implementation pop-up cards.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Feature 1 Pop-up Card
        with st.popover("⚙️ Smart Text Extraction — PyMuPDF & docx &rarr;", use_container_width=True):
            st.markdown(
                """
                ### ⚙️ Smart Text Extraction Pipeline
                - **Supported Formats**: `.pdf`, `.docx`, and `.txt` files up to **10 MB**.
                - **Engines Used**:
                  - **PyMuPDF (`fitz`)**: High-performance extraction of text spans, multi-column layouts, tables, and headers from PDF files.
                  - **python-docx**: Structured parsing of Microsoft Word paragraphs, headings, and bullet points.
                - **Text Sanitization**:
                  - Automated Unicode normalisation and whitespace cleanup.
                  - Empty and unreadable document detection (returns HTTP 422 if no readable characters exist).
                - **Storage**: Clean text is linked to a unique SQLite document record with metadata before indexing.
                """
            )

        # Feature 2 Pop-up Card
        with st.popover("⚡ Dense Vector Storage — Sentence Transformers & FAISS &rarr;", use_container_width=True):
            st.markdown(
                """
                ### ⚡ Dense Vector Storage & Indexing
                - **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` generating **384-dimensional** semantic embeddings.
                - **Chunking Strategy**: Recursive character chunking with contextual overlap to retain meaning across sentence boundaries.
                - **Vector Database**: **FAISS (`IndexFlatIP`)** vector store.
                  - Normalized inner product similarity matching cosine similarity.
                  - Sub-millisecond similarity search across thousands of text vectors.
                - **Lifecycle Synchronization**:
                  - Adding new documents dynamically updates the in-memory index.
                  - Deleting a document removes both metadata and corresponding FAISS vectors.
                """
            )

        # Feature 3 Pop-up Card
        with st.popover("🧠 Contextual RAG Retrieval — Neural QA & Sourcing &rarr;", use_container_width=True):
            st.markdown(
                """
                ### 🧠 Contextual RAG Retrieval Architecture
                - **Query Embedding**: The user's natural language question is encoded into a 384-dimensional query vector.
                - **Similarity Search**: FAISS retrieves the top-k most semantically relevant text chunks.
                - **Targeted Knowledge Scoping**:
                  - Search across **All Indexed Documents** for broad answers.
                  - Scope down to **Specific Documents** for focused contract or manual analysis.
                - **Response Synthesis**:
                  - Retrieved passages are combined into a grounded prompt context.
                  - The LLM generates factual, context-grounded answers accompanied by exact source chunks and similarity scores.
                """
            )

    # Bottom Two-Column Motivo Highlight Cards
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns([1, 1])

    with b_col1:
        st.markdown(
            """
            <div class="motivo-deep-teal-card">
                <div>
                    <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: rgba(255,255,255,0.7); margin-bottom: 12px;">Trusted by Teams</div>
                    <div style="font-size: 2rem; line-height: 1; font-family: var(--font-serif-italic); margin-bottom: 8px;">“</div>
                    <p style="font-size: 1.05rem; line-height: 1.55; font-weight: 500; margin: 0 0 1.5rem 0; color: #FFFFFF !important;">
                        NEXOR has completely transformed how our team searches complex contracts and technical documentation. It is fast, accurate, and saves hours of manual work every day.
                    </p>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.1rem;">⭐⭐⭐⭐⭐</span>
                        <span style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF !important;">4.9 / 5</span>
                    </div>
                    <span style="font-size: 0.75rem; color: rgba(255,255,255,0.85) !important;">Production Proven</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b_col2:
        with st.container(border=True):
            st.markdown(
                """
                <div style="padding: 0.5rem 0.5rem;">
                    <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #0D7B70; margin-bottom: 8px;">Ready to explore?</div>
                    <div style="font-size: 1.7rem; font-weight: 800; color: #11181C; letter-spacing: -0.025em; line-height: 1.2; margin-bottom: 10px;">
                        Let's analyze something<br>
                        <span class="serif-italic">amazing together.</span>
                    </div>
                    <p style="font-size: 0.9rem; color: #5F7377; line-height: 1.5; margin-bottom: 1.5rem;">
                        Start by uploading your PDF, DOCX, or TXT documents, or query existing knowledge vectors directly.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.button(
                "Start Asking Questions &rarr;",
                type="primary",
                use_container_width=True,
                key="bottom_cta_chat",
                on_click=set_nav,
                args=("AI Chat Assistant",)
            )


# =========================================================
# PAGE 2: DOCUMENTS HUB (FULL PAGE: UPLOAD + REPOSITORY)
# =========================================================

elif current_page == "Documents":

    st.markdown(
        """
        <div style="margin-bottom: 1.5rem; padding-top: 0.25rem;">
            <div class="motivo-pill-badge">
                <span class="badge-tag">WORKSPACE</span>
                <span>Document Ingestion & Repository</span>
            </div>
            <h1 class="motivo-headline" style="font-size: 2.2rem; margin-bottom: 0.25rem;">
                Document Repository & <span class="serif-italic">Indexing Hub</span>
            </h1>
            <p class="motivo-subheadline" style="margin-bottom: 0;">
                Upload new files for vector processing and manage your stored knowledge vectors in one view.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SECTION 1: UPLOAD DOCUMENTS (TOP)
    # -----------------------------------------------------
    with st.container(border=True):
        st.markdown(
            """
            <div style="margin-bottom: 1rem;">
                <div style="font-weight: 800; font-size: 1.2rem; color: #11181C;">Upload Documents</div>
                <div style="font-size: 0.85rem; color: #5F7377; margin-top: 4px;">
                    Supported: <span class="badge-pdf">PDF</span> <span class="badge-docx">DOCX</span> <span class="badge-txt">TXT</span> &bull; Max file size: <b>10 MB</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        uploaded_files = st.file_uploader(
            "Choose your documents",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Select one or more PDF, DOCX, or TXT files to process.",
            label_visibility="collapsed"
        )

        if uploaded_files:
            st.markdown(
                f"<div style='margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 700; font-size: 0.9rem; color: #11181C;'>Selected Files ({len(uploaded_files)}):</div>",
                unsafe_allow_html=True
            )

            for f in uploaded_files:
                f_size = format_file_size(len(f.getvalue()))
                f_ext = f.name.split(".")[-1].lower() if "." in f.name else "txt"
                badge_style = "badge-pdf" if f_ext == "pdf" else ("badge-docx" if f_ext == "docx" else "badge-txt")

                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; background: #FFFFFF; border: 1.5px solid #E4ECE9; border-radius: 10px; padding: 10px 14px; margin-bottom: 6px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span class="{badge_style}">{f_ext.upper()}</span>
                            <span style="font-weight: 600; font-size: 0.9rem; color: #11181C;">{f.name}</span>
                        </div>
                        <span style="font-size: 0.8rem; color: #5F7377; font-family: var(--font-mono); font-weight: 600;">{f_size}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if st.button("🚀 Upload and Index Documents &rarr;", type="primary", use_container_width=True, key="btn_run_upload"):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                total = len(uploaded_files)

                for index, file in enumerate(uploaded_files):
                    status_text.info(f"⏳ Extracting and indexing **{file.name}**...")
                    res = upload_and_index(file)
                    results.append(res)
                    progress_bar.progress((index + 1) / total)

                st.session_state.upload_results = results
                status_text.success("🎉 All documents uploaded, text extracted, and indexed into FAISS!")

    # Results summary cards
    if st.session_state.upload_results:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #11181C; font-weight: 800;'>Upload & Indexing Results</h3>", unsafe_allow_html=True)

        for res in st.session_state.upload_results:
            if res.get("success"):
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="color: #0D7B70; font-size: 1.1rem; font-weight: 800;">✔</span>
                                <span style="font-weight: 800; font-size: 1rem; color: #11181C;">{res['filename']}</span>
                            </div>
                            <span class="badge-mint">● Indexed in FAISS</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Document ID", f"#{res['document_id']}")
                    with c2:
                        st.metric("Characters", f"{res['extracted_text_length']:,}")
                    with c3:
                        st.metric("Chunks Created", res['chunks_created'])
                    with c4:
                        st.metric("File Size", format_file_size(res.get('file_size')))

                    st.button(
                        f"💬 Chat with {res['filename']} &rarr;",
                        key=f"res_q_{res['document_id']}",
                        on_click=set_nav,
                        args=("AI Chat Assistant", res['document_id'])
                    )
            else:
                st.error(f"❌ **{res.get('filename')}**: {res.get('error')}")

        if st.button("Clear Results Summary", key="clear_results"):
            st.session_state.upload_results = []
            st.rerun()

    # -----------------------------------------------------
    # SECTION 2: STORED DOCUMENT REPOSITORY (BELOW UPLOAD)
    # -----------------------------------------------------
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <div style="font-weight: 800; font-size: 1.4rem; color: #11181C;">
                Stored Documents Repository <span style="font-size: 1.1rem; color: #0D7B70; font-weight: 700;">({len(documents)} files)</span>
            </div>
            <div style="font-size: 0.85rem; color: #5F7377;">Search, filter, and inspect all indexed files stored in the SQLite database and FAISS index.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.delete_success_message:
        st.success(st.session_state.delete_success_message)
        st.session_state.delete_success_message = None

    # Filter & Action Toolbar
    with st.container(border=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
        with f_col1:
            search_query = st.text_input(
                "Search repository",
                placeholder="Search by title or ID...",
                label_visibility="collapsed"
            )
        with f_col2:
            format_filter = st.selectbox(
                "Format",
                ["All Formats", "PDF", "DOCX", "TXT"],
                label_visibility="collapsed"
            )
        with f_col3:
            status_filter = st.selectbox(
                "Status",
                ["All Statuses", "Indexed", "Pending", "Failed"],
                label_visibility="collapsed"
            )
        with f_col4:
            if st.button("🔄 Refresh List", use_container_width=True, key="btn_refresh_repo"):
                st.rerun()

    # Filter documents
    filtered = documents
    if search_query:
        filtered = [
            d for d in filtered
            if search_query.lower() in get_document_name(d).lower() or search_query.lower() in str(get_document_id(d))
        ]

    if format_filter != "All Formats":
        filtered = [
            d for d in filtered
            if d.get("file_type", "").lower() == format_filter.lower()
        ]

    if status_filter != "All Statuses":
        req_status = "processed" if status_filter == "Indexed" else status_filter.lower()
        filtered = [
            d for d in filtered
            if d.get("status", "").lower() == req_status
        ]

    if not filtered:
        if not documents:
            st.info("No documents uploaded yet. Use the upload box above to add your first document!")
        else:
            st.info("No documents match your filter criteria.")
    else:
        table_rows = []
        for doc in filtered:
            doc_id = get_document_id(doc)
            name = get_document_name(doc)
            file_type = doc.get("file_type", "N/A").upper()
            status_val = "Indexed" if doc.get("status") == "processed" else doc.get("status", "unknown").capitalize()
            created = doc.get("created_at", "N/A")
            if len(created) >= 19:
                created = created[:19].replace("T", " ")

            table_rows.append({
                "Doc ID": f"#{doc_id}",
                "Document Name": name,
                "Format": file_type,
                "Status": status_val,
                "Indexed Date": created
            })

        st.dataframe(
            table_rows,
            width="stretch",
            hide_index=True,
            column_config={
                "Doc ID": st.column_config.TextColumn("Doc ID", width="small"),
                "Document Name": st.column_config.TextColumn("Document Name", width="large"),
                "Format": st.column_config.TextColumn("Format", width="small"),
                "Status": st.column_config.TextColumn("Status", width="medium"),
                "Indexed Date": st.column_config.TextColumn("Indexed Date", width="medium")
            }
        )

    # -----------------------------------------------------
    # SECTION 3: PERMANENT DELETION CARD (AT BOTTOM)
    # -----------------------------------------------------
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.4rem;">
                <span style="color: #BE123C; font-size: 1.1rem;">🗑️</span>
                <span style="font-weight: 800; font-size: 1.1rem; color: #11181C;">Delete a Document</span>
            </div>
            <div style="font-size: 0.85rem; color: #5F7377; margin-bottom: 1rem;">
                Permanently delete a document file, its SQLite record, and all vector embeddings from the FAISS database.
            </div>
            """,
            unsafe_allow_html=True
        )

        if not documents:
            st.caption("No documents available to delete.")
        else:
            doc_options = {
                f"{get_document_name(doc)} (ID: #{get_document_id(doc)})": get_document_id(doc)
                for doc in documents
            }

            del_c1, del_c2 = st.columns([2, 1])
            with del_c1:
                target_doc_label = st.selectbox(
                    "Select document to delete",
                    options=list(doc_options.keys()),
                    key="delete_doc_selector"
                )
            with del_c2:
                st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
                confirmed = st.checkbox("Confirm permanent deletion", key="confirm_delete_box")

            if st.button("Delete Selected Document", type="primary", disabled=not confirmed, use_container_width=True, key="btn_confirm_delete"):
                doc_id_to_del = doc_options[target_doc_label]
                with st.spinner("Deleting document and clearing FAISS vectors..."):
                    del_res = delete_document_api(doc_id_to_del)

                if del_res.get("success"):
                    st.session_state.delete_success_message = del_res.get("message", "Document deleted successfully.")
                    st.session_state.last_query_result = None
                    st.rerun()
                else:
                    st.error(del_res.get("message", "Failed to delete document."))


# =========================================================
# PAGE 3: AI CHAT ASSISTANT
# =========================================================

elif current_page == "AI Assistant":

    st.markdown(
        """
        <div style="margin-bottom: 1.5rem; padding-top: 0.25rem;">
            <div class="motivo-pill-badge">
                <span class="badge-tag">RAG CHAT</span>
                <span>Neural Conversational Assistant</span>
            </div>
            <h1 class="motivo-headline" style="font-size: 2.2rem; margin-bottom: 0.25rem;">
                AI Document <span class="serif-italic">Assistant</span>
            </h1>
            <p class="motivo-subheadline" style="margin-bottom: 0;">
                Ask natural-language questions and receive grounded, sourced answers from your documents.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    indexed_documents = [d for d in documents if d.get("status") == "processed"]

    if not indexed_documents:
        with st.container(border=True):
            st.markdown(
                """
                <div style="text-align: center; padding: 2.5rem 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📂</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #11181C; margin-bottom: 0.5rem;">No Indexed Documents Available</div>
                    <p style="font-size: 0.9rem; color: #5F7377; max-width: 480px; margin: 0 auto 1.5rem auto;">
                        Please upload and index at least one PDF, DOCX, or TXT file to begin querying.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            _, c_btn, _ = st.columns([1.5, 1, 1.5])
            with c_btn:
                st.button(
                    "Go to Documents Hub &rarr;",
                    type="primary",
                    use_container_width=True,
                    key="btn_goto_docs",
                    on_click=set_nav,
                    args=("Documents Hub",)
                )
    else:
        # Knowledge Scope Selector (with high-contrast explicit text)
        target_doc_id = st.session_state.get("target_chat_doc_id")

        with st.container(border=True):
            sc_c1, sc_c2 = st.columns([1.1, 1.9])
            with sc_c1:
                scope_idx = 1 if target_doc_id else 0
                scope_choice = st.radio(
                    "Search Scope",
                    ["🌐 All Indexed Documents", "🎯 Select Specific Documents"],
                    index=scope_idx,
                    horizontal=False
                )

            selected_docs = []
            with sc_c2:
                if "Specific" in scope_choice:
                    doc_dict = {
                        f"{get_document_name(d)} (ID: #{get_document_id(d)})": d
                        for d in indexed_documents
                    }
                    defaults = []
                    if target_doc_id:
                        for label, d in doc_dict.items():
                            if str(get_document_id(d)) == str(target_doc_id):
                                defaults.append(label)
                        st.session_state.target_chat_doc_id = None

                    chosen_labels = st.multiselect(
                        "Choose target documents for retrieval",
                        options=list(doc_dict.keys()),
                        default=defaults,
                        placeholder="Select one or more documents..."
                    )
                    selected_docs = [doc_dict[k] for k in chosen_labels]
                else:
                    st.markdown(
                        f"""
                        <div style="padding-top: 1.25rem;">
                            <span style="font-size: 0.9rem; font-weight: 800; color: #11181C;">Full Knowledge Base Scope</span>
                            <div style="font-size: 0.82rem; color: #5F7377;">Searching across all {len(indexed_documents)} indexed document(s) in FAISS.</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Empty State Suggested Prompts
        if not st.session_state.chat_history:
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(
                    """
                    <div style="margin-bottom: 0.75rem;">
                        <div style="font-size: 1.1rem; font-weight: 800; color: #11181C;">✨ Suggested Inquiries</div>
                        <div style="font-size: 0.82rem; color: #5F7377;">Click any prompt to instantly query the knowledge base:</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                p1, p2 = st.columns(2)
                prompts = [
                    "Summarize the key takeaways and main concepts.",
                    "What technologies, frameworks, or tools are covered?",
                    "List all key requirements, recommendations, or guidelines.",
                    "Provide an executive overview of the uploaded content."
                ]

                chosen_prompt = None
                with p1:
                    if st.button(f"📌 {prompts[0]}", use_container_width=True, key="p_btn_0"):
                        chosen_prompt = prompts[0]
                    if st.button(f"📌 {prompts[1]}", use_container_width=True, key="p_btn_1"):
                        chosen_prompt = prompts[1]
                with p2:
                    if st.button(f"📌 {prompts[2]}", use_container_width=True, key="p_btn_2"):
                        chosen_prompt = prompts[2]
                    if st.button(f"📌 {prompts[3]}", use_container_width=True, key="p_btn_3"):
                        chosen_prompt = prompts[3]

                if chosen_prompt:
                    st.session_state["pending_prompt"] = chosen_prompt
                    st.rerun()

        # Render Conversation Feed
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"**{msg['content']}**")
                    if msg.get("timestamp"):
                        st.caption(f"Sent at {msg['timestamp']}")
            else:
                with st.chat_message("assistant", avatar="✳️"):
                    st.markdown(msg["content"])
                    sources = msg.get("sources", [])
                    if sources:
                        with st.expander(f"📚 Retrieved Sources ({len(sources)})", expanded=False):
                            for idx, s in enumerate(sources, 1):
                                doc_id = s.get("document_id", "N/A")
                                score = s.get("score")
                                chunk = s.get("chunk", "No content snippet.")
                                score_badge = f"Similarity: {score:.4f}" if score is not None else "Relevance: High"

                                st.markdown(
                                    f"""
                                    <div class="source-box">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                            <span style="font-size: 0.82rem; font-weight: 800; color: #0D7B70;">Source {idx} &bull; Document #{doc_id}</span>
                                            <span class="badge-mint">{score_badge}</span>
                                        </div>
                                        <p class="source-box-text">{chunk}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

        # Prominent Interactive Query Bar (Replaces black footer look & prevents auto-scroll)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">💬</span>
                        <span style="font-weight: 800; font-size: 1rem; color: #11181C;">Ask a Question about your Documents</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.form("inpage_query_form", clear_on_submit=True, border=False):
                q_col1, q_col2 = st.columns([5, 1])
                with q_col1:
                    interactive_query = st.text_input(
                        "Enter your question",
                        placeholder="E.g. What are the key concepts and recommendations?",
                        label_visibility="collapsed",
                        key="inpage_query_input"
                    )
                with q_col2:
                    btn_ask = st.form_submit_button("Send 🚀", type="primary", use_container_width=True)

            if st.session_state.chat_history:
                if st.button("Clear Conversation History", key="btn_clear_chat"):
                    st.session_state.chat_history = []
                    st.session_state.last_query_result = None
                    st.rerun()

        # Handle Query Input (from in-page form or suggested prompt click)
        query_input = None
        if btn_ask and interactive_query.strip():
            query_input = interactive_query.strip()
        elif st.session_state.get("pending_prompt"):
            query_input = st.session_state.pop("pending_prompt")

        if query_input:
            if "Specific" in scope_choice and not selected_docs:
                st.warning("⚠️ Please select at least one document from the dropdown above.")
            else:
                ts = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": query_input,
                    "timestamp": ts
                })

                with st.spinner("Searching FAISS vectors and synthesizing answer..."):
                    q_res = ask_question(
                        query=query_input,
                        selected_documents=selected_docs if "Specific" in scope_choice else None
                    )

                st.session_state.last_query_result = q_res

                if q_res.get("success"):
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": q_res.get("answer", "No answer could be generated."),
                        "sources": q_res.get("sources", []),
                        "searched_docs": str(q_res.get("searched_document_ids", "")),
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                else:
                    err_msg = q_res.get("error", "Failed to retrieve an answer.")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"⚠️ **Error generating answer:** {err_msg}\n\n*If the FAISS vector index was cleared, please re-upload or re-index your documents in the Documents Hub.*",
                        "sources": [],
                        "searched_docs": "",
                        "timestamp": datetime.now().strftime("%H:%M")
                    })

                st.rerun()
