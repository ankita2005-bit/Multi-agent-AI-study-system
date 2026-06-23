import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

VECTOR_DB_PATH = "vectordb"


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vector_db(docs):

    embeddings = get_embeddings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250,
        separators=["\n\n", "\n", ".", " "],
    )

    chunks = splitter.split_documents(docs)

    print(f"Chunks Created: {len(chunks)}")

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
    )

    print("Vector DB ready.")

    return db


def load_vector_db():

    embeddings = get_embeddings()

    if not os.path.exists(VECTOR_DB_PATH):

        return None

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
    )
