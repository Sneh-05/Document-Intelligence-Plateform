# NEXOR – Document Intelligence Platform

**An AI-powered platform for intelligent document processing, semantic search, and question answering using Retrieval-Augmented Generation (RAG).**

NEXOR is a Document Intelligence Platform that allows users to upload multiple documents, extract their content, and ask questions using natural language. It retrieves relevant information from uploaded documents through semantic search and generates context-aware answers using an LLM.

The platform combines **FastAPI, Streamlit, Sentence Transformers, FAISS, SQLite, and an LLM API** to provide an intelligent document question-answering experience.

---

## Key Features

- **Multi-format Document Upload:** Upload PDF, DOCX, and TXT files.
- **Text Extraction:** Automatically extract text from uploaded documents.
- **Document Management:** View, manage, and delete uploaded documents.
- **Automatic Indexing:** Process uploaded documents and convert their content into searchable chunks.
- **Semantic Search:** Retrieve relevant document content using Sentence Transformers and FAISS.
- **Multi-document RAG:** Ask questions across all indexed documents or select specific documents.
- **AI-powered Question Answering:** Generate context-aware answers using an LLM API.
- **Source Tracking:** View the source documents and similarity scores associated with retrieved information.
- **Context-aware Responses:** Avoid unsupported answers when the requested information is not available in indexed documents.
- **Interactive Dashboard:** Monitor document statistics and backend status through a Streamlit interface.

---

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python, FastAPI |
| API Communication | REST APIs |
| Document Processing | PyPDF, python-docx |
| Text Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database / Search | FAISS |
| Metadata Storage | SQLite |
| LLM Integration | Coforge LLM Router API |
| Version Control | Git and GitHub |

---

## System Architecture

The platform follows a Retrieval-Augmented Generation (RAG) workflow.

1. **Document Upload:** Users upload PDF, DOCX, or TXT documents through the frontend.
2. **Text Extraction:** The backend extracts textual content from the uploaded files.
3. **Text Chunking:** Extracted text is divided into smaller, overlapping chunks.
4. **Embedding Generation:** Sentence Transformers converts the chunks into numerical vector embeddings.
5. **Vector Indexing:** FAISS stores the embeddings and enables similarity-based retrieval.
6. **Question Processing:** The user's question is converted into an embedding.
7. **Semantic Retrieval:** FAISS retrieves the most relevant chunks from the selected indexed documents.
8. **Answer Generation:** The retrieved context is passed to the LLM, which generates a context-aware response.
9. **Source Display:** The frontend displays the generated answer along with its source documents.

---

## Project Structure

```text
Document-Intelligence-Plateform/
│
├── backend/
│   ├── app/
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   │
│   │   ├── services/
│   │   │   ├── chunker.py
│   │   │   ├── embedder.py
│   │   │   ├── vector_store.py
│   │   │   ├── rag_pipeline.py
│   │   │   └── llm.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   └── document_processor.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── app.py
│
├── database/
│   └── documents.db
│
├── uploaded_documents/
│
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10 or later
- Git
- VS Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Sneh-05/Document-Intelligence-Plateform.git
```

```bash
cd Document-Intelligence-Plateform
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Add your LLM API configuration:

```env
API_URL=your_llm_api_endpoint
MODEL_NAME=your_model_name
API_KEY=your_api_key
```

**Important:** Replace the placeholder values with your actual API credentials. Never commit your `.env` file or expose API keys publicly.

### 5. Start the Backend

From the `backend` directory, run:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Frontend

Open another terminal from the project root, activate the virtual environment, and run:

```bash
streamlit run frontend/app.py
```

The frontend will open in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome endpoint |
| GET | `/health` | Check backend health |
| POST | `/upload` | Upload and extract document content |
| GET | `/documents` | Retrieve all stored documents |
| POST | `/documents/{document_id}/index` | Index a document for semantic search |
| POST | `/query` | Ask questions using RAG |
| DELETE | `/documents/{document_id}` | Delete a document |

### Example: Query Request

```json
{
  "query": "What is the purpose of this document?",
  "document_ids": [1, 2]
}
```

To search across all indexed documents, provide the query without a document ID or document ID list.

---

## Important Implementation Notes

- Document metadata is stored in SQLite.
- Uploaded original files are stored in the `uploaded_documents` directory.
- FAISS currently maintains vector indexes in memory. The vector index is rebuilt through document indexing after a backend restart.
- The LLM generates responses using the retrieved document context.
- Only indexed documents are available for question answering.

---

## Contributors

| Name | Role |
|---|---|
| **Sneha** | Team Lead |
| **Sandli** | Contributor |
| **Archita** | Contributor |

---

## Future Enhancements

- Persistent FAISS vector storage.
- Support for additional document formats.
- Improved document summarization.
- Advanced conversational memory.
- User authentication and role-based access.
- Enhanced retrieval and ranking strategies.
- Cloud deployment and scalability.

---

## License

This project is developed for educational and learning purposes. Licensing terms can be added as the project evolves.

---

**NEXOR – Making Documents Intelligent.**
