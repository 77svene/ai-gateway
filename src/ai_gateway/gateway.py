"""AI Gateway core implementation."""
    
    from typing import Optional, List, Dict, Any
    import asyncio
    import httpx
    from dataclasses import dataclass
    from enum import Enum
    
    class Provider(Enum):
        GROQ = "groq"
        OPENAI = "openai"
        ANTHROPIC = "anthropic"
        OPENROUTER = "openrouter"
    
    @dataclass
    class ModelInfo:
        name: str
        provider: Provider
        cost_per_million: float
        supports_vision: bool = False
    
    # Model registry with pricing
    MODELS: Dict[str, ModelInfo] = {
        # Groq - cheapest option
        "llama-3.1-8b-instant": ModelInfo("llama-3.1-8b-instant", Provider.GROQ, 0.10),
        "llama-3.1-70b-versatile": ModelInfo("llama-3.1-70b-versatile", Provider.GROQ, 0.70),
        "mixtral-8x7b-32768": ModelInfo("mixtral-8x7b-32768", Provider.GROQ, 0.24),
        
        # OpenAI
        "gpt-4o-mini": ModelInfo("gpt-4o-mini", Provider.OPENAI, 0.15),
        "gpt-4o": ModelInfo("gpt-4o", Provider.OPENAI, 2.50),
        
        # Anthropic
        "claude-3-haiku-20240307": ModelInfo("claude-3-haiku-20240307", Provider.ANTHROPIC, 0.80, True),
        "claude-3.5-sonnet-20240620": ModelInfo("claude-3.5-sonnet-20240620", Provider.ANTHROPIC, 3.00, True),
        
        # Auto selects cheapest
        "auto": ModelInfo("auto", Provider.GROQ, 0.10),
    }
    
    class AIGateway:
        """Smart AI request router."""
        
        def __init__(self):
            self.providers = {
                Provider.GROQ: GroqProvider(),
                Provider.OPENAI: OpenAIProvider(),
                Provider.ANTHROPIC: AnthropicProvider(),
            }
            self.usage_stats: Dict[str, int] = {}
        
        def get_cheapest_model(self, requires_vision: bool = False) -> ModelInfo:
            """Get the cheapest available model."""
            candidates = [
                m for m in MODELS.values() 
                if m.name != "auto" and (not requires_vision or m.supports_vision)
            ]
            return min(candidates, key=lambda x: x.cost_per_million)
        
        async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            model: str = "auto",
            **kwargs
        ) -> Dict[str, Any]:
            """Route and execute chat completion request."""
            if model == "auto":
                model_info = self.get_cheapest_model()
            else:
                model_info = MODELS.get(model, self.get_cheapest_model())
            
            provider = self.providers[model_info.provider]
            
            try:
                result = await provider.chat_completion(messages, model_info.name, **kwargs)
                self.usage_stats[model_info.provider.value] = self.usage_stats.get(model_info.provider.value, 0) + 1
                return result
            except Exception as e:
                # Fallback to next cheapest
                fallback = self.get_cheapest_model()
                if fallback != model_info:
                    return await self.providers[fallback.provider].chat_completion(
                        messages, fallback.name, **kwargs
                    )
                raise
    
    class GroqProvider:
        """Groq API provider."""
        
        def __init__(self):
            self.base_url = "https://api.groq.com/openai/v1"
        
        async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            model: str,
            **kwargs
        ) -> Dict[str, Any]:
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not set")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"model": model, "messages": messages, **kwargs},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
    
    class OpenAIProvider:
        """OpenAI API provider."""
        
        async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            model: str,
            **kwargs
        ) -> Dict[str, Any]:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set")
            
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key)
            result = await client.chat.completions.create(
                model=model, messages=messages, **kwargs
            )
            return result.model_dump()
    
    class AnthropicProvider:
        """Anthropic API provider."""
        
        async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            model: str,
            **kwargs
        ) -> Dict[str, Any]:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "max_tokens": kwargs.get("max_tokens", 1024)
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                # Convert to OpenAI format
                return {
                    "choices": [{
                        "message": {"role": "assistant", "content": data["content"][0]["text"]},
                        "finish_reason": data.get("stop_reason", "stop")
                    }],
                    "usage": data.get("usage", {})
                }