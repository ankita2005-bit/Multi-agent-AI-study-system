from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

import random
import json

load_dotenv()


def generate_quiz(docs):

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)

    chunks = splitter.split_documents(docs)

    # select chunks only for quiz
    selected = random.sample(chunks, min(8, len(chunks)))

    context = "\n\n".join(c.page_content for c in selected)

    prompt = f"""
Generate exactly 5 MCQs.

Return JSON.

[
 {{
  "question":"",
  "options":["","","",""],
  "answer":""
 }}
]

Notes:
{context}
"""

    try:

        response = llm.invoke(prompt)

        text = response.content

        start = text.find("[")

        end = text.rfind("]") + 1

        return json.loads(text[start:end])

    except:

        return []
