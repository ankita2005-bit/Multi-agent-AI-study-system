from dotenv import load_dotenv
from langchain_groq import ChatGroq
import json

load_dotenv()


def generate_flashcards(docs):

    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.4)

    context = ""

    for page in docs:

        context += page.page_content + "\n\n"

    context = context[:10000]

    prompt = f"""
Create study flashcards.

Return ONLY JSON.

Format:

[
 {{
   "front":"Question",
   "back":"Answer"
 }}
]

Generate EXACTLY 10 cards.

Document:

{context}
"""

    response = llm.invoke(prompt)

    content = response.content

    try:

        if isinstance(content, list):
            return content

        content = str(content).replace("```json", "").replace("```", "").strip()

        return json.loads(content)

    except:

        return [{"front": "Flashcards unavailable", "back": "Retry"}]
