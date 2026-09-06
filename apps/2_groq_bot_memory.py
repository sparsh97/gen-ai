from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_community.utilities import GoogleSerperAPIWrapper
import streamlit as st

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", streaming=True)
search = GoogleSerperAPIWrapper()

st.title("My Qna Bot")

if "messages" not in st.session_state:
    st.session_state.messages = InMemorySaver()
    st.session_state.history = []


agent = create_agent(
        model=llm,
        tools=[search.run],
        system_prompt="You are a AI Agent. You need to provide answer to user questions.",
        checkpointer=st.session_state.messages
    )

for message in st.session_state.history:
    role = message['role']
    content = message['content']
    st.chat_message(role).markdown(content)

query = st.chat_input(placeholder="Enter your query")
if query:
    st.session_state.history.append({"role":"user", "content": query})
    st.chat_message(name="human").markdown(query)
    res = agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        {"configurable": {"thread_id": "thread-1"}},
        stream_mode="values",
    )
    for r in res:
        last_message = r["messages"][-1]
        if last_message.type == "ai" and last_message.content:
            st.chat_message(name="ai").markdown(last_message.content)
            st.session_state.history.append({"role": "assistant", "content": last_message.content})


