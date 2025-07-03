# 📄 AI Paper Navigator 💡

An intelligent document Q&A application that allows you to have a conversation with your PDF files. This project uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware answers with **highlighted sources** from the original document.

![Demo GIF](https://raw.githubusercontent.com/YourUsername/ai-paper-navigator/main/assets/demo.gif)


---

## 🚀 Features

-   **Interactive Chat UI:** A clean and responsive web interface built with React and Vite.
-   **PDF Processing:** Ingests any PDF document and extracts its text content, keeping track of page numbers.
-   **Conversational Memory:** Remembers the context of the conversation for seamless follow-up questions.
-   **Source Highlighting (Explainable AI):** For every answer, the application displays the exact text snippets and page numbers from the document that were used as sources, building trust and allowing for verification.
-   **Local & Private Embeddings:** Uses `sentence-transformers` to generate text embeddings locally. No data is sent to external services for the core semantic search.
-   **High-Performance LLM:** Utilizes the Groq API for near-instant answer generation with the powerful Llama 3 model.

---

## 🛠️ Tech Stack

-   **Frontend:** React (with Vite), Axios
-   **Backend:** Python, FastAPI
-   **AI / ML:**
    -   **Orchestration:** LangChain
    -   **LLM Provider:** Groq (Llama 3)
    -   **Embeddings:** Hugging Face `sentence-transformers` (all-MiniLM-L6-v2)
    -   **Vector Store:** ChromaDB (In-memory)
-   **Deployment:**
    -   Backend on Render (coming soon!)
    -   Frontend on Vercel (coming soon!)

---

## ⚙️ Local Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

-   Python 3.8+
-   Node.js and npm

### 1. Clone the repository
git clone https://github.com/YourUsername/ai-paper-navigator.git
cd ai-paper-navigator

### 2. Set up the Backend
# Create and activate a virtual environment
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create a .env file in the root directory and add your Groq API key
echo 'GROQ_API_KEY="gsk_YourGroqApiKeyGoesHere"' > .env

# Run the backend server
uvicorn server:app --reload


The backend will be running at http://127.0.0.1:8000.

### 3. Set up the Frontend
Generated bash
# Open a new terminal in the project root
cd frontend

# Install Node.js dependencies
npm install

# Run the frontend development server
npm run dev

The frontend will be running at http://localhost:5173 (or another port specified in the terminal). Open this URL in your browser.

🗺️ Project Roadmap

Core RAG Pipeline: Implement text extraction, chunking, and Q&A.

Web Interface: Build a functional frontend with React.

Conversational Memory: Enable follow-up questions.

Source Highlighting: Display source snippets for answer verification.

Deployment: Host the backend on Render and frontend on Vercel.

Multiple Document Support: Allow users to upload and chat with a collection of PDFs.

Error Handling & UI Polish: Improve loading states and handle more edge cases.

