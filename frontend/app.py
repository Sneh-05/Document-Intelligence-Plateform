
import os

import requests
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="NEXOR | Document Intelligence",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# CUSTOM CSS - NEXOR FINAL THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       MAIN APPLICATION
    ========================================= */

    .stApp {
        background-color: #F9FAFC;
        color: #292929;
        font-family: Arial, sans-serif;
    }

    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 2rem;
    }

    /* =========================================
       TOP HEADER - REMOVE BLACK BACKGROUND
    ========================================= */

    header[data-testid="stHeader"] {
        background-color: #F9FAFC !important;
        height: 3.5rem;
    }

    .stAppHeader {
        background-color: #F9FAFC !important;
    }

    div[data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    /* =========================================
       SIDEBAR
    ========================================= */

    section[data-testid="stSidebar"] {
        background-color: #FFCA83;
        border-right: 1px solid #F2BB70;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 7px;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.18);
    }

    /* =========================================
       HEADINGS AND TEXT
    ========================================= */

    .main-title {
        font-size: 30px;
        font-weight: 700;
        color: #292929;
        margin-bottom: 0;
    }

    .subtitle {
        color: #929292;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #292929;
        font-size: 21px;
        font-weight: 650;
    }

    p, li {
        color: #444444;
    }

    /* =========================================
       DASHBOARD METRIC CARDS
    ========================================= */

    div[data-testid="stMetric"] {
        background-color: #FFF8EF;
        padding: 20px;
        border-radius: 9px;
        border: 1px solid #FFF0DE;
        box-shadow: none;
    }

    div[data-testid="stMetric"] label {
        color: #929292;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #292929;
        font-weight: 700;
    }

    /* =========================================
       CONTENT CONTAINERS
    ========================================= */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-color: #E5E5E5;
        border-radius: 9px;
    }

    /* =========================================
       BUTTONS
    ========================================= */

    div.stButton > button {
        background-color: #F5C477;
        color: #292929;
        border: 1px solid #F5C477;
        border-radius: 7px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #EBAF58;
        border-color: #EBAF58;
        color: #292929;
    }

    /* =========================================
       INPUT FIELDS
    ========================================= */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF;
        color: #292929;
        border-radius: 7px;
        border-color: #DDDDDD;
    }

    /* =========================================
       FILE UPLOADER
    ========================================= */

    section[data-testid="stFileUploader"] {
        background-color: #FFF8EF;
        border: 1px dashed #F5C477;
        border-radius: 9px;
        padding: 12px;
    }

    /* =========================================
       DATA TABLE
    ========================================= */

    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E5E5;
        border-radius: 9px;
    }

    /* =========================================
       DOCUMENT STATUS BADGES
    ========================================= */

    .status-indexed {
        background-color: #E8F5E9;
        color: #267342;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
    }

    .status-uploaded {
        background-color: #FFF1D6;
        color: #946200;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
    }

    /* =========================================
       DIVIDERS AND ALERTS
    ========================================= */

    hr {
        border-color: #E8E8E8;
    }

    div[data-testid="stAlert"] {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# =========================================================
# SESSION STATE
# =========================================================

if "upload_results" not in st.session_state:
    st.session_state.upload_results = []

if "last_query_result" not in st.session_state:
    st.session_state.last_query_result = None

if "delete_success_message" not in st.session_state:
    st.session_state.delete_success_message = None

# =========================================================
# API HELPERS
# =========================================================

def check_backend():
    """Check whether the FastAPI backend is running."""

    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def get_documents():
    """Fetch documents from the backend."""

    try:
        response = requests.get(
            f"{BACKEND_URL}/documents",
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("documents", [])

        return []

    except requests.RequestException as error:
        st.error(f"Unable to fetch documents: {error}")
        return []


def delete_document_api(document_id):
    """Delete a document through the FastAPI backend."""

    try:
        response = requests.delete(
            f"{BACKEND_URL}/documents/{document_id}",
            timeout=30
        )

        response.raise_for_status()

        return {
            "success": True,
            "message": response.json().get(
                "message",
                "Document deleted successfully."
            )
        }

    except requests.HTTPError as error:

        message = "Unable to delete document."

        if error.response is not None:
            try:
                message = error.response.json().get(
                    "detail",
                    error.response.text
                )
            except ValueError:
                message = error.response.text

        return {
            "success": False,
            "message": message
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "message": str(error)
        }

def get_document_id(document):
    """Support different document ID field names."""

    return document.get(
        "document_id",
        document.get("id")
    )


def get_document_name(document):
    """Get a readable document name."""

    return (
        document.get("filename")
        or document.get("title")
        or document.get("file_name")
        or "Untitled Document"
    )


def upload_and_index(file):
    """
    Upload a document through FastAPI,
    extract its text and index it into FAISS.
    """

    try:
        # STEP 1: Upload document

        files = {
            "file": (
                file.name,
                file.getvalue(),
                file.type or "application/octet-stream"
            )
        }

        upload_response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files,
            timeout=120
        )

        upload_response.raise_for_status()

        upload_data = upload_response.json()

        document_id = upload_data.get("document_id")
        extracted_text = upload_data.get("extracted_text", "")

        if document_id is None:
            raise ValueError(
                "Backend did not return a document ID."
            )

        if not extracted_text.strip():
            raise ValueError(
                "No text could be extracted from this document."
            )

        # STEP 2: Index extracted text

        index_response = requests.post(
            f"{BACKEND_URL}/documents/{document_id}/index",
            json={
                "text": extracted_text
            },
            timeout=180
        )

        index_response.raise_for_status()

        index_data = index_response.json()

        return {
            "success": True,
            "document_id": document_id,
            "filename": file.name,
            "extracted_text_length": len(extracted_text),
            "chunks_created": index_data.get(
                "chunks_created", 0
            ),
            "message": index_data.get(
                "message",
                "Document uploaded and indexed successfully."
            )
        }

    except requests.HTTPError as error:

        message = "Backend request failed."

        if error.response is not None:
            try:
                message = error.response.json().get(
                    "detail",
                    error.response.text
                )
            except ValueError:
                message = error.response.text

        return {
            "success": False,
            "filename": file.name,
            "error": message
        }

    except (requests.RequestException, ValueError) as error:

        return {
            "success": False,
            "filename": file.name,
            "error": str(error)
        }


def ask_question(query, selected_documents):
    """Send a question to the RAG query endpoint."""

    payload = {
        "query": query
    }

    if selected_documents:
        document_ids = [
            get_document_id(document)
            for document in selected_documents
        ]

        document_ids = [
            doc_id for doc_id in document_ids
            if doc_id is not None
        ]

        if len(document_ids) == 1:
            payload["document_id"] = document_ids[0]

        elif len(document_ids) > 1:
            payload["document_ids"] = document_ids

    try:
        response = requests.post(
            f"{BACKEND_URL}/query",
            json=payload,
            timeout=180
        )

        response.raise_for_status()

        return response.json()

    except requests.HTTPError as error:

        message = "Unable to generate an answer."

        if error.response is not None:
            try:
                message = error.response.json().get(
                    "detail",
                    error.response.text
                )
            except ValueError:
                message = error.response.text

        st.error(f"Query failed: {message}")

    except requests.RequestException as error:
        st.error(f"Backend connection error: {error}")

    return None


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("NEXOR")
st.sidebar.caption("Document Intelligence Platform")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Documents",
        "AI Assistant"
    ]
)

