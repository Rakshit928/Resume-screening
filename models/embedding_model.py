import chromadb
from sentence_transformers import SentenceTransformer
import os
from django.conf import settings

# Load Sentence Transformer model for embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=settings.CHROMADB_PATH)
collection = chroma_client.get_or_create_collection(name="resume_store")

def store_embedding(doc_id, text):
    """Generate embedding and store in ChromaDB"""
    embedding = embedder.encode(text).tolist()
    collection.add(ids=[doc_id], embeddings=[embedding], metadatas=[{"text": text}])

def retrieve_similar_resumes(query, top_k=3):
    """Retrieve top K similar resumes"""
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["metadatas"][0] if results["metadatas"] else []
