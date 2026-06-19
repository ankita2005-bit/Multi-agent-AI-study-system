from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def build_chat(db):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2
    )

    return {

        "db": db,

        "llm": llm,

        "history": []

    }


def ask_question(
    chat,
    question
):

    db = chat["db"]

    llm = chat["llm"]

    # retrieve more chunks
    docs = db.similarity_search(

        question,

        k=12

    )

    # fallback:
    if len(docs) < 4:

        docs += db.similarity_search(

            "summary main topics",

            k=8
        )

    # remove duplicates
    seen = set()

    unique = []

    for d in docs:

        text = d.page_content

        if text not in seen:

            seen.add(text)

            unique.append(text)

    context = "\n\n".join(
        unique
    )

    context = context[:18000]

    history = "\n".join(
        chat["history"][-6:]
    )

    prompt = f"""
You are an AI study tutor.

Answer ONLY using uploaded notes.

Rules:
- Use information from multiple sections.
- If answer exists indirectly, infer carefully.
- Do not summarize unless asked.
- Answer in teaching style.
- If not found say:
"I could not find this in the uploaded notes."

Conversation:
{history}

Study Material:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(
        prompt
    )

    answer = response.content

    chat["history"].append(
        f"User: {question}"
    )

    chat["history"].append(
        f"Assistant: {answer}"
    )

    sources = []

    for d in unique[:5]:

        sources.append(
            d[:300]
        )

    return (

        answer,

        sources
    )