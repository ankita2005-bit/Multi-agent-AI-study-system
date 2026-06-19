# StudyMate AI — Multi-Agent AI Study Assistant

StudyMate AI is an intelligent **multi-agent learning platform** that transforms uploaded study materials into an interactive and personalized study experience.

Users can upload **PDF or DOCX documents**, and the system automatically processes content using **Retrieval-Augmented Generation (RAG)**, **LangChain**, **ChromaDB**, and **LLMs** to generate summaries, explanations, quizzes, flashcards, and contextual document chat.

Designed to move beyond static notes and create a smarter way to learn.

---

## Features

### Smart Document Understanding

* Upload **PDF** and **DOCX** study materials
* Automatic text extraction and processing
* Supports extraction and display of visual content from documents

### AI Summary Agent

* Generates concise summaries from entire notes
* Captures key concepts and important takeaways
* Optimized for long documents

### Explanation Agent

* Converts complex content into simplified explanations
* Provides student-friendly learning support
* Generates structured explanations from uploaded notes

### Interactive Quiz Agent

* Generates **MCQ-based quizzes**
* Interactive answer selection
* Instant score evaluation

### Flashcard Agent

* Converts study notes into revision flashcards
* Reveal-answer interaction for active recall learning

### Chat With Notes (RAG)

* Ask questions directly from uploaded documents
* Context-aware retrieval using vector search
* Source-based responses from uploaded content

### Visual Learning Support

* Displays extracted visuals from uploaded documents
* Supports:

  * PDF page rendering
  * DOCX embedded image extraction

---

## System Architecture

```plaintext
User Upload
     ↓
Document Loader
(PDF / DOCX)
     ↓
Text + Image Extraction
     ↓
Chunking
     ↓
Embedding Generation
(HuggingFace)
     ↓
Chroma Vector Database
     ↓
Multi-Agent Layer
 ├── Summary Agent
 ├── Explanation Agent
 ├── Quiz Agent
 ├── Flashcard Agent
 └── Chat Agent (RAG)
     ↓
Interactive Study Experience
```

---

## Tech Stack

### Frontend

* Streamlit

### AI & LLM

* LangChain
* Groq API
* HuggingFace Embeddings

### RAG Pipeline

* ChromaDB
* Recursive Character Text Splitting

### Document Processing

* PyMuPDF
* Python-DOCX

### Infrastructure

* Docker
* Docker Compose

---

## Project Structure

```plaintext
study-ai/
│
├── frontend/
│   └── app.py
│
├── agents/
│   ├── summary_agent.py
│   ├── explanation_agent.py
│   ├── quiz_agent.py
│   ├── flashcard_agent.py
│   └── chat_agent.py
│
├── rag/
│   ├── loader.py
│   └── embed.py
│
├── utils/
│   └── image_extractor.py
│
├── temp/
├── vectordb/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-url>
cd study-ai
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

### Run Locally

```bash
streamlit run frontend/app.py
```

Open:

```plaintext
http://localhost:8501
```

---

## 🐳 Run With Docker

### Build

```bash
docker compose build
```

### Start

```bash
docker compose up
```

Open:

```plaintext
http://localhost:8501
```

Stop:

```bash
docker compose down
```



## Project Vision

To create an AI-powered study companion that transforms traditional notes into an **interactive, visual, and personalized learning experience** through multi-agent AI systems.

---

