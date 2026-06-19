from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def explain_document(docs):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

    context = ""

    for page in docs:
        context += page.page_content + "\n\n"

    context = context[:15000]

    prompt = f"""
You are an expert tutor.

Explain the ENTIRE uploaded document.

Format:

# Overview

# Detailed Explanation

# Examples

# Important Concepts

# Revision Notes

Document:

{context}
"""

    response = llm.invoke(
        prompt
    )

    return response.content