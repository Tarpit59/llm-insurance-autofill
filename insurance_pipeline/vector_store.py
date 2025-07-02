from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from pinecone import ServerlessSpec
import pinecone
from insurance_pipeline.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(docs)
    print("Documents split into chunks.")
    return chunks

def initialize_pinecone(api_key, index_name, dimension=768, metric='cosine', cloud='aws', region='us-east-1'):
    try:
        pc = pinecone.Pinecone(api_key=api_key)
        if index_name in pc.list_indexes().names():
            pc.delete_index(index_name)
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region)
        )
        print(f"Pinecone index '{index_name}' created successfully.")
    except Exception as e:
        print(f"Error initializing Pinecone: {e}")

def create_vector_store(documents, embeddings, index_name):
    try:
        index = Pinecone.from_documents(documents, embeddings, index_name=index_name)
        print("Vector store created successfully.")
        return index
    except Exception as e:
        print(f"Error creating vector store: {e}")
        raise
