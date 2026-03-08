import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

openai.api_key = "PASTE_YOUR_OPENAI_API_KEY_HERE"  # USER should replace this

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    class_id: str = "10" # default example
    subject: str = "science"
    chapter: str = "chapter_1"
    query: str

@app.post("/chat")
async def chat(request: ChatRequest):
    data_path = f"data/class_{request.class_id}/{request.subject}/{request.chapter}/context.txt"
    
    if not os.path.exists(data_path):
        return {"response": f"Sorry, I don't have the context for {request.subject} {request.chapter} for Class {request.class_id}. Please make sure to add it to the data folder!"}

    with open(data_path, "r") as f:
        context = f.read()

    # Simple RAG: Context + Query
    prompt = f"Context from the textbook:\n{context}\n\nQuestion: {request.query}\nAnswer based ONLY on the context above. If the context doesn't contain the answer, say you don't know."

    # Using OpenAI as an example. You can replace this with any LLM.
    # If the user doesn't have an API key, we could return a mock "Context-based answer"
    try:
        # response = openai.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful educational tutor."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        # return {"response": response.choices[0].message.content}
        
        # MOCK Response for demonstration if no API key is provided
        # In a real environment, uncomment the openai part above.
        mock_response = f"(MOCK RAG RESPONSE) Based on the chapter context, you asked about '{request.query}'. The textbook mentions: '{context[:100]}...'"
        return {"response": mock_response}
        
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