st.sidebar.divider()

if check_backend():
    st.sidebar.success("Backend Connected")
else:
    st.sidebar.error("Backend Disconnected")

st.sidebar.caption(
    "Powered by FastAPI, FAISS and Coforge LLM"
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<p class="main-title">NEXOR Dashboard</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Your intelligent document workspace</p>',
        unsafe_allow_html=True
    )

    backend_status = check_backend()
    documents = get_documents()

    total_documents = len(documents)

    indexed_documents = sum(
        1
        for document in documents
        if document.get("status") == "processed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Documents",
            total_documents
        )

    with col2:
        st.metric(
            "Indexed Documents",
            indexed_documents
        )

    with col3:
        st.metric(
            "Backend Status",
            "Online" if backend_status else "Offline"
        )

    st.divider()

    st.markdown(
        '<p class="section-title">Welcome to NEXOR</p>',
        unsafe_allow_html=True
    )

    st.write(
        """
        NEXOR is an AI-powered Document Intelligence Platform
        that allows users to upload documents and ask questions
        using Retrieval-Augmented Generation (RAG).
        """
    )

    st.markdown("### How it works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**01. Upload**")
        st.caption("Upload PDF, DOCX or TXT files.")

    with col2:
        st.markdown("**02. Extract**")
        st.caption("Extract text from uploaded documents.")

    with col3:
        st.markdown("**03. Index**")
        st.caption("Generate embeddings and store vectors using FAISS.")

    with col4:
        st.markdown("**04. Ask**")
        st.caption("Retrieve relevant information and generate answers.")

    st.divider()

    st.markdown("### Recent Documents")

    if documents:

        for document in documents[:5]:

            name = get_document_name(document)
            status = document.get("status", "unknown")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"📄 {name}")

            with col2:
                if status == "processed":
                    st.success("Indexed")
                else:
                    st.warning(status.capitalize())

    else:
        st.info("No documents uploaded yet.")


