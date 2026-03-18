# AI Gateway 🧠
    
    > Smart API router for AI requests. Automatically routes to the cheapest available provider.
    
    [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
    [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
    
    ## Why AI Gateway?
    
    When you build AI applications, you're paying too much. Different providers have wildly different prices for similar quality:
    
    | Model | Provider | Cost per 1M tokens |
    |-------|----------|-------------------|
    | llama-3.1-8b | Groq | $0.10 |
    | gpt-4o-mini | OpenAI | $0.15 |
    | claude-3-haiku | Anthropic | $0.80 |
    
    **AI Gateway automatically routes your requests to the cheapest provider that meets your quality needs.**
    
    ## Features
    
    - 🔄 **Automatic Routing** - Pick "auto" and get the best price
    - 🛡️ **Fallback** - Seamlessly switches providers on failure
    - 📊 **Usage Tracking** - See where your money goes
    - 🚀 **Drop-in Compatible** - Works with your existing OpenAI code
    - 🌐 **Open Source** - No vendor lock-in
    
    ## Installation
    
    ```bash
    pip install ai-gateway
    ```
    
    ## Quick Start
    
    ```python
    from ai_gateway import AI Gateway
    
    gateway = AIGateway()
    
    # Automatically routes to cheapest provider
    response = await gateway.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": "Explain quantum computing"}]
    )
    
    print(response.choices[0].message.content)
    ```
    
    ## Configuration
    
    Set your API keys as environment variables:
    
    ```bash
    export GROQ_API_KEY=your_groq_key
    export OPENAI_API_KEY=your_openai_key
    export ANTHROPIC_API_KEY=your_anthropic_key
    export OPENROUTER_API_KEY=your_openrouter_key
    ```
    
    ## Running the Server
    
    ```bash
    python -m ai_gateway.server --port 8080
    ```
    
    Then use it as a proxy:
    
    ```python
    import openai
    
    client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key="none")
    
    # This gets automatically routed to cheapest provider
    response = client.chat.completions.create(
        model="auto",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    ```
    
    ## Architecture
    
    ```
    ┌─────────────┐
    │   Client    │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  AI Gateway │  ← Routes requests based on cost/availability
    └──────┬──────┘
           │
       ┌───┴───┬────────┐
       ▼       ▼        ▼
    ┌─────┐ ┌─────┐ ┌──────┐
    │Groq │ │OpenAI│ │Anthropic│
    └─────┘ └─────┘ └──────┘
    ```
    
    ## License
    
    MIT © AI Gateway Contributors
    