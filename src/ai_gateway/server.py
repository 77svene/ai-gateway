"""AI Gateway FastAPI server."""
    
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Optional, Dict, Any
    import os
    
    from ai_gateway import AIGateway
    
    app = FastAPI(title="AI Gateway")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    gateway = AIGateway()
    
    class Message(BaseModel):
        role: str
        content: str
    
    class ChatRequest(BaseModel):
        model: str = "auto"
        messages: List[Message]
        temperature: Optional[float] = 0.7
        max_tokens: Optional[int] = 1024
    
    @app.post("/v1/chat/completions")
    async def chat_completions(request: ChatRequest):
        """Proxy endpoint for chat completions."""
        try:
            result = await gateway.chat_completion(
                messages=[m.model_dump() for m in request.messages],
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.get("/v1/models")
    async def list_models():
        """List available models."""
        return {
            "data": [
                {"id": name, "object": "model", "created": 1677610602, "owned_by": info.provider.value}
                for name, info in MODELS.items()
            ]
        }
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "usage": gateway.usage_stats}
    
    if __name__ == "__main__":
        import uvicorn
        port = int(os.environ.get("PORT", 8080))
        uvicorn.run(app, host="0.0.0.0", port=port)