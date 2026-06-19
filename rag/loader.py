import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader
)


def load_document(file_path):

    ext = os.path.splitext(
        file_path
    )[1].lower()

    if ext == ".pdf":

        loader = PyPDFLoader(
            file_path
        )

    elif ext == ".docx":

        loader = Docx2txtLoader(
            file_path
        )

    else:

        raise ValueError(
            "Only PDF and DOCX supported"
        )

    docs = loader.load()

    return docs