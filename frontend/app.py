import streamlit as st
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from rag.loader import load_document
from rag.embed import build_vector_db

from agents.summary_agent import generate_summary
from agents.explanation_agent import explain_document
from agents.quiz_agent import generate_quiz
from agents.flashcard_agent import generate_flashcards
from agents.chat_agent import build_chat, ask_question

from utils.image_extractor import extract_images

st.set_page_config(page_title="StudyMate AI", layout="wide")


# ---------- UI ----------
st.markdown(
    """
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
}

</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<div class='hero'>

<h1>StudyMate AI</h1>

<p>
Upload → Summary → Explain →
Quiz → Flashcards → Chat
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ---------- SESSION ----------
if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "db" not in st.session_state:
    st.session_state.db = None

if "chat" not in st.session_state:
    st.session_state.chat = None


uploaded = st.file_uploader("Upload PDF / DOCX", type=["pdf", "docx"])


if uploaded:

    # detect NEW upload
    new_upload = st.session_state.current_file != uploaded.file_id

    if new_upload:

        os.makedirs("temp", exist_ok=True)

        path = os.path.join("temp", uploaded.name)

        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())

        with st.spinner("Preparing notes..."):

            docs = load_document(path)

            db = build_vector_db(docs)

            images = extract_images(path)

        # overwrite EVERYTHING
        st.session_state.current_file = uploaded.file_id

        st.session_state.docs = docs

        st.session_state.db = db

        st.session_state.chat = build_chat(db)

        st.session_state.quiz = None

        st.session_state.cards = None

        st.session_state.images = images

        st.success("New document loaded")

    docs = st.session_state.docs
    db = st.session_state.db
    images = st.session_state.images

    st.divider()

    action = st.selectbox(
        "Choose Mode", ["Summary", "Explanation", "Quiz", "Flashcards", "Chat"]
    )

    # ---------- SUMMARY ----------
    if action == "Summary":

        if st.button("Generate Summary"):

            st.markdown(generate_summary(docs))

    # ---------- EXPLAIN ----------
    elif action == "Explanation":

        if st.button("Explain Notes"):

            st.markdown(explain_document(docs))

    # ---------- QUIZ ----------
    elif action == "Quiz":

        if st.button("Generate Quiz"):

            st.session_state.quiz = generate_quiz(docs)

        if st.session_state.quiz:

            score = 0

            answers = []

            for i, q in enumerate(st.session_state.quiz):

                selected = st.radio(q["question"], q["options"], key=f"q{i}")

                answers.append(selected)

            if st.button("Submit Quiz"):

                for i, q in enumerate(st.session_state.quiz):

                    if answers[i] == q["answer"]:
                        score += 1

                st.success(f"Score: {score}/5")

    # ---------- FLASHCARDS ----------
    elif action == "Flashcards":

        if st.button("Generate Flashcards"):

            st.session_state.cards = generate_flashcards(docs)

        if st.session_state.cards:

            for c in st.session_state.cards:

                with st.expander(c["front"]):

                    st.write(c["back"])

    # ---------- CHAT ----------
    elif action == "Chat":

        question = st.chat_input("Ask your notes")

        if question:

            st.chat_message("user").write(question)

            answer, sources = ask_question(st.session_state.chat, question)

            st.chat_message("assistant").write(answer)

            if sources:

                with st.expander("Sources"):

                    for s in sources:

                        st.caption(s)

    # ---------- IMAGES ----------
    if images:

        st.divider()

        st.subheader("Images")

        for img in images:

            st.image(img, use_container_width=True)
