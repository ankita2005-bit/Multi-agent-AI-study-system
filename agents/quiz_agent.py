from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

load_dotenv()


def generate_quiz(docs):

    llm = ChatGroq(

        model="llama-3.1-8b-instant",

        temperature=0.3

    )

    content = "\n".join(

        [

            d.page_content

            for d in docs

        ]

    )

    content = content[:15000]

    prompt = f"""
Generate 5 MCQs.

Return ONLY JSON.

Format:

[
{{
"question":"",
"options":["A","B","C","D"],
"answer":"",
"explanation":""
}}
]

Content:

{content}
"""

    response = llm.invoke(
        prompt
    )

    text = (
        response.content
        .replace(
            "```json",
            ""
        )
        .replace(
            "```",
            ""
        )
        .strip()
    )

    try:

        quiz = json.loads(
            text
        )

        return quiz

    except:

        return [
            {
                "question":
                "Quiz generation failed",

                "options":
                [

                    "Retry"

                ],

                "answer":
                "Retry",

                "explanation":
                ""
            }
        ]