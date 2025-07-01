import os
from pypdf import PdfReader
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# --- New Imports for Generation ---
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return ""
    print(f"Reading PDF from: {pdf_path}")
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text: # Ensure text was extracted
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
    print(f"Text successfully split into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks):
    print("Creating vector store with local embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(texts=chunks, embedding=embeddings)
    print("Vector store created successfully.")
    return vector_store

# --- NEW FUNCTION ---
def generate_answer(query, vector_store):
    """
    Retrieves relevant documents and generates a final answer using an LLM.
    """
    print("\n--- Generating Final Answer ---")
    
    # 1. Retrieve relevant documents
    print("Searching for relevant documents...")
    relevant_docs = vector_store.similarity_search(query, k=4) # Get top 4 docs
    # Combine the content of the retrieved documents into a single context string
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # 2. Define the prompt template
    prompt_template = """
    You are a helpful AI assistant. Use the following context from a research paper
    to answer the user's question. If you don't know the answer from the context,
    just say that you don't know. Do not make up information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # 3. Initialize the LLM (using Groq)
    # We are using Llama 3, a powerful open-source model.
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.2)
    
    # 4. Create and run the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke({"context": context, "question": query})
    
    return response['text']


if __name__ == "__main__":
    pdf_file_path = os.path.join("documents", "attention.pdf")
    
    document_text = extract_text_from_pdf(pdf_file_path)
    
    if document_text:
        text_chunks = chunk_text(document_text)
        
        # --- NEW CLEANING STEP ---
        # Filter out very short or nonsensical chunks
        cleaned_chunks = [chunk for chunk in text_chunks if len(chunk) > 100 and "..." not in chunk]
        print(f"Filtered chunks, retaining {len(cleaned_chunks)} chunks.")

        vector_store = create_vector_store(cleaned_chunks)
        
        # Ask the question
        query = "What is the main idea of the attention mechanism in the Transformer model?"
        final_answer = generate_answer(query, vector_store)
        
        print("\n\n================ FINAL ANSWER ================")
        print(f"Question: {query}")
        print(f"Answer: {final_answer}")
        print("==========================================")
    
    else:
        print("\nCould not extract text from the PDF.")