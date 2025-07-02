# rag_logic.py

from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

# --- NEW IMPORTS for Memory and a new Chain Type ---
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# --- CORE RAG FUNCTIONS (Mostly Unchanged) ---

def extract_text_from_pdf(pdf_file):
    print("Reading PDF...")
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    print("PDF reading complete.")
    return text

def chunk_text(text):
    print("Starting text chunking...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    cleaned_chunks = [chunk for chunk in chunks if len(chunk) > 100]
    print(f"Text successfully split and cleaned into {len(cleaned_chunks)} chunks.")
    return cleaned_chunks

def create_vector_store(chunks):
    print("Creating vector store with local embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(texts=chunks, embedding=embeddings)
    print("Vector store created successfully.")
    return vector_store

# --- MODIFIED CHAIN CREATION ---
def create_conversational_rag_chain(retriever):
    """
    Creates the Conversational RAG chain with memory.
    This function now takes the retriever as an argument.
    """
    print("Creating Conversational RAG chain...")
    
    # 1. Initialize Memory
    # `return_messages=True` ensures the history is stored as a list of message objects.
    # `memory_key='chat_history'` is the variable name the chain will use for history.
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # 2. Initialize the LLM
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.2)
    
    # 3. Create the ConversationalRetrievalChain
    # This chain is smart. It can use the chat history to rephrase a follow-up
    # question into a standalone question before sending it to the retriever.
    # For example, if you ask "what about it?", it might rephrase it to
    # "what about the Transformer model?" based on the history.
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        # We can optionally add a prompt here to condense the question if needed,
        # but the default usually works well.
    )
    
    print("Conversational RAG chain created.")
    return chain

# --- ORCHESTRATION FUNCTIONS (Simplified) ---

def process_pdf_and_create_chain(pdf_file):
    """The complete pipeline to process a PDF and return a ready-to-use chain."""
    raw_text = extract_text_from_pdf(pdf_file)
    text_chunks = chunk_text(raw_text)
    vector_store = create_vector_store(text_chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    # The chain is now created *after* the PDF is processed
    chain = create_conversational_rag_chain(retriever)
    return chain