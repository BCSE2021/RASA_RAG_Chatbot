from typing import Union, Optional, List
#from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.schema import Document
import os
import datetime
import chromadb

# class VectorDB:
#     def __init__(self, documents=None, vector_db: Union[Chroma, FAISS] = Chroma, embedding=HuggingFaceBgeEmbeddings(), cohere_api_key: str = None) -> None:
#         self.vector_db = vector_db
#         self.embedding = embedding
#         self.db = self._build_db(documents)

#         if cohere_api_key:
#             os.environ["COHERE_API_KEY"] = cohere_api_key

#         try:
#             self.cohere_reranker = CohereRerank()
#         except Exception as e:
#             print(f"Error initializing CohereRerank: {e}")
#             self.cohere_reranker = None

#     def _build_db(self, documents):
#         db = self.vector_db.from_documents(documents=documents, embedding=self.embedding)
#         return db
    
#     def get_retriever(self, search_type: str = "similarity", search_kwargs: dict = {"k": 10}, rerank: bool = False):
#         retriever = self.db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)

#         if rerank and self.cohere_reranker:
#             compression_retriever = ContextualCompressionRetriever(
#                 base_compressor=self.cohere_reranker,  
#                 base_retriever=retriever  
#             )
#             return compression_retriever
#         else:
#             return retriever

# vectorstore.py


class VectorDB:
    def __init__(
        self,
        collection_name = "my_collection",
        documents: Optional[List[Document]] = None,
        vector_db: Union[Chroma, FAISS] = Chroma,
        embedding: Optional[HuggingFaceBgeEmbeddings] = None,
        cohere_api_key: Optional[str] = None,
        persist_directory: Optional[str] = None,
        document_directory: Optional[str] = None
    ) -> None:
        self.vector_db = vector_db
        self.embedding = embedding or HuggingFaceBgeEmbeddings()
        self.persist_directory = persist_directory 
        self.document_directory = document_directory
        if self.persist_directory and os.path.exists(self.persist_directory):
            self.db = self._load_db(self.persist_directory)
            print(f"Loaded vector database from {self.persist_directory}.")
            if documents:
                self.add_documents(documents)
        else:
            if documents:
                self.db = self._build_db(documents,self.persist_directory)
                self.add_documents(documents)
                self.print_all_metadatas()
                print("Built new vector database from provided documents.")
                #self.save_db(self.persist_directory)
                print(f"Persisted vector database to {self.persist_directory}.")
            else:
                raise ValueError("No documents provided and persist directory does not exist.")

        if cohere_api_key:
            os.environ["COHERE_API_KEY"] = cohere_api_key

        try:
            self.cohere_reranker = CohereRerank(model="rerank-medium")
        except Exception as e:
            print(f"Error initializing CohereRerank: {e}")
            self.cohere_reranker = None
        
    def _build_db(self, documents: List[Document], persist_directory):
        db = self.vector_db.from_documents(documents=documents, embedding=self.embedding, persist_directory=persist_directory)
        return db

    def _load_db(self, directory: str):
        if self.vector_db is Chroma:
            db = Chroma(persist_directory=directory, embedding_function=self.embedding)
        elif self.vector_db is FAISS:
            db = FAISS.load_local(directory, self.embedding)
        else:
            raise ValueError("Unsupported vector_db type. Use Chroma or FAISS.")
        return db


    def save_db(self, directory: Optional[str] = None):
        directory = directory or self.persist_directory
        self.db.persist()

    def get_retriever(
        self,
        search_type: str = "similarity",
        search_kwargs: dict = {"k": 10},
        rerank: bool = False
    ):
        retriever = self.db.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
        if rerank and self.cohere_reranker:
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=self.cohere_reranker,
                base_retriever=retriever
            )
            return compression_retriever
        else:
            return retriever

    def add_documents(self, new_documents: List[Document]):
        #for doc in new_documents:
            #print(f"Adding document with metadata: {doc.metadata}")
        self.db.add_documents(new_documents, embedding=self.embedding, include_metadata=True)
        print(f"Added {len(new_documents)} documents and persisted updates to {self.persist_directory}.")


    def delete_metadata(self, key: str, value: str):
    # Search for the documents matching the metadata using the `where` condition
        result = self.db._collection.get(where={key: value})  # Search documents where metadata matches key-value

        ids_to_delete = []
    
        # Check if any documents were found
        if result and 'ids' in result:
            ids_to_delete = result['ids']  # This is a list of IDs to delete
        
        # Perform the deletion only if there are matching IDs
        if ids_to_delete:
            self.db._collection.delete(ids=ids_to_delete)
            print(f"Deleted {len(ids_to_delete)} documents where {key} = {value}.")
            return True
        else:
            print(f"No documents found with metadata {key} = {value}.")
            return False
        
    def print_all_metadatas(self):
    # Retrieve all documents from the database
        result = self.db.get(include=['metadatas'])
        print(f"Retrieved result: {result}")
        metadatas_list = []
    # Check if any metadata is present
        if result and 'metadatas' in result:
            for idx, metadata in enumerate(result['metadatas']):
                print (f"Document {idx + 1}: {metadata}")
                metadatas_list.append(metadata)
            return metadatas_list
        else:
            print ("No metadata found.")
            return []
        
    def print_metadata(self):
        result = self.db.get(include=['metadatas'])
        filenames_set = set() 
        if result and 'metadatas' in result:
            for metadata in result['metadatas']:
                # Kiểm tra nếu metadata chứa "filename"
                if 'filename' in metadata:
                    filenames_set.add(metadata['filename'])  # Thêm vào set (đảm bảo không lặp)
        
        if filenames_set:
            print("List of unique filenames in the database:")
            for idx, filename in enumerate(filenames_set, start=1):
                print(f"{idx}. {filename}")
        else:
            print("No filenames found in metadata.")

        return list(filenames_set)
