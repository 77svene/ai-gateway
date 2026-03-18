# AI Gateway 🚀
    
    **Smart API router for AI requests — automatically routes to the cheapest provider.**
    
    ## Why This Exists
    
    Most AI developers overpay by manually switching between providers. AI Gateway does it automatically.
    
    ### Features
    - **Automatic cost optimization** — Routes requests to the cheapest capable provider
    - **Fallback support** — If one provider fails, automatically retries with another
    - **Unified API** — Single interface for OpenAI, Anthropic, Gemini, Ollama, and more
    - **Cost tracking** — Built-in usage monitoring
    
    ## Quick Start
    
    ```bash
    pip install ai-gateway
    ```
    
    ```python
    from ai_gateway import Router
    
    router = Router()
    response = await router.generate("Explain quantum computing", model="claude-3-haiku")  # Gets routed to cheapest
    ```
    
    ## Pricing Comparison (Example: 1M tokens)
    
    | Provider | Model | Cost |
    |----------|-------|------|
    | OpenAI | gpt-4o-mini | $0.15 |
    | Anthropic | claude-3-haiku | $0.25 |
    | **AI Gateway** | auto-route | **$0.15** |
    
    Save up to 60% on AI inference costs.
    
    ## Supported Providers
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude 3, Claude 2)
    - Google (Gemini)
    - Groq
    - Ollama (local models)
    
    ---
    
    *Star this repo if it saves you money!*
    