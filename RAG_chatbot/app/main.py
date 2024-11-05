from pydantic import BaseModel, Field
from fastapi import UploadFile
from app.file_loader import Loader
from app.vectorstore import VectorDB
from app.offline_rag import Offilne_RAG
import os
from dotenv import load_dotenv
import datetime
from io import BytesIO

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
class InputQA(BaseModel):
    question: str = Field(..., title="Question to ask the model")

class OutputQA(BaseModel):
    answer: str = Field(..., title="Answer from the model")

def load_new_pdf(data_dir, data_type: str = "pdf"):
    loader = Loader(file_type=data_type)
    doc_loaded = loader.load_dir(data_dir, workers=4)
    for doc in doc_loaded:
        if not doc.metadata:
            doc.metadata = {}
        if 'filename' not in doc.metadata:
            doc.metadata['filename'] = os.path.basename(doc.metadata.get('source', 'Unknown'))
        if 'upload_date' not in doc.metadata:
            doc.metadata['upload_date'] = datetime.datetime.now().isoformat()
    vectorstore = VectorDB(documents= doc_loaded, persist_directory=data_dir)
    return vectorstore

async def load_new_pdfs(data_dir,uploadfile :UploadFile):
    file_content = await  uploadfile.read()
    pdf_file_stream = BytesIO(file_content)
    loader = Loader(file_type="pdf")
    doc_loaded = loader.load(pdf_file_stream, workers=4)

    for doc in doc_loaded:
        if not doc.metadata:
            doc.metadata = {}
        if 'filename' not in doc.metadata:
            doc.metadata['filename'] = os.path.basename(doc.metadata.get('source', 'Unknown'))
        if 'upload_date' not in doc.metadata:
            doc.metadata['upload_date'] = datetime.datetime.now().isoformat()

    vectorstore = VectorDB(documents= doc_loaded, persist_directory=data_dir)
    vectorstore.save_db(data_dir)
    vector = vectorstore.print_metadata()
    return vector

def delete_file_by_metadata(data_dir, filename):
    vectordb = VectorDB(persist_directory= data_dir)
    print(vectordb.print_all_metadatas())
    return vectordb.delete_metadata(key= "filename", value = filename)

def get_metadata(data_dir):
    vectordb = VectorDB(persist_directory= data_dir)
    return vectordb.print_metadata()

def build_rag_chain(llm, data_dir, use_reranking= True):
    #doc_loaded = Loader(file_type= data_type).load_dir(data_dir, workers = 2)
    #retriever = VectorDB(documents= doc_loaded, cohere_api_key= "2cCcS01i5dbGhJj65J8WwGpuqM4Y9fq7gqBnxex8", persist_directory=data_dir).get_retriever(rerank= use_reranking)
    #retriever = VectorDB(documents= doc_loaded).get_retriever()
    retriever = VectorDB( persist_directory=data_dir, cohere_api_key= cohere_api_key).get_retriever()
    print("Retrivers: ", retriever)
    rag_chain = Offilne_RAG(llm).get_chain(retriever)
    return rag_chain 
