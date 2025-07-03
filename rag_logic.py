# rag_logic.py

from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

# --- NEW IMPORTS for Memory and a new Chain Type ---
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# At the top of rag_logic.py, with the other imports
from langchain.schema import Document

# --- CORE RAG FUNCTIONS (Mostly Unchanged) ---

# In rag_logic.py

# In rag_logic.py

# Add this import at the top
from langchain.schema import Document

# ... other imports ...

def extract_pages_from_pdf(pdf_file):
    """Extracts text and page number from each page of a PDF."""
    print("Reading PDF pages...")
    pdf_reader = PdfReader(pdf_file)
    docs = [] # We'll call it docs now to be clear
    for i, page in enumerate(pdf_reader.pages):
        page_text = page.extract_text()
        if page_text:
            # --- THE FIX IS HERE ---
            # Create a LangChain Document object instead of a Python dict.
            docs.append(Document(
                page_content=page_text,
                metadata={"page": i + 1}
            ))
    print(f"Extracted and created {len(docs)} Document objects.")
    return docs

def chunk_pages(pages):
    """Splits pages into smaller, cleaned chunks while preserving metadata."""
    print("Starting page chunking...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    # The splitter can process documents with metadata and will keep it attached to the chunks
    chunks = text_splitter.split_documents(pages)
    
    # We'll skip the extra cleaning step for now, as the splitter is quite good.
    print(f"Text successfully split into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks):
    """Creates a vector store from chunks using a local embedding model."""
    print("Creating vector store with local embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Chroma can directly accept documents with metadata
    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings)
    print("Vector store created successfully.")
    return vector_store

# In rag_logic.py

def create_conversational_rag_chain(retriever):
    """Creates the Conversational RAG chain with memory."""
    print("Creating Conversational RAG chain...")
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        output_key='answer' # Explicitly set the output key
    )
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.2)
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True, # <-- THIS IS THE MOST CRITICAL LINE
        output_key='answer'
    )
    
    print("Conversational RAG chain created.")
    return chain

# --- ORCHESTRATION FUNCTIONS (Simplified) ---

# ... (create_conversational_rag_chain remains the same) ...

def process_pdf_and_create_chain(pdf_file):
    """The complete pipeline to process a PDF and return a ready-to-use chain."""
    pages = extract_pages_from_pdf(pdf_file)
    chunks_with_metadata = chunk_pages(pages)
    vector_store = create_vector_store(chunks_with_metadata)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    chain = create_conversational_rag_chain(retriever)
    return chain