from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def generate_summary(docs):

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2
    )

    context = ""

    for page in docs:
        context += page.page_content + "\n\n"

    context = context[:15000]

    prompt = f"""
You are an AI Study Assistant.

Generate concise study notes.

Document:
{context}

Format:

# Overview

# Main Concepts

# Key Definitions

# Revision Notes
"""

    response = llm.invoke(
        prompt
    )

    return response.content