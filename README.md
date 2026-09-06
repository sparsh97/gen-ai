# gen-ai

A personal learning/experimentation repo for building with LangChain and LangGraph — covering LLM providers (Google Gemini via `langchain-google-genai`, Groq via `langchain-groq`), prompt templates, agents, and tool use (web search via Serper).

## Structure

- `apps/` — standalone Streamlit chat UIs.
  - `1_qna_bot.py` — minimal single-turn Q&A using `ChatGoogleGenerativeAI` piped through `StrOutputParser`.
  - `2_groq_bot_memory.py` — agent-based chat using `langchain.agents.create_agent` with a Groq model, the `GoogleSerperAPIWrapper` search tool, and a LangGraph `InMemorySaver` checkpointer for conversational memory.
- `notebooks/` — scratch notebooks exploring LangChain building blocks incrementally: raw LLM invocation, `ChatPromptTemplate` composition into an LCEL chain, and `create_agent` with a search tool.

## Setup

1. Create/activate the virtual environment:
   ```
   python -m venv env
   env\Scripts\activate       # PowerShell/cmd
   source env/Scripts/activate  # Git Bash
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the repo root with the required API keys, e.g.:
   ```
   GOOGLE_API_KEY=...
   GROQ_API_KEY=...
   SERPER_API_KEY=...
   ```

## Running

- Streamlit apps:
  ```
  streamlit run apps/1_qna_bot.py
  streamlit run apps/2_groq_bot_memory.py
  ```
- Notebooks:
  ```
  jupyter notebook
  ```
