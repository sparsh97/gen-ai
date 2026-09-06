from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
parser = StrOutputParser()
st.title("My Qna Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message['role']
    content = message['content']
    st.chat_message(role).markdown(content)

query = st.chat_input(placeholder="Enter your query")
if query:
    st.session_state.messages.append({"role":"user", "content": query})
    st.chat_message(name="human").markdown(query)
    res = (llm | parser).invoke(query)
    st.chat_message(name="ai").markdown(res)
    st.session_state.messages.append({"role":"assistant", "content": res})                    