import streamlit as st
from pathlib import Path
import sys

# ==========================================
# BACKEND CONNECTION
# ==========================================

PROJECT_PATH = Path(__file__).resolve().parent.parent
BACKEND_APP_PATH = PROJECT_PATH / "backend" / "app"

sys.path.insert(0, str(BACKEND_APP_PATH))

try:
    from document_processor import extract_text
    import_error = None
except Exception as e:
    extract_text = None
    import_error = str(e)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NEXOR | Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #080E1B, #101D35);
    color: #F8FAFC;
}

.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

[data-testid="stSidebar"] {
    background: #111C32;
    border-right: 1px solid #293B59;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #F1F5F9 !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    font-weight: 600 !important;
}

.hero {
    background: linear-gradient(120deg, #142B4D, #293E78);
    padding: 35px;
    border-radius: 18px;
    border: 1px solid #3D5688;
    margin-bottom: 28px;
}

.hero h1 {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 700;
}

.hero p {
    color: #D6E3F5;
    font-size: 16px;
}

.metric {
    background: #16243B;
    border: 1px solid #304666;
    padding: 23px;
    border-radius: 15px;
    min-height: 130px;
}

.metric h2 {
    color: #A5B4FC;
    font-size: 27px;
}

.metric p {
    color: #E2E8F0;
    font-size: 15px;
}

.section-title {
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 700;
    margin-top: 28px;
}

/* All action buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #536DFE, #6875F5) !important;
    color: #FFFFFF !important;
    border: 1px solid #7188FF !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
}

/* Button text visibility */
.stButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
}

/* Hover effect */
.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #4055D6 !important;
    color: #FFFFFF !important;
    border: 1px solid #8EA0FF !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #17243A;
    color: #FFFFFF;
    border: 1px solid #405477;
}

[data-testid="stFileUploader"] {
    background: #16243B !important;
    border: 1px solid #536DFE !important;
    border-radius: 16px !important;
    padding: 18px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #1C2D49 !important;
    border: 2px dashed #7188B5 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Browse Files button */
[data-testid="stFileUploaderDropzone"] button {
    background: #536DFE !important;
    color: #FFFFFF !important;
    border: 1px solid #7188FF !important;
    border-radius: 9px !important;
}

/* Uploaded file name */
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Uploaded file details */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}
[data-testid="stFileUploader"] small {
    color: #DCE7F7 !important;
}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #FFFFFF !important;
}

h1, h2, h3, p, label {
    color: #F8FAFC;
}
/* Remove white Streamlit header */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Match toolbar with dark theme */
[data-testid="stToolbar"] {
    background: transparent !important;
}

/* Remove top decoration */
[data-testid="stDecoration"] {
    display: none !important;
}

/* Main app background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #080E1B, #101D35);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🧠 NeuralX")

    st.markdown(
        "<p style='color:#B8C7E0;font-size:13px;'>"
        "DOCUMENT INTELLIGENCE PLATFORM"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Documents", "AI Assistant"],
        key="navigation_menu"
    )

    st.divider()

    st.markdown(
        "<p style='color:#B8C7E0;font-size:13px;'>"
        "Powered by intelligent document processing"
        "</p>",
        unsafe_allow_html=True
    )


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Document Intelligence Platform</h1>
        <p>
        Transform your documents into meaningful insights.
        Upload, extract and explore your information in one place.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric">
            <h2>📄</h2>
            <p>Smart Document Processing</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric">
            <h2>⚡</h2>
            <p>Fast Text Extraction</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric">
            <h2>🤖</h2>
            <p>AI-Powered Insights</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<p class="section-title">Get Started</p>',
        unsafe_allow_html=True
    )

    st.info(
        "Navigate to Documents to upload a PDF or DOCX file "
        "and extract its text."
    )


# ==========================================
# DOCUMENT WORKSPACE
# ==========================================

elif page == "Documents":

    st.title("📁 Document Workspace")

    st.write(
        "Upload your PDF or DOCX document to extract its text."
    )

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "docx"],
        key="document_upload"
    )

    if uploaded_file:

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("⚡ Extract Text", key="extract_button"):

            if extract_text is None:

                st.error(
                    f"Document processor import failed: {import_error}"
                )

            else:

                try:

                    temp_dir = PROJECT_PATH / "frontend" / "temp_uploads"
                    temp_dir.mkdir(exist_ok=True)

                    file_path = temp_dir / uploaded_file.name

                    file_path.write_bytes(
                        uploaded_file.getvalue()
                    )

                    extracted_text = extract_text(str(file_path))

                    st.session_state["extracted_text"] = extracted_text
                    st.session_state["document_name"] = uploaded_file.name

                    st.success("Document text extracted successfully!")

                except Exception as e:

                    st.error(f"Extraction failed: {e}")

    if st.session_state.get("extracted_text"):

        st.markdown(
            '<p class="section-title">Extracted Content</p>',
            unsafe_allow_html=True
        )

        st.caption(
            st.session_state.get("document_name", "")
        )

        extracted_text = st.session_state["extracted_text"]

        if extracted_text.strip():

            st.text_area(
                "Document Text",
                value=extracted_text,
                height=350
            )

            st.download_button(
                "Download Extracted Text",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )

        else:

            st.warning(
                "No text was found in this document. "
                "Scanned PDFs may require OCR."
            )


# ==========================================
# AI ASSISTANT
# ==========================================

elif page == "AI Assistant":

    st.title("🤖 AI Document Assistant")

    st.write(
        "Interact with your documents using intelligent AI assistance."
    )

    st.info(
        "AI question-answering will be available after "
        "the RAG and AI backend integration."
    )

    question = st.text_input(
        "Ask your question",
        placeholder="What is this document about?"
    )

    if st.button("Ask AI"):

        if question.strip():

            st.warning(
                "AI answering functionality is coming soon."
            )

        else:

            st.warning("Please enter a question.")