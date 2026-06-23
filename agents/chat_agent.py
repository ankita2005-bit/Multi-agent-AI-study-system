from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def build_chat(db):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
    )

    return {
        "db": db,
        "llm": llm,
        "history": [],
    }


def reset_chat(chat, new_db):

    chat["db"] = new_db

    chat["history"] = []

    return chat


def ask_question(chat, question):

    db = chat["db"]

    llm = chat["llm"]

    docs = db.similarity_search(
        question,
        k=12,
    )

    # fallback retrieval
    if len(docs) < 3:

        docs += db.similarity_search(
            "summary key concepts explanation",
            k=6,
        )

    if not docs:

        return (
            "I could not find this in the uploaded notes.",
            [],
        )

    seen = set()

    unique = []

    for d in docs:

        text = d.page_content.strip()

        if text and text not in seen:

            seen.add(text)

            unique.append(text)

    context = "\n\n".join(unique)

    context = context[:18000]

    history = "\n".join(chat["history"][-6:])

    prompt = f"""
You are an AI study tutor.

Rules:
- Use uploaded notes as primary source.
- If exact words are absent,
  use related context.
- Explain naturally.
- Infer carefully.
- Do not invent facts.
- If truly unavailable say:
"I could not find this in the uploaded notes."

Conversation:
{history}

Study Material:
{context}

Question:
{question}

Answer:
"""

    try:

        response = llm.invoke(prompt)

        answer = response.content

    except Exception:

        answer = "Generation failed."

    chat["history"].append(f"User: {question}")

    chat["history"].append(f"Assistant: {answer}")

    sources = []

    for d in unique[:5]:

        sources.append(d[:300])

    return (
        answer,
        sources,
    )
