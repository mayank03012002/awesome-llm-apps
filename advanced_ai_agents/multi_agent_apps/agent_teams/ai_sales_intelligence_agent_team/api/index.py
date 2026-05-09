from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import root_agent

app = FastAPI(title="AI Sales Intelligence Agent API")

# Configure CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/chat", response_model=QueryResponse)
def chat_endpoint(request: QueryRequest):
    try:
        # Depending on google-adk version, it could be root_agent.run() or root_agent()
        # Trying typical agent run methods:
        if hasattr(root_agent, "run"):
            result = root_agent.run(request.query)
        else:
            result = root_agent(request.query)
            
        # Extract text from result if it's an object, else return string
        if hasattr(result, "text"):
            response_text = result.text
        elif hasattr(result, "content"):
            response_text = result.content
        else:
            response_text = str(result)
            
        return QueryResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
