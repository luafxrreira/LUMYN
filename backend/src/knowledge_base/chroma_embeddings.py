import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_store(chunks=None):
    local_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    persist_directory = "src/knowledge_base/chroma_db"

    if chunks:
        return Chroma.from_texts(
            collection_name="lumyn_collection",
            embedding=local_embeddings,
            persist_directory=persist_directory,
            texts=chunks
        )

    return Chroma(
        collection_name="lumyn_collection",
        embedding_function=local_embeddings,
        persist_directory=persist_directory
    )