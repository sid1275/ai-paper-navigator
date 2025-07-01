# 📄 AI Paper Navigator

An intelligent document Q&A application that allows you to have a conversation with your PDF files. This project uses a Retrieval-Augmented Generation (RAG) pipeline, leveraging local embeddings for privacy and cost-effectiveness, and a powerful open-source LLM for generating accurate answers.

![Demo GIF](https://github.com/sid1275/ai-paper-navigator/blob/main/assets/demo.gif?raw=true)


---

## 🚀 Features

-   **PDF Text Extraction:** Ingests any PDF document and extracts its text content.
-   **Local & Private Embeddings:** Uses `sentence-transformers` to generate text embeddings locally on your machine. No data is sent to external services for embedding.
-   **Efficient Retrieval:** Creates a `ChromaDB` vector store for fast and semantic searching of relevant document chunks.
-   **Advanced Q&A:** Utilizes a powerful Large Language Model (LLM) via the Groq API for generating high-quality, context-aware answers.
-   **Modular Code:** Written in clean, modular Python, making it easy to extend and maintain.

---

## 🛠️ Tech Stack

-   **Backend:** Python
-   **AI / ML:**
    -   **Orchestration:** LangChain
    -   **LLM Provider:** Groq (Llama 3)
    -   **Embeddings:** Hugging Face `sentence-transformers` (all-MiniLM-L6-v2)
    -   **Vector Store:** ChromaDB
-   **Core Libraries:** `pypdf`, `python-dotenv`

---

## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/ai-paper-navigator.git
    cd ai-paper-navigator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: We will create the `requirements.txt` file in a later step).*

4.  **Set up environment variables:**
    -   Create a file named `.env` in the root of the project.
    -   Add your Groq API key to it:
    ```
    GROQ_API_KEY="gsk_YourGroqApiKeyGoesHere"
    ```

---

## Usage

1.  Place the PDF you want to query inside the `documents` folder.
2.  Update the `pdf_file_path` variable in `main.py` to point to your PDF.
3.  Run the main script:
    ```bash
    python main.py
    ```
4.  The script will process the PDF and print the answer to the hard-coded question.

---

## 🗺️ Roadmap: Future Work

This is the foundation of a larger application. The next steps are:

-   [ ] **Interactive CLI:** Allow users to ask questions continuously in the terminal.
-   [ ] **FastAPI Backend:** Refactor the code into a robust REST API.
-   [ ] **React Frontend:** Build a user-friendly web interface for uploading PDFs and chatting.
-   [ ] **Conversation Memory:** Implement a system to remember the chat history for follow-up questions.
-   [ ] **Source Highlighting:** Show which parts of the document were used to generate the answer.