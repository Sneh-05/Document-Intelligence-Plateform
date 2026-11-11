import streamlit as st
import requests
from pathlib import Path
import sys

# ==========================================
# BACKEND CONNECTION
# ==========================================

PROJECT_PATH = Path(__file__).resolve().parent.parent
BACKEND_APP_PATH = PROJECT_PATH / "backend" / "app"
BACKEND_URL = "http://127.0.0.1:8000"

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

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #536DFE, #6875F5) !important;
    color: #FFFFFF !important;
    border: 1px solid #7188FF !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
}

.stButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
}

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

[data-testid="stFileUploaderDropzone"] button {
    background: #536DFE !important;
    color: #FFFFFF !important;
    border: 1px solid #7188FF !important;
    border-radius: 9px !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

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

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

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
        "Navigate to Documents to upload a PDF or DOCX file, "
        "then go to AI Assistant to ask questions about it."
    )

# ==========================================
# DOCUMENT WORKSPACE
# ==========================================

elif page == "Documents":

    st.title("📁 Document Workspace")
    st.write("Upload your PDF or DOCX document to extract and index its text.")

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "docx"],
        key="document_upload"
    )

    if uploaded_file:

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("⚡ Extract & Index", key="extract_button"):

            if extract_text is None:
                st.error(f"Document processor import failed: {import_error}")

            else:
                try:
                    # 1. Save file temporarily
                    temp_dir = PROJECT_PATH / "frontend" / "temp_uploads"
                    temp_dir.mkdir(exist_ok=True)
                    file_path = temp_dir / uploaded_file.name
                    file_path.write_bytes(uploaded_file.getvalue())

                    # 2. Extract text
                    with st.spinner("Extracting text..."):
                        extracted_text = extract_text(str(file_path))

                    if not extracted_text.strip():
                        st.warning("No text found in this document. Scanned PDFs may require OCR.")
                    else:
                        st.session_state["extracted_text"] = extracted_text
                        st.session_state["document_name"] = uploaded_file.name

                        # 3. Register document in DB via backend
                        file_type = uploaded_file.name.split(".")[-1].lower()
                        with st.spinner("Registering document..."):
                            reg_response = requests.post(
                                f"{BACKEND_URL}/documents",
                                json={
                                    "title": uploaded_file.name,
                                    "file_type": file_type
                                }
                            )
                            reg_response.raise_for_status()
                            doc_data = reg_response.json()
                            document_id = doc_data["id"]
                            st.session_state["document_id"] = document_id

                        # 4. Send extracted text to backend for chunking + indexing
                        with st.spinner("Indexing document for AI search..."):
                            index_response = requests.post(
                                f"{BACKEND_URL}/documents/{document_id}/index",
                                json={"text": extracted_text}
                            )
                            index_response.raise_for_status()
                            index_data = index_response.json()

                        st.success(
                            f"Document indexed successfully! "
                            f"{index_data['chunks_created']} chunks created. "
                            f"You can now ask questions in the AI Assistant."
                        )

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to backend. "
                        "Make sure the FastAPI server is running: "
                        "uvicorn main:app --reload"
                    )
                except Exception as e:
                    st.error(f"Processing failed: {e}")

    if st.session_state.get("extracted_text"):

        st.markdown('<p class="section-title">Extracted Content</p>', unsafe_allow_html=True)
        st.caption(st.session_state.get("document_name", ""))

        extracted_text = st.session_state["extracted_text"]
        st.text_area("Document Text", value=extracted_text, height=350)
        st.download_button(
            "Download Extracted Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

# ==========================================
# AI ASSISTANT
# ==========================================

elif page == "AI Assistant":

    st.title("🤖 AI Document Assistant")
    st.write("Ask questions about your uploaded document.")

    # Check if a document has been indexed in this session
    document_id = st.session_state.get("document_id")
    document_name = st.session_state.get("document_name")

    if not document_id:
        st.warning(
            "No document indexed yet. "
            "Go to Documents, upload a file, and click Extract & Index first."
        )
    else:
        st.info(f"Active document: **{document_name}** (ID: {document_id})")

        question = st.text_input(
            "Ask your question",
            placeholder="What are the payment terms?"
        )

        if st.button("Ask AI"):

            if not question.strip():
                st.warning("Please enter a question.")

            else:
                try:
                    with st.spinner("Thinking..."):
                        response = requests.post(
                            f"{BACKEND_URL}/query",
                            json={
                                "document_id": document_id,
                                "query": question
                            }
                        )
                        response.raise_for_status()
                        result = response.json()

                    st.markdown('<p class="section-title">Answer</p>', unsafe_allow_html=True)
                    st.write(result["answer"])

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Cannot connect to backend. "
                        "Make sure the FastAPI server is running: "
                        "uvicorn main:app --reload"
                    )
                except requests.exceptions.HTTPError as e:
                    st.error(f"Backend error: {e.response.json().get('detail', str(e))}")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
