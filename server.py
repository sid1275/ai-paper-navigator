# server.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

import rag_logic

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW Application State ---
# We now only need to store the single, stateful chain object.
app_state = {
    "chain": None
}

# --- Pydantic Models (Unchanged) ---
class QueryRequest(BaseModel):
    question: str

# --- API Endpoints (MODIFIED) ---

@app.on_event("startup")
def on_startup():
    """This function now does nothing on startup, as the chain is created on upload."""
    print("Server startup complete. Waiting for PDF upload.")

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    
    try:
        # This function now does everything and returns a stateful chain
        chain = rag_logic.process_pdf_and_create_chain(file.file)
        app_state["chain"] = chain
        return {"message": f"Successfully processed '{file.filename}' and created a new chat session."}
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF. Error: {e}")

@app.post("/ask/")
async def ask_question(request: QueryRequest):
    chain = app_state.get("chain")
    if not chain:
        raise HTTPException(status_code=400, detail="No chat session is active. Please upload a PDF first.")
    
    try:
        # The chain now takes the question directly and manages history internally.
        # The result object has a different structure.
        result = chain.invoke({"question": request.question})
        return {"answer": result["answer"]}
    except Exception as e:
        print(f"Error getting answer: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get answer. Error: {e}")

# To restart the chat session (clear memory), the user just re-uploads the PDF.
# We can add an explicit /reset endpoint later if needed.