# gen-ai

A personal learning/experimentation repo for building with LangChain and LangGraph — covering LLM providers (Google Gemini via `langchain-google-genai`, Groq via `langchain-groq`), prompt templates, agents, and tool use (web search via Serper).

## Structure

- `apps/` — standalone Streamlit chat UIs (plus one plain script).
  - `1_qna_bot.py` — minimal single-turn Q&A using `ChatGoogleGenerativeAI` piped through `StrOutputParser`.
  - `2_groq_bot_memory.py` — agent-based chat using `langchain.agents.create_agent` with a Groq model, the `GoogleSerperAPIWrapper` search tool, and a LangGraph `InMemorySaver` checkpointer for conversational memory.
  - `3_human_in_loop.py` — LangGraph human-in-the-loop email drafting: pauses mid-graph via `interrupt`, resumes via `Command(resume=...)`.
- `blog_app/` — multi-agent LangGraph blog-writing pipeline (research → human review → write → human review → edit), with research/writer/editor agents in `agents.py`, graph wiring in `graph.py`, and shared state in `state.py`.
- `notebooks/` — scratch notebooks exploring LangChain building blocks incrementally: raw LLM invocation, `ChatPromptTemplate` composition into an LCEL chain, `create_agent` with a search tool, and RAG document loading/splitting.
- `data/` — sample documents used by the RAG notebook.

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
- Human-in-the-loop script:
  ```
  python apps/3_human_in_loop.py
  ```
- Notebooks:
  ```
  jupyter notebook
  ```
