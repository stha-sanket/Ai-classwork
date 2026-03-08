import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3:8b" 

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    class_id: str
    subject: str
    chapter: str
    query: str

@app.get("/")
async def root():
    return {"message": "EduBrain API is running!", "status": "online"}

@app.post("/chat")
async def chat(request: ChatRequest):
    data_path = f"data/class_{request.class_id}/{request.subject}/{request.chapter}/context.txt"
    
    if not os.path.exists(data_path):
        return {"response": f"Sorry, I don't have the context for {request.subject} {request.chapter} for Class {request.class_id}. Please make sure to add it to the data folder!"}

    with open(data_path, "r") as f:
        context = f.read()

    # System prompt to restrict answers to the context
    system_prompt = (
        "You are a helpful educational tutor. "
        "Use ONLY the following context to answer the student's question. "
        "If the answer is not in the context, say: 'I'm sorry, that specific information is not in this chapter.' "
        "Keep your response concise and student-friendly.\n\n"
        f"CHAPTER CONTEXT:\n{context}"
    )

    ollama_payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.query}
        ],
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(OLLAMA_URL, json=ollama_payload)
            response.raise_for_status()
            result = response.json()
            return {"response": result['message']['content']}
            
    except httpx.ConnectError:
        return {"response": "Error: Could not connect to Ollama. Make sure it is running on http://localhost:11434!"}
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
