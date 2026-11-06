from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI()

@app.get("/")      #root endpoint
def home():
    return {
        "message": "Welcome to NEXOR",
        "project": "Document Intelligence Platform",
        "status": "Running"
    }

@app.get("/health")           #a way to check whether their backend application is running
def health_check():
    return {
        "status": "healthy",
        "application": "NEXOR"
    }

@app.get("/documents")       #this endpoint will retrieve actual document records from our database
def get_documents():
    return {
        "documents": []
    }

class DocumentCreate(BaseModel):  #This pydantic model defines what the API accepts. 
    title: str = Field(min_length=3, max_length=100)  #Adds validation rules
    file_type: Literal["pdf", "docx", "txt"]

class DocumentResponse(BaseModel): #This pydantic model defines what the API returns.
    id: int
    title: str
    file_type: str
    status: str


documents = []

@app.post("/documents",response_model=DocumentResponse,status_code=201)
def create_document(document: DocumentCreate):

    new_document = {
        "id": len(documents) + 1,
        "title": document.title,
        "file_type": document.file_type,
        "status": "uploaded",
        "internal_note": "This is a private backend field"  #will not be seen in the output 
    }

    documents.append(new_document)

    return new_document
