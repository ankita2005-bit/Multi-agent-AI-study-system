import streamlit as st
import os
import sys



ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT not in sys.path:
    sys.path.insert(
        0,
        ROOT
    )




from rag.loader import load_document
from rag.embed import build_vector_db

from agents.summary_agent import generate_summary
from agents.explanation_agent import explain_document
from agents.quiz_agent import generate_quiz
from agents.flashcard_agent import generate_flashcards
from agents.chat_agent import (
    build_chat,
    ask_question
)

from utils.image_extractor import (
    extract_images
)




st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)



st.markdown("""
<style>

.block-container{
padding-top:2rem;
}

.hero{
padding:35px;

border-radius:18px;

background:
linear-gradient(
135deg,
#EEF2FF,
#FFFFFF
);

margin-bottom:25px;
}

.stButton>button{

width:100%;

height:48px;

border-radius:12px;

background:#5B6CFF;

color:white;

border:none;

font-size:15px;

}

.stButton>button:hover{

background:#4B59F0;

}

</style>
""",
unsafe_allow_html=True)




st.markdown(
"""
<div class='hero'>

<h1>StudyMate AI</h1>

<p>
Upload notes → Summarize → Explain →
Quiz → Flashcards → Chat
</p>

</div>
""",
unsafe_allow_html=True
)




uploaded = st.file_uploader(
    "Upload PDF / DOCX",
    type=[
        "pdf",
        "docx"
    ]
)




if uploaded:

    os.makedirs(
        "temp",
        exist_ok=True
    )

    path = os.path.join(
        "temp",
        uploaded.name
    )

    with open(
        path,
        "wb"
    ) as f:

        f.write(
            uploaded.getbuffer()
        )

    try:

        with st.spinner(
            "Preparing notes..."
        ):

            docs = load_document(
                path
            )

            db = build_vector_db(
                docs
            )

            images = extract_images(
                path
            )

        st.success(
            "Document Ready"
        )

        c1, c2, c3 = st.columns(
            3
        )

        with c1:

            st.metric(
                "Pages",
                len(docs)
            )

        with c2:

            st.metric(
                "Images",
                len(images)
            )

        with c3:

            st.metric(
                "Status",
                "Ready"
            )

        st.divider()

        action = st.selectbox(

            "Choose Mode",

            [

                "Summary",

                "Explanation",

                "Quiz",

                "Flashcards",

                "Chat"

            ]

        )

        

        if action == "Summary":

            if st.button(
                "Generate Summary"
            ):

                output = (
                    generate_summary(
                        docs
                    )
                )

                st.markdown(
                    output
                )

                if images:

                    st.subheader(
                        "Images From Notes"
                    )

                    for img in images:

                        st.image(
                            img,
                            use_container_width=True
                        )

        

        elif action == "Explanation":

            if st.button(
                "Explain Notes"
            ):

                output = (
                    explain_document(
                        docs
                    )
                )

                st.markdown(
                    output
                )

                if images:

                    st.subheader(
                        "📷 Reference Images"
                    )

                    for img in images:

                        st.image(
                            img,
                            use_container_width=True
                        )

      

        elif action == "Quiz":

            if st.button(
                "Generate Quiz"
            ):

                st.session_state.quiz = (
                    generate_quiz(
                        docs
                    )
                )

            if (
                "quiz"
                in st.session_state
                and
                st.session_state.quiz
            ):

                score = 0

                answers = []

                for i, q in enumerate(
                    st.session_state.quiz
                ):

                    st.write(
                        f"### Q{i+1}"
                    )

                    selected = st.radio(
                        q["question"],
                        q["options"],
                        key=f"quiz{i}"
                    )

                    answers.append(
                        selected
                    )

                if st.button(
                    "Submit Quiz"
                ):

                    for i, q in enumerate(
                        st.session_state.quiz
                    ):

                        if (
                            answers[i]
                            ==
                            q["answer"]
                        ):

                            score += 1

                    st.success(
                        f"Score: {score}/5"
                    )

        # ===================
        # FLASHCARDS
        # ===================

        elif action == "Flashcards":

            if st.button(
                "Generate Flashcards"
            ):

                st.session_state.cards = (
                    generate_flashcards(
                        docs
                    )
                )

            if (
                "cards"
                in st.session_state
            ):

                for card in (
                    st.session_state.cards
                ):

                    with st.expander(
                        card["front"]
                    ):

                        st.write(
                            card["back"]
                        )

        # ===================
        # CHAT
        # ===================

        elif action == "Chat":

            if (
                "chat"
                not in st.session_state
            ):

                st.session_state.chat = (
                    build_chat(
                        db
                    )
                )

            question = st.chat_input(
                "Ask your notes"
            )

            if question:

                st.chat_message(
                    "user"
                ).write(
                    question
                )

                answer, sources = (

                    ask_question(

                        st.session_state.chat,

                        question

                    )
                )

                st.chat_message(
                    "assistant"
                ).write(
                    answer
                )

                with st.expander(
                    "Sources"
                ):

                    for s in sources:

                        st.caption(
                            s
                        )

    except Exception as e:

        st.error(
            str(e)
        )