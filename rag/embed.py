from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_chroma import (
    Chroma
)


def build_vector_db(docs):

  

    splitter = (
        RecursiveCharacterTextSplitter(

            chunk_size=1200,

            chunk_overlap=250,

            separators=[
                "\n\n",
                "\n",
                ".",
                " "
            ]
        )
    )

    chunks = splitter.split_documents(
        docs
    )

    print(
        f"Chunks Created: {len(chunks)}"
    )

   

    embeddings = (
        HuggingFaceEmbeddings(

            model_name=
            "sentence-transformers/all-MiniLM-L6-v2",

            model_kwargs={

                "device":
                "cpu"

            },

            encode_kwargs={

                "normalize_embeddings":
                True

            }
        )
    )


    db = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings

    )

    return db