# =========================================================
# DOCUMENT MANAGEMENT
# =========================================================

elif page == "Documents":

    st.markdown(
        '<p class="main-title">Document Management</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Upload, process and manage your documents</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="section-title">Upload Documents</p>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Choose your documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX and TXT"
    )

    if uploaded_files:

        st.write(
            f"**{len(uploaded_files)} file(s) selected**"
        )

        for file in uploaded_files:
            st.caption(f"📄 {file.name}")

        if st.button(
            "Upload and Index Documents",
            type="primary",
            use_container_width=True
        ):

            results = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            total_files = len(uploaded_files)

            for index, file in enumerate(uploaded_files):

                status_text.info(
                    f"Processing {file.name}..."
                )

                result = upload_and_index(file)

                results.append(result)

                progress_bar.progress(
                    (index + 1) / total_files
                )

            st.session_state.upload_results = results

            status_text.success(
                "Document processing completed."
            )

    # Display upload results

    if st.session_state.upload_results:

        st.divider()

        st.markdown("### Upload Results")

        for result in st.session_state.upload_results:

            if result["success"]:

                with st.container(border=True):

                    st.success(
                        f"{result['filename']} uploaded and indexed successfully."
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Document ID",
                        result["document_id"]
                    )

                    col2.metric(
                        "Extracted Characters",
                        result["extracted_text_length"]
                    )

                    col3.metric(
                        "Chunks Created",
                        result["chunks_created"]
                    )

            else:

                st.error(
                    f"{result['filename']}: {result['error']}"
                )

        if st.button("Clear Upload Results"):
            st.session_state.upload_results = []
            st.rerun()

    st.divider()

   
    # Stored documents

    st.markdown(
        '<p class="section-title">Stored Documents</p>',
        unsafe_allow_html=True
    )

    if st.button("Refresh Documents"):
        st.rerun()

    # Show deletion success message after refreshing
    if st.session_state.delete_success_message:
        st.success(st.session_state.delete_success_message)
        st.session_state.delete_success_message = None

    documents = get_documents()

    if documents:

        display_rows = []

        for document in documents:

            display_rows.append({
                "Document ID": get_document_id(document),
                "Filename": get_document_name(document),
                "File Type": document.get("file_type", "N/A"),
                "Status": document.get("status", "unknown"),
                "Created At": document.get("created_at", "N/A")
            })

        st.dataframe(
            display_rows,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------------------
        # DELETE DOCUMENT
        # -----------------------------------------

        st.divider()

        st.markdown("### Delete a Document")

        document_options = {
            f"{get_document_name(document)} (ID: {get_document_id(document)})":
                get_document_id(document)
            for document in documents
        }

        selected_document = st.selectbox(
            "Select a document to delete",
            options=list(document_options.keys()),
            key="delete_document_selection"
        )

        confirm_delete = st.checkbox(
            "I understand that this action permanently deletes the document.",
            key="confirm_document_deletion"
        )

        if st.button(
            "Delete Selected Document",
            type="primary",
            use_container_width=True,
            disabled=not confirm_delete,
            key="delete_document_button"
        ):

            document_id = document_options[selected_document]

            with st.spinner("Deleting document..."):

                result = delete_document_api(document_id)

            if result["success"]:

                st.session_state.delete_success_message = (
                    result["message"]
                )

                # Clear potentially outdated AI results
                st.session_state.last_query_result = None

                # Refresh the document list
                st.rerun()

            else:
                st.error(result["message"])

    else:
        st.info(
            "No documents available. Upload a document to get started."
        )


# =========================================================
# AI ASSISTANT
# =========================================================

elif page == "AI Assistant":

    st.markdown(
        '<p class="main-title">AI Document Assistant</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Ask questions and get answers from your documents</p>',
        unsafe_allow_html=True
    )

    documents = get_documents()

    indexed_documents = [
        document
        for document in documents
        if document.get("status") == "processed"
    ]

    if not indexed_documents:

        st.warning(
            "No indexed documents found. Please upload and index documents first."
        )

    else:

        st.markdown("### Select Knowledge Source")

        source_option = st.radio(
            "Search documents",
            [
                "All Indexed Documents",
                "Select Specific Documents"
            ],
            horizontal=True
        )

        selected_documents = []

        if source_option == "Select Specific Documents":

            document_options = {
                (
                    f"{get_document_name(document)} "
                    f"(ID: {get_document_id(document)})"
                ): document
                for document in indexed_documents
            }

            selected_names = st.multiselect(
                "Choose documents",
                options=list(document_options.keys())
            )

            selected_documents = [
                document_options[name]
                for name in selected_names
            ]

        st.divider()

        st.markdown("### Ask a Question")

        query = st.text_area(
            "Enter your question",
            placeholder="Example: What technologies are used in this project?",
            height=100
        )

        if st.button(
            "Generate Answer",
            type="primary",
            use_container_width=True
        ):

            if not query.strip():

                st.warning("Please enter a question.")

            elif (
                source_option == "Select Specific Documents"
                and not selected_documents
            ):

                st.warning("Please select at least one document.")

            else:

                with st.spinner(
                    "Searching documents and generating an answer..."
                ):

                    result = ask_question(
                        query.strip(),
                        selected_documents
                    )

                    if result:
                        st.session_state.last_query_result = result

        # Display latest answer

        result = st.session_state.last_query_result

        if result:

            st.divider()

            st.markdown("### AI Generated Answer")

            # Render answer as Markdown, not unsafe HTML.
            st.markdown(
                result.get(
                    "answer",
                    "No answer returned."
                )
            )

            sources = result.get("sources", [])

            if sources:

                st.divider()

                st.markdown("### Retrieved Sources")

                for index, source in enumerate(sources, start=1):

                    with st.container(border=True):

                        document_id = source.get(
                            "document_id",
                            "N/A"
                        )

                        score = source.get(
                            "score",
                            None
                        )

                        st.markdown(
                            f"**Source {index} — Document ID: {document_id}**"
                        )

                        if score is not None:
                            st.caption(
                                f"Similarity Score: {score:.4f}"
                            )

                        st.write(
                            source.get(
                                "chunk",
                                "No source text available."
                            )
                        )

            else:
                st.info("No source information returned.")

            searched_ids = result.get(
                "searched_document_ids"
            )

            if searched_ids:
                st.caption(
                    f"Searched documents: {searched_ids}"
                )